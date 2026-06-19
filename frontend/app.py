# OSの環境変数を読み込むために使用
import os


# Streamlit : 画面を作るライブラリ
# requests  : FastAPIへHTTP通信するためのライブラリ
import streamlit as st
import requests



# =========================
# FastAPIのURL設定
# =========================

# Docker環境では
# http://backend:8000
#
# ローカル実行では
# http://127.0.0.1:8000
#
# を使用する
#
# docker-compose.yml の
# BACKEND_URLを取得する

BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
)



# 画面タイトル表示
st.title(
    "総務問い合わせAI"
)



# 説明文表示
st.write(
    "問い合わせ内容を入力してください。"
)



# =========================
# 問い合わせ入力画面
# =========================


# 複数行入力できる入力欄を作成
question = st.text_area(
    "問い合わせ内容",
    height=160
)



# ボタンが押された時だけ処理する
if st.button("分析する"):


    # 入力チェック
    #
    # 空文字の場合はAIに送信しない
    if question.strip() == "":


        st.error(
            "問い合わせ内容を入力してください"
        )


        # ここで処理終了
        st.stop()



    try:


        # FastAPIへ問い合わせ内容を送信
        #
        # POST /analyze
        #
        # 送信データ:
        # {
        #   "question":"入力内容"
        # }

        response = requests.post(

            f"{BACKEND_URL}/analyze",

            json={

                "question": question

            },

            timeout=60

        )



        # FastAPI側でエラーが発生した場合
        #
        # 例:
        # 500 Internal Server Error

        if response.status_code != 200:


            st.error(
                "APIエラー"
            )


            # backendから返ってきた内容表示
            st.write(
                response.text
            )


            st.stop()



        # FastAPIから返ってきたJSONをPython辞書へ変換
        #
        # 例:
        #
        # {
        #  "category":"給与",
        #  "priority":"高",
        #  "answer":"..."
        # }

        result = response.json()



        st.success(
            "分析完了"
        )



        # =====================
        # AI結果表示
        # =====================


        st.subheader(
            "AI回答"
        )



        st.write(
            "カテゴリ:",
            result["category"]
        )



        st.write(
            "緊急度:",
            result["priority"]
        )



        st.write(
            "回答案:"
        )



        st.write(
            result["answer"]
        )



    # ネットワークエラー処理
    #
    # backendが起動していない場合など

    except requests.exceptions.RequestException as e:


        st.error(
            "バックエンドに接続できません"
        )


        st.write(e)



    # JSON変換失敗時
    #
    # FastAPIからJSON以外が返った場合

    except ValueError:


        st.error(
            "APIからJSONが返されませんでした"
        )





# =========================
# 問い合わせ履歴表示
# =========================


st.subheader(
    "問い合わせ履歴"
)



try:


    # FastAPIから保存済みデータ取得
    #
    # GET /inquiries

    response = requests.get(

        f"{BACKEND_URL}/inquiries",

        timeout=10

    )



    # API取得失敗

    if response.status_code != 200:


        st.error(
            "履歴取得エラー"
        )


        st.write(
            response.text
        )



    else:


        # JSONをPython形式へ変換

        inquiries = response.json()



        # データが存在しない場合

        if len(inquiries) == 0:


            st.write(
                "履歴はありません"
            )



        else:



            # 保存されている問い合わせを
            # 1件ずつ表示

            for item in inquiries:



                # 折りたたみ表示
                #
                # クリックすると詳細表示

                with st.expander(

                    f"{item['id']} : {item['question']}"

                ):



                    st.write(

                        "日時:",

                        item["created_at"]

                    )



                    st.write(

                        "カテゴリ:",

                        item["category"]

                    )



                    st.write(

                        "緊急度:",

                        item["priority"]

                    )



                    st.write(

                        "回答:",

                        item["answer"]

                    )



# 履歴取得時の通信エラー

except requests.exceptions.RequestException as e:


    st.error(
        "履歴取得でバックエンド接続失敗"
    )


    st.write(e)