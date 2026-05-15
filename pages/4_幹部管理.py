import streamlit as st

from utils.auth import require_login, logout_button


st.set_page_config(
    page_title="幹部管理 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

OFFICER_ROLES = ["社長", "副社長", "總務", "攝錄", "點心", "文書"]

st.title("幹部管理")
st.caption("維護幹部基本資料與職位分工，後續可加入匯入、查詢與交接紀錄。")

st.subheader("新增幹部")
col1, col2, col3 = st.columns(3)

with col1:
    st.text_input("姓名")
with col2:
    st.text_input("學號")
with col3:
    st.selectbox("職位", OFFICER_ROLES)

st.button("新增", type="primary", disabled=True)

st.subheader("幹部列表")
st.dataframe(
    [
        {"姓名": "範例幹部", "學號": "S000000", "職位": "社長", "狀態": "正常"},
    ],
    use_container_width=True,
)
