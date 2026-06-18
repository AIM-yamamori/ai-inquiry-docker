import os
import streamlit as st
import requests

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)

st.title("総務問い合わせ入力")
question = st.text_area("問い合わせ内容", height=160)

if st.button("APIに送信する"):
    if question.strip() == "":
        st.error("問い合わせ内容を入力してください。")
    else:
        response = requests.post(
            f"{BACKEND_URL}/analyze",
            json={"question": question},
            timeout=30
        )
        result = response.json()
        st.write("カテゴリ:", result["category"])
        st.write("緊急度:", result["priority"])
        st.write("回答案:", result["answer"])

# 問い合わせ一覧を取得して表示する（追加部分）
st.subheader("問い合わせ一覧")
resp = requests.get(f"{BACKEND_URL}/inquiries", timeout=10)
if resp.status_code == 200:
    inquiries = resp.json()
    if inquiries:
        for item in inquiries:
            st.write(f"[{item['id']}] {item['created_at']} | {item['question'][:40]}")
    else:
        st.write("まだ問い合わせはありません。")