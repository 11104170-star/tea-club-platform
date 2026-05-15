import streamlit as st

from utils.achievement_report import DEFAULT_TEMPLATE_PATH, build_report
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
st.caption("匯入問卷資料與活動照片，產生 Word 成果書。")

with st.expander("範本設定", expanded=False):
    st.write(f"目前預設範本：`{DEFAULT_TEMPLATE_PATH.name}`")
    template_file = st.file_uploader(
        "上傳自訂 Word 範本（可選）",
        type=["docx"],
        help="未上傳時會使用平台內建的成果書範本。",
    )

st.subheader("基本資料")
col1, col2, col3 = st.columns(3)

with col1:
    fill_date = st.date_input("填寫日期")
    activity_name = st.text_input("活動名稱")
    activity_place = st.text_input("活動地點")

with col2:
    activity_date = st.text_input("活動日期")
    activity_people = st.text_input("參加人數")
    activity_leader = st.text_input("活動負責人")

with col3:
    phone = st.text_input("連絡電話")

st.subheader("成果內容")
activity_review = st.text_area("活動檢討", height=140)
teacher_comment = st.text_area("指導老師評語", height=120)

st.subheader("問卷資料")
questionnaire_file = st.file_uploader(
    "上傳問卷 Excel / CSV",
    type=["xlsx", "csv"],
)

st.subheader("照片")
image_col1, image_col2 = st.columns(2)

with image_col1:
    flow_photo = st.file_uploader("活動流程照片", type=["jpg", "jpeg", "png"])
    photo1 = st.file_uploader("照片 1", type=["jpg", "jpeg", "png"])
    photo1_desc = st.text_input("照片 1 說明")

with image_col2:
    group_photo = st.file_uploader("大合照", type=["jpg", "jpeg", "png"])
    photo2 = st.file_uploader("照片 2", type=["jpg", "jpeg", "png"])
    photo2_desc = st.text_input("照片 2 說明")

photo3 = st.file_uploader("照片 3", type=["jpg", "jpeg", "png"])
photo3_desc = st.text_input("照片 3 說明")

fields = {
    "fill_date": fill_date.strftime("%Y-%m-%d"),
    "activity_name": activity_name,
    "activity_place": activity_place,
    "activity_date": activity_date,
    "activity_people": activity_people,
    "activity_leader": activity_leader,
    "phone": phone,
    "activity_review": activity_review,
    "teacher_comment": teacher_comment,
    "photo1_desc": photo1_desc,
    "photo2_desc": photo2_desc,
    "photo3_desc": photo3_desc,
}

images = {
    "flow_photo": flow_photo,
    "group_photo": group_photo,
    "photo1": photo1,
    "photo2": photo2,
    "photo3": photo3,
}

if st.button("產生成果書", type="primary"):
    try:
        output, result_text = build_report(
            template_file=template_file,
            questionnaire_file=questionnaire_file,
            fields=fields,
            images=images,
        )
    except Exception as exc:
        st.error("成果書產生失敗，請確認範本、問卷或圖片格式是否正確。")
        st.exception(exc)
    else:
        file_name = f"{activity_name or '活動'}_成果書.docx"
        st.success("成果書已產生。")

        with st.expander("問卷分析結果預覽", expanded=False):
            st.text(result_text)

        st.download_button(
            label="下載成果書",
            data=output,
            file_name=file_name,
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        )
