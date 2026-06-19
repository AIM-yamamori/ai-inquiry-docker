# FastAPIでAPIサーバーを作るためのライブラリ
from fastapi import FastAPI



# リクエストデータの型チェックをするためのライブラリ
from pydantic import BaseModel



# Gemini分析処理を読み込む
#
# gemini.py
#     ↓
# analyze_with_gemini()
#
# を使用する

from backend.gemini import (

    analyze_with_gemini

)



# JSON保存処理を読み込む
#
# storage.py
#     ↓
# save_inquiry()
# load_inquiries()
#
# を使用する

from backend.storage import (

    save_inquiry,

    load_inquiries

)






# FastAPIアプリを作成
#
# このappがAPIサーバーになる

app = FastAPI()







# =========================
# リクエストデータ定義
# =========================


# フロントエンドから送られてくる
# JSON形式を定義する
#
# 例:
#
# {
#   "question":"交通費について"
# }

class InquiryRequest(BaseModel):


    # 問い合わせ内容
    # 文字列で受け取る

    question: str







# =========================
# 動作確認API
# =========================



# GET /
#
# ブラウザで
#
# http://localhost:8000/
#
# にアクセスした時に実行

@app.get("/")
def root():


    return {


        # APIが起動している確認用

        "message": "API is running"

    }








# =========================
# 問い合わせ分析API
# =========================



# POST /analyze
#
# frontendから問い合わせ内容を受け取り
# Geminiで分析する

@app.post("/analyze")
def analyze_inquiry(


    # 受け取ったJSONを
    # InquiryRequest型として扱う

    request: InquiryRequest

):



    # =====================
    # ① Gemini分析
    # =====================


    # ユーザーの質問をGeminiへ送信
    #
    # 返り値例:
    #
    # {
    #   "category":"経費精算",
    #   "priority":"中",
    #   "answer":"..."
    # }

    ai_result = analyze_with_gemini(

        request.question

    )







    # =====================
    # ② JSON保存
    # =====================



    # Geminiの結果を
    # inquiries.jsonへ保存

    saved_data = save_inquiry(


        # ユーザー入力

        question=request.question,



        # AIが判断したカテゴリ

        category=ai_result["category"],



        # AIが判断した緊急度

        priority=ai_result["priority"],



        # AIが作成した回答

        answer=ai_result["answer"]

    )








    # =====================
    # ③ 結果返却
    # =====================


    # 保存したデータを
    # frontendへ返す
    #
    # Streamlit側では
    #
    # response.json()
    #
    # で受け取る

    return saved_data







# =========================
# 問い合わせ一覧取得API
# =========================




# GET /inquiries
#
# 保存されている
# 問い合わせ履歴を取得する

@app.get("/inquiries")
def get_inquiries():



    # storage.pyの
    #
    # load_inquiries()
    #
    # を実行して
    # JSONデータを返す

    return load_inquiries()