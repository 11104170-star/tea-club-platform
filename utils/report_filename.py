import re


def report_date_digits(activity_date: str) -> str:
    digits = re.sub(r"\D", "", activity_date or "")

    if len(digits) == 8 and digits.startswith(("19", "20")):
        roc_year = int(digits[:4]) - 1911
        return f"{roc_year:03d}{digits[4:8]}"

    if len(digits) == 7:
        return digits

    if len(digits) == 6:
        return f"0{digits}"

    return digits or "日期"


def safe_file_name(name: str) -> str:
    cleaned = re.sub(r'[\\/:*?"<>|]', "", name or "").strip()
    return cleaned or "活動"


def achievement_report_file_name(activity_date: str, activity_name: str) -> str:
    return f"10-{report_date_digits(activity_date)}{safe_file_name(activity_name)}_成果報告表.docx"
