import streamlit as st

from utils.auth import require_login, logout_button


st.set_page_config(
    page_title="社員管理 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

st.title("社員管理")
st.caption("維護社員基本資料，後續可加入匯入、查詢與出缺席紀錄。")

st.subheader("新增社員")
col1, col2, col3 = st.columns(3)

with col1:
    st.text_input("姓名")
with col2:
    st.text_input("學號")
with col3:
    st.selectbox("身分", ["社員", "幹部", "顧問"])

st.button("新增", type="primary", disabled=True)

st.subheader("社員列表")
st.dataframe(
    [
        {"姓名": "範例社員", "學號": "S000000", "身分": "社員", "狀態": "正常"},
    ],
    use_container_width=True,
)
