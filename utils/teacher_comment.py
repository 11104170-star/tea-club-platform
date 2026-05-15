from __future__ import annotations


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

    from openai import OpenAI

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
- 80 到 140 字
- 不要捏造未提供的活動細節

活動名稱：{activity_name or "未填"}
活動檢討：{activity_review or "未填"}
照片說明：
{descriptions or "未填"}
""".strip()

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=model,
        input=[
            {
                "role": "developer",
                "content": "你是協助學校社團撰寫成果書的行政文字助手。",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        max_output_tokens=300,
    )

    return response.output_text.strip()
