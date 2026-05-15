# Codex Notes

## Project

茶道社幹部平台，使用 Streamlit 多頁架構。

## Run

```bash
streamlit run app.py
```

## Key Pages

- `app.py`: 首頁與登入入口。
- `pages/1_成果書生成.py`: 成果書生成、問卷分析結果填入 Word、活動負責人選擇。
- `pages/4_幹部管理.py`: 幹部名單管理，提供成果書活動負責人選項。
- `pages/5_行事曆.py`: 行事曆管理。

## Persistent Data

- `data/officers.json`: 幹部名單。
- `data/calendar_events.json`: 行事曆活動。
- 若設定 `GITHUB_TOKEN`，資料會優先永久寫入 GitHub repo。
- 未設定 `GITHUB_TOKEN` 時，改用本機檔案儲存。

## Secrets

Streamlit Secrets 可設定：

```toml
PASSWORD = "平台密碼"
GEMINI_API_KEY = "Gemini API key"
GEMINI_MODEL = "gemini-2.5-flash"
GITHUB_TOKEN = "GitHub fine-grained token"
```

`GITHUB_TOKEN` 需要 repo `Contents` 的 read/write 權限。

## Git

Remote 使用 SSH：

```text
git@github.com:11104170-star/Tea-Ceremony-Club-Executive-Platform.git
```
