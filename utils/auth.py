import streamlit as st


def init_auth_state() -> None:
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False


def logout_button() -> None:
    if st.button("登出"):
        st.session_state["authenticated"] = False
        st.rerun()


def require_login() -> None:
    init_auth_state()

    if not st.session_state["authenticated"]:
        st.warning("請先回到首頁登入。")
        st.stop()
