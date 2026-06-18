import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-lite")


class InquiryResult(BaseModel):
    category: str
    priority: str
    answer: str


def analyze_with_gemini(question: str) -> InquiryResult:
    prompt = f"""
あなたは総務部門の問い合わせ一次回答担当です。
社員からの問い合わせを読み、カテゴリ・緊急度・回答案を判定してください。

- category: 問い合わせのカテゴリ（例: 休暇、備品、給与、保険、その他）
- priority: 緊急度を「高」「中」「低」のいずれかで返す
- answer: 社員への一次回答案（日本語、2〜3文程度）

問い合わせ:
{question}
"""
    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=InquiryResult,
        ),
    )
    parsed = response.parsed
    # SDKのバージョンによってリスト/タプルで返ることがある。
    # isinstance ではなく属性の有無で判定する（カスタム型にも対応）
    if not hasattr(parsed, 'category'):
        parsed = parsed[0]
    return parsed