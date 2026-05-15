import streamlit as st

from utils.auth import require_login, logout_button
from utils.officer_store import (
    OFFICER_ROLES,
    add_officer,
    delete_officer,
    format_officer_label,
    load_officers,
)


st.set_page_config(
    page_title="幹部管理 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

st.title("幹部管理")
st.caption("維護幹部基本資料與職位分工，成果書的活動負責人會使用這份名單。")

st.subheader("新增幹部")
with st.form("officer_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        name = st.text_input("姓名")
    with col2:
        student_id = st.text_input("學號")
    with col3:
        role = st.selectbox("職位", OFFICER_ROLES)

    submitted = st.form_submit_button("新增", type="primary")

if submitted:
    if not name.strip():
        st.error("請輸入姓名。")
    else:
        add_officer(name=name, student_id=student_id, role=role)
        st.success("已新增幹部。")
        st.rerun()

st.subheader("幹部列表")
officers = load_officers()

if officers:
    st.dataframe(officers, use_container_width=True, hide_index=True)

    delete_options = list(range(len(officers)))
    selected_index = st.selectbox(
        "選擇要刪除的幹部",
        delete_options,
        format_func=lambda index: format_officer_label(officers[index]),
    )

    if st.button("刪除幹部"):
        delete_officer(selected_index)
        st.success("已刪除幹部。")
        st.rerun()
else:
    st.info("目前尚未新增幹部。")
