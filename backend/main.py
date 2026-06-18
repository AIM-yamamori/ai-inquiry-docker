from fastapi import FastAPI
from pydantic import BaseModel

from backend.storage import save_inquiry, load_inquiries
from backend.gemini import analyze_with_gemini


app = FastAPI()


class InquiryRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "message": "API is running"
    }


@app.post("/analyze")
def analyze_inquiry(request: InquiryRequest):

    # Geminiへ問い合わせ
    result = analyze_with_gemini(
        request.question
    )

    # JSON保存
    item = save_inquiry(
        question=request.question,
        category=result.category,
        priority=result.priority,
        answer=result.answer
    )

    return item


@app.get("/inquiries")
def get_inquiries():

    return load_inquiries()