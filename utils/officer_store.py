from __future__ import annotations

import base64
import json
import os
from pathlib import Path
from urllib import error, parse, request


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
OFFICERS_PATH = DATA_DIR / "officers.json"
OFFICER_ROLES = ["社長", "副社長", "總務", "攝錄", "點心", "文書"]
GITHUB_REPO = "11104170-star/Tea-Ceremony-Club-Executive-Platform"
GITHUB_BRANCH = "main"
GITHUB_DATA_PATH = "data/officers.json"


def get_secret(name: str) -> str:
    value = os.getenv(name, "").strip()
    if value:
        return value

    try:
        import streamlit as st

        return str(st.secrets.get(name, "")).strip()
    except Exception:
        return ""


def github_token() -> str:
    return get_secret("GITHUB_TOKEN")


def github_contents_url() -> str:
    encoded_path = parse.quote(GITHUB_DATA_PATH)
    return f"https://api.github.com/repos/{GITHUB_REPO}/contents/{encoded_path}"


def github_request(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")

    req = request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )

    with request.urlopen(req, timeout=15) as response:
        return json.loads(response.read().decode("utf-8"))


def load_remote_officers(token: str) -> list[dict[str, str]] | None:
    url = f"{github_contents_url()}?ref={parse.quote(GITHUB_BRANCH)}"

    try:
        response = github_request("GET", url, token)
    except (OSError, error.HTTPError, json.JSONDecodeError):
        return None

    content = response.get("content", "")
    if not content:
        return []

    try:
        decoded = base64.b64decode(content).decode("utf-8")
        data = json.loads(decoded)
    except (ValueError, json.JSONDecodeError):
        return None

    return normalize_officers(data)


def save_remote_officers(officers: list[dict[str, str]], token: str) -> bool:
    url = f"{github_contents_url()}?ref={parse.quote(GITHUB_BRANCH)}"
    sha = None

    try:
        current_file = github_request("GET", url, token)
        sha = current_file.get("sha")
    except error.HTTPError as exc:
        if exc.code != 404:
            return False
    except (OSError, json.JSONDecodeError):
        return False

    content = json.dumps(officers, ensure_ascii=False, indent=2)
    encoded_content = base64.b64encode(content.encode("utf-8")).decode("ascii")
    payload = {
        "message": "Update officer list",
        "content": encoded_content,
        "branch": GITHUB_BRANCH,
    }

    if sha:
        payload["sha"] = sha

    try:
        github_request("PUT", github_contents_url(), token, payload)
    except (OSError, error.HTTPError, json.JSONDecodeError):
        return False

    return True


def normalize_officers(data: object) -> list[dict[str, str]]:
    if not isinstance(data, list):
        return []

    officers = []
    for item in data:
        if not isinstance(item, dict):
            continue

        name = str(item.get("姓名", "")).strip()
        student_id = str(item.get("學號", "")).strip()
        role = str(item.get("職位", "")).strip()

        if name:
            officers.append({"姓名": name, "學號": student_id, "職位": role})

    return officers


def load_officers() -> list[dict[str, str]]:
    token = github_token()
    if token:
        remote_officers = load_remote_officers(token)
        if remote_officers is not None:
            return remote_officers

    if not OFFICERS_PATH.exists():
        return []

    try:
        data = json.loads(OFFICERS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

    return normalize_officers(data)


def save_officers(officers: list[dict[str, str]]) -> None:
    token = github_token()
    if token and save_remote_officers(officers, token):
        return

    DATA_DIR.mkdir(exist_ok=True)
    OFFICERS_PATH.write_text(
        json.dumps(officers, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def storage_label() -> str:
    if github_token():
        return "GitHub 永久儲存"

    return "本機檔案儲存"


def add_officer(*, name: str, student_id: str, role: str) -> None:
    officers = load_officers()
    officers.append(
        {
            "姓名": name.strip(),
            "學號": student_id.strip(),
            "職位": role.strip(),
        }
    )
    save_officers(officers)


def delete_officer(index: int) -> None:
    officers = load_officers()
    if 0 <= index < len(officers):
        del officers[index]
        save_officers(officers)


def move_officer(index: int, direction: int) -> None:
    officers = load_officers()
    new_index = index + direction

    if not 0 <= index < len(officers):
        return

    if not 0 <= new_index < len(officers):
        return

    officers[index], officers[new_index] = officers[new_index], officers[index]
    save_officers(officers)


def move_officer_to_top(index: int) -> None:
    officers = load_officers()

    if not 0 <= index < len(officers):
        return

    officer = officers.pop(index)
    officers.insert(0, officer)
    save_officers(officers)


def format_officer_label(officer: dict[str, str]) -> str:
    name = officer.get("姓名", "")
    role = officer.get("職位", "")
    student_id = officer.get("學號", "")

    details = "、".join(item for item in (role, student_id) if item)
    if details:
        return f"{name}（{details}）"

    return name
