# 環境変数を取得するための標準ライブラリ
import os

# 画面作成用ライブラリ
import streamlit as st

# FastAPIへHTTP通信するためのライブラリ
import requests



# バックエンドAPIのURLを取得
#
# Docker環境:
#   http://backend:8000
#
# ローカル実行:
#   http://127.0.0.1:8000
#
# 環境変数がない場合はローカルURLを使用
BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)




# 画面タイトル表示
st.title("総務問い合わせ入力")



# 問い合わせ入力欄
#
# height=160
# → 入力欄の高さ指定
question = st.text_area(
    "問い合わせ内容",
    height=160
)




# ボタン押下時の処理
if st.button("APIに送信する"):


    # 空文字チェック
    if question.strip() == "":

        # エラー表示
        st.error(
            "問い合わせ内容を入力してください。"
        )


    else:


        # FastAPIへ問い合わせを送信
        #
        # POST /analyze
        #
        # 送信データ:
        # {
        #   "question": "問い合わせ内容"
        # }
        response = requests.post(

            # backend URL
            f"{BACKEND_URL}/analyze",

            # JSON形式で送信
            json={
                "question": question
            },

            # タイムアウト30秒
            timeout=30
        )



        # FastAPIから返ってきたJSONを取得
        result = response.json()



        # Gemini分析結果を表示
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





# 問い合わせ履歴一覧表示
st.subheader(
    "問い合わせ一覧"
)



# FastAPIから過去データ取得
#
# GET /inquiries
#
resp = requests.get(

    f"{BACKEND_URL}/inquiries",

    timeout=10
)




# 正常取得できた場合
if resp.status_code == 200:


    # JSON → Pythonデータへ変換
    inquiries = resp.json()



    # データが存在する場合
    if inquiries:


        # 1件ずつ表示
        for item in inquiries:


            st.write(

                # 表示例:
                # [1] 2026-06-18 10:00:00 | 健康保険証...
                f"[{item['id']}] "
                f"{item['created_at']} | "
                f"{item['question'][:40]}"
            )



    # データがない場合
    else:

        st.write(
            "まだ問い合わせはありません。"
        )