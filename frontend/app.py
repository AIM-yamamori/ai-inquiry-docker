# =========================
# import
# =========================

# OSの環境変数を取得するために使用
import os


# Streamlit : 画面作成
# requests  : FastAPIへHTTP通信

import streamlit as st
import requests





# =========================
# FastAPI URL設定
# =========================


# Docker環境:
# http://backend:8000
#
# ローカル:
# http://127.0.0.1:8000
#
# docker-compose.ymlの
# BACKEND_URLを取得する

BACKEND_URL = os.getenv(

    "BACKEND_URL",

    "http://127.0.0.1:8000"

)







# =========================
# 画面タブ作成
# =========================


# 画面を2つに分ける
#
# tab1:
# 問い合わせ入力・AI分析
#
# tab2:
# 過去の問い合わせ履歴

tab1, tab2 = st.tabs(

    [

        "問い合わせ",

        "問い合わせ履歴"

    ]

)









# ==================================================
# タブ1
# 問い合わせ入力・AI分析
# ==================================================


with tab1:



    # タイトル表示

    st.title(

        "総務問い合わせAI"

    )



    # 説明表示

    st.write(

        "問い合わせ内容を入力してください。"

    )







    # =========================
    # 問い合わせ入力
    # =========================


    # 複数行入力できるテキスト欄

    question = st.text_area(

        "問い合わせ内容",

        height=160

    )







    # ボタン押下時にAI分析開始

    if st.button(

        "問い合わせる"

    ):




        # =========================
        # 入力チェック
        # =========================


        # 空文字の場合は処理しない

        if question.strip() == "":



            st.error(

                "問い合わせ内容を入力してください"

            )


            st.stop()






        try:



            # =========================
            # FastAPIへ送信
            # =========================


            # POST /analyze
            #
            # 送信:
            #
            # {
            #   "question":"質問内容"
            # }

            response = requests.post(


                f"{BACKEND_URL}/analyze",


                json={

                    "question": question

                },


                timeout=60


            )







            # =========================
            # APIエラー確認
            # =========================


            if response.status_code != 200:



                st.error(

                    "APIエラー"

                )


                st.write(

                    response.text

                )


                st.stop()







            # =========================
            # JSON取得
            # =========================


            # FastAPIから返ったJSONを
            # Python辞書へ変換

            result = response.json()







            st.success(

                "分析完了"

            )







            # =========================
            # AI結果表示
            # =========================


            st.subheader(

                "AI回答"

            )





            # get()を使用することで
            # キーがない場合でもエラー防止

            st.write(

                "カテゴリ:",

                result.get(

                    "category",

                    "未分類"

                )

            )



            st.write(

                "緊急度:",

                result.get(

                    "priority",

                    "未設定"

                )

            )



            st.write(

                "回答案:"

            )



            st.write(

                result.get(

                    "answer",

                    "回答なし"

                )

            )








        # FastAPIへ接続できない場合

        except requests.exceptions.RequestException as e:



            st.error(

                "バックエンドに接続できません"

            )


            st.write(e)







        # JSON変換失敗

        except ValueError:



            st.error(

                "JSON取得失敗"

            )









# ==================================================
# タブ2
# 問い合わせ履歴
# ==================================================


with tab2:



    st.subheader(

        "問い合わせ履歴"

    )





    # 履歴更新ボタン

    if st.button(

        "履歴更新"

    ):


        st.rerun()






    try:



        # =========================
        # 履歴取得
        # =========================


        # GET /inquiries
        #
        # 保存済み問い合わせ一覧取得

        response = requests.get(


            f"{BACKEND_URL}/inquiries",


            timeout=10


        )







        # APIエラー

        if response.status_code != 200:



            st.error(

                "履歴取得エラー"

            )


            st.write(

                response.text

            )







        else:



            # JSONへ変換

            inquiries = response.json()







            # 履歴がない場合

            if len(inquiries) == 0:



                st.write(

                    "履歴はありません"

                )








            else:



                # =========================
                # 新しい順で表示
                # =========================


                # reversedで逆順表示

                for item in reversed(inquiries):






                    # 折りたたみ表示

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







    # 通信エラー

    except requests.exceptions.RequestException as e:



        st.error(

            "履歴取得でバックエンド接続失敗"

        )


        st.write(e)