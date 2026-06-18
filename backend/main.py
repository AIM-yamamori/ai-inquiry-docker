# FastAPIアプリ作成用
from fastapi import FastAPI

# リクエストデータの型定義用
from pydantic import BaseModel


# 問い合わせデータ保存・読み込み処理
from backend.storage import save_inquiry, load_inquiries

# Gemini分析処理
from backend.gemini import analyze_with_gemini



# FastAPIアプリを作成
# このappがAPIサーバーの入口になる
app = FastAPI()



# フロントエンドから受け取る
# 問い合わせデータの形式を定義
class InquiryRequest(BaseModel):

    # 問い合わせ本文
    question: str




# 動作確認用API
# http://localhost:8000/
# にアクセスすると実行される
@app.get("/")
def root():

    return {
        "message": "API is running"
    }




# 問い合わせ分析API
#
# 流れ:
#
# Streamlit
#    |
#    ↓
# FastAPI (/analyze)
#    |
#    ↓
# Gemini分析
#    |
#    ↓
# JSON保存
#    |
#    ↓
# 結果返却
#
@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):


    # 受け取った問い合わせ文を
    # Geminiへ送って分析する
    result = analyze_with_gemini(
        request.question
    )



    # Geminiの結果をJSONファイルへ保存
    #
    # 保存内容:
    # - 問い合わせ内容
    # - カテゴリ
    # - 緊急度
    # - 回答案
    #
    item = save_inquiry(

        # 元の問い合わせ
        question=request.question,

        # Gemini判定結果
        category=result.category,

        # 緊急度
        priority=result.priority,

        # AI回答案
        answer=result.answer
    )



    # 保存したデータを
    # フロントエンドへ返す
    return item




# 問い合わせ一覧取得API
#
# Streamlitが過去データを見るために使用
#
# GET /inquiries
#
@app.get("/inquiries")
def get_inquiries():


    # JSONファイルから
    # 保存済み問い合わせ一覧を取得
    return load_inquiries()