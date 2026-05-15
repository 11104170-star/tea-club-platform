import streamlit as st

from utils.auth import require_login, logout_button


st.set_page_config(
    page_title="問卷分析 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

st.title("問卷分析")
st.caption("匯入問卷資料，後續可建立統計摘要與圖表。")

uploaded_file = st.file_uploader("上傳問卷資料", type=["xlsx", "csv"])

if uploaded_file:
    st.success("檔案已上傳，可於後續加入 pandas 分析流程。")
else:
    st.info("請上傳 Excel 或 CSV 問卷資料。")

st.subheader("分析摘要")
metric_col1, metric_col2, metric_col3 = st.columns(3)
metric_col1.metric("回覆數", "-")
metric_col2.metric("平均滿意度", "-")
metric_col3.metric("待追蹤項目", "-")

st.subheader("資料預覽")
st.dataframe([], use_container_width=True)
