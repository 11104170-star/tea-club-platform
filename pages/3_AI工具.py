import streamlit as st

from utils.auth import require_login, logout_button


st.set_page_config(
    page_title="AI工具 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

st.title("AI工具")
st.caption("協助產生活動文案、公告草稿與行政內容。")

tool_type = st.selectbox(
    "工具類型",
    ["活動公告", "成果摘要", "社群貼文", "會議紀錄整理"],
)

st.text_area("輸入素材", height=180, placeholder="貼上活動資訊、重點或原始文字...")

col1, col2 = st.columns([1, 4])
with col1:
    st.button("產生內容", type="primary", disabled=True)
with col2:
    st.caption("此頁目前為基本 UI，AI 串接可於後續擴充。")

st.subheader("輸出結果")
st.text_area("產生結果", height=220, disabled=True)
