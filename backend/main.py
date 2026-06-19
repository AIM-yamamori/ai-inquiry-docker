from fastapi import FastAPI

from pydantic import BaseModel

from backend.gemini import (
    analyze_with_gemini
)

from backend.storage import (
    save_inquiry,
    load_inquiries
)



app = FastAPI()



# リクエスト形式
class InquiryRequest(BaseModel):

    question: str




# 動作確認用
@app.get("/")
def root():

    return {
        "message": "API is running"
    }





# 問い合わせ分析
@app.post("/analyze")
def analyze_inquiry(
    request: InquiryRequest
):


    # Geminiで分析
    ai_result = analyze_with_gemini(
        request.question
    )



    # JSON保存
    saved_data = save_inquiry(

            question=request.question,

            category=ai_result["category"],

            priority=ai_result["priority"],

            answer=ai_result["answer"]

    )



    # 保存した内容を返す
    return saved_data





# 問い合わせ一覧取得
@app.get("/inquiries")
def get_inquiries():


    return load_inquiries()