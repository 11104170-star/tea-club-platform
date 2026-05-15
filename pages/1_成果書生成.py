import streamlit as st

from utils.auth import require_login, logout_button


st.set_page_config(
    page_title="成果書生成 | 茶道社幹部平台",
    page_icon="🍵",
    layout="wide",
)

require_login()

with st.sidebar:
    st.success("已登入")
    logout_button()

st.title("成果書生成")
st.caption("建立活動成果書，後續可接入 Word 範本與活動資料。")

st.subheader("基本資料")
col1, col2 = st.columns(2)

with col1:
    st.text_input("活動名稱")
    st.date_input("活動日期")

with col2:
    st.text_input("負責幹部")
    st.text_input("活動地點")

st.subheader("內容草稿")
st.text_area("活動成果摘要", height=160)
st.file_uploader("上傳活動照片", type=["png", "jpg", "jpeg"], accept_multiple_files=True)

st.button("產生成果書", type="primary", disabled=True)
st.caption("此頁目前為基本 UI，文件生成功能可於後續擴充。")
