# 茶道社幹部平台

Streamlit 多頁平台專案，首頁提供登入，功能頁放在 `pages` 資料夾由 Streamlit 自動管理。

## 專案結構

```text
.
├── app.py
├── assets
│   └── 成果書模板_已標記.docx
├── pages
│   ├── 1_成果書生成.py
│   ├── 2_問卷分析.py
│   ├── 3_AI工具.py
│   └── 4_社員管理.py
├── utils
│   ├── __init__.py
│   └── auth.py
├── requirements.txt
└── .streamlit
    └── secrets.toml.example
```

## 啟動方式

1. 安裝套件：

```bash
pip install -r requirements.txt
```

2. 建立 `.streamlit/secrets.toml`：

```toml
PASSWORD = "你的平台密碼"
```

3. 啟動平台：

```bash
streamlit run app.py
```

## 成果書生成

`成果書生成` 頁面已整合舊成果書系統，可使用內建 Word 範本，也可以上傳自訂 `.docx` 範本。問卷資料支援 `.xlsx` 與 `.csv`，照片支援 `.jpg`、`.jpeg`、`.png`。
