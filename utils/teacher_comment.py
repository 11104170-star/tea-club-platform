from __future__ import annotations

import base64
import json
from urllib import error, parse, request


def generate_gemini_text(
    *,
    api_key: str,
    model: str,
    system_instruction: str,
    prompt: str,
    images: list[object] | None = None,
) -> str:
    parts = [{"text": prompt}]

    for image in images or []:
        if image is None:
            continue

        mime_type = getattr(image, "type", None) or "image/png"
        image_data = base64.b64encode(image.getvalue()).decode("ascii")
        parts.append(
            {
                "inlineData": {
                    "mimeType": mime_type,
                    "data": image_data,
                }
            }
        )

    payload = {
        "systemInstruction": {
            "parts": [{"text": system_instruction}],
        },
        "contents": [
            {
                "role": "user",
                "parts": parts,
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 500,
        },
    }
    encoded_model = parse.quote(model, safe="")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/"
        f"models/{encoded_model}:generateContent"
    )
    req = request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
    )

    try:
        with request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (OSError, error.HTTPError, json.JSONDecodeError) as exc:
        raise RuntimeError("Gemini API 呼叫失敗，請確認 GEMINI_API_KEY 與 GEMINI_MODEL。") from exc

    texts = []
    for candidate in data.get("candidates", []):
        content = candidate.get("content", {})
        for part in content.get("parts", []):
            text = part.get("text")
            if text:
                texts.append(text)

    generated_text = "\n".join(texts).strip()
    if not generated_text:
        raise RuntimeError("Gemini API 未回傳文字內容。")

    return generated_text


def fallback_teacher_comment(
    *,
    activity_name: str,
    activity_review: str,
    photo_descriptions: list[str],
) -> str:
    descriptions = [item.strip() for item in photo_descriptions if item.strip()]

    if descriptions:
        photo_summary = "、".join(descriptions)
        detail = f"從照片紀錄可見，活動包含{photo_summary}等內容，展現出社團活動的完整規劃與執行成果。"
    else:
        detail = "從活動紀錄可見，活動流程安排完整，參與同學能在過程中投入學習並完成預定目標。"

    review_sentence = ""
    if activity_review.strip():
        review_sentence = f"幹部亦能針對活動進行檢討，包含「{activity_review.strip()}」，有助於後續活動持續精進。"

    name = activity_name.strip() or "本次活動"

    return (
        f"{name}整體辦理情形良好，活動內容具教育意義，並能呈現茶道社重視禮節、實作與團隊合作的精神。"
        f"{detail}{review_sentence}期許社團持續累積經驗，讓未來活動更加完善。"
    )


def fallback_activity_overview(
    *,
    activity_name: str,
    photo_descriptions: list[str],
) -> str:
    descriptions = [item.strip() for item in photo_descriptions if item.strip()]
    name = activity_name.strip() or "本次活動"

    if descriptions:
        joined_descriptions = "、".join(descriptions)
        return (
            f"{name}以茶道學習與實作體驗為核心，透過{joined_descriptions}等活動內容，"
            "引導參與者認識茶席禮儀、茶具使用與泡茶流程，並在實際操作中體會茶道文化的精神。"
        )

    return (
        f"{name}以茶道學習與實作體驗為主軸，安排社員參與茶道相關流程，"
        "讓參與者在活動中認識茶文化、培養禮節觀念，並增進社團成員之間的互動與合作。"
    )


def is_weak_activity_overview(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 45:
        return True

    if not stripped.endswith(("。", "！", "？")):
        return True

    weak_phrases = (
        "本次活動內容豐富多元",
        "旨在提供社員",
        "透過多元活動",
    )
    return any(phrase in stripped for phrase in weak_phrases)


def is_weak_teacher_comment(text: str) -> bool:
    stripped = text.strip()
    if len(stripped) < 45:
        return True

    if not stripped.endswith(("。", "！", "？")):
        return True

    weak_phrases = (
        "本次茶道社的社團活動",
        "社員們展現了積極的參與熱情",
        "整體而言",
    )
    return any(phrase in stripped for phrase in weak_phrases)


def generate_teacher_comment(
    *,
    api_key: str | None,
    model: str,
    activity_name: str,
    activity_review: str,
    photo_descriptions: list[str],
) -> str:
    if not api_key:
        return fallback_teacher_comment(
            activity_name=activity_name,
            activity_review=activity_review,
            photo_descriptions=photo_descriptions,
        )

    descriptions = "\n".join(
        f"- {description.strip()}"
        for description in photo_descriptions
        if description.strip()
    )

    prompt = f"""
請根據茶道社成果書資料，生成一段「指導老師評語」。

要求：
- 使用繁體中文
- 語氣像學校成果書中的老師評語
- 溫和、正式、肯定學生努力
- 不要條列
- 80 到 140 字，必須是一段完整句子並以句號結尾
- 不要捏造未提供的活動細節
- 不要使用「本次茶道社的社團活動」或「社員們展現了積極的參與熱情」這類空泛模板語句

活動名稱：{activity_name or "未填"}
活動檢討：{activity_review or "未填"}
照片說明：
{descriptions or "未填"}
""".strip()

    generated_text = generate_gemini_text(
        api_key=api_key,
        model=model,
        system_instruction="你是協助學校社團撰寫成果書的行政文字助手。",
        prompt=prompt,
    )

    if is_weak_teacher_comment(generated_text):
        return fallback_teacher_comment(
            activity_name=activity_name,
            activity_review=activity_review,
            photo_descriptions=photo_descriptions,
        )

    return generated_text


def generate_activity_overview(
    *,
    api_key: str | None,
    model: str,
    activity_name: str,
    photo_descriptions: list[str],
    photos: list[object] | None = None,
) -> str:
    if not api_key:
        return fallback_activity_overview(
            activity_name=activity_name,
            photo_descriptions=photo_descriptions,
        )

    descriptions = "\n".join(
        f"- {description.strip()}"
        for description in photo_descriptions
        if description.strip()
    )

    prompt = f"""
請根據茶道社成果書資料，生成一段「活動內容概述」。

要求：
- 使用繁體中文
- 適合放在學校活動成果報告表
- 內容正式、清楚、具體
- 不要條列
- 80 到 140 字，必須是一段完整句子並以句號結尾
- 若有上傳照片，優先根據照片內容撰寫；照片說明只作為輔助線索
- 不要捏造未提供的細節
- 不要使用「本次活動內容豐富多元」或「旨在提供社員」這類空泛模板語句

活動名稱：{activity_name or "未填"}
照片說明：
{descriptions or "未填"}
""".strip()

    generated_text = generate_gemini_text(
        api_key=api_key,
        model=model,
        system_instruction="你是協助學校社團撰寫成果報告表的行政文字助手。",
        prompt=prompt,
        images=photos,
    )

    if is_weak_activity_overview(generated_text):
        return fallback_activity_overview(
            activity_name=activity_name,
            photo_descriptions=photo_descriptions,
        )

    return generated_text
