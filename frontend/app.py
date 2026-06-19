import os
import streamlit as st
import requests

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.title("総務問い合わせ入力")

st.write(
    "社員から総務への問い合わせを入力してください。"
)


question = st.text_area(
    "問い合わせ内容",
    height=160
)


if st.button("APIに送信する"):

    if question.strip() == "":
        st.error(
            "問い合わせ内容を入力してください。"
        )

    else:

        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={
                "question": question
            },
            timeout=30
        )

        #st.write(response.status_code)
        #st.write(response.text)
        result = response.json()


        st.subheader("AI回答")

        st.write(
            "カテゴリ:",
            result["category"]
        )

        st.write(
            "緊急度:",
            result["priority"]
        )

        st.write(
            "回答案:",
            result["answer"]
        )



# 履歴一覧表示
st.subheader(
    "問い合わせ一覧"
)


response = requests.get(
    f"{BACKEND_URL}/inquiries",
    timeout=10
)


if response.status_code == 200:

    inquiries = response.json()


    if inquiries:

        for item in inquiries:

            st.write(
                f"[{item['id']}] "
                f"{item['created_at']} | "
                f"{item['question'][:40]}"
            )

    else:

        st.write(
            "まだ問い合わせはありません。"
        )

else:
    
    st.error(
        response.text
    )
    
    st.stop()