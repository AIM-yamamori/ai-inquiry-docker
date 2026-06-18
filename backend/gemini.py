# OSの環境変数を扱うための標準ライブラリ
import os

# .envファイルから環境変数を読み込むライブラリ
from dotenv import load_dotenv

# Gemini APIを利用するためのライブラリ
from google import genai

# Geminiの設定（JSON形式・スキーマ指定など）で使用
from google.genai import types

# Geminiの返却データ形式を定義するために使用
from pydantic import BaseModel


# .envファイルを読み込む
# GEMINI_API_KEYなどをPythonから取得できるようにする
load_dotenv()


# Gemini APIクライアント作成
# APIキーはコードに直接書かず、.envから取得する
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# 使用するGeminiモデル名
# .envに設定があればそれを使用
# なければ gemini-2.5-flash-lite を使用
MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)


# Geminiから返してほしいデータ形式を定義
# JSONとして category / priority / answer を取得する
class InquiryResult(BaseModel):

    # 問い合わせカテゴリ
    category: str

    # 緊急度（高・中・低）
    priority: str

    # 社員への回答案
    answer: str



# 問い合わせ文をGeminiへ送り、
# カテゴリ・緊急度・回答案を取得する関数
def analyze_with_gemini(question: str) -> InquiryResult:


    # Geminiへ渡す指示文（プロンプト）
    prompt = f"""
あなたは総務部門の問い合わせ一次回答担当です。
社員からの問い合わせを読み、カテゴリ・緊急度・回答案を判定してください。

- category: 問い合わせのカテゴリ（例: 休暇、備品、給与、保険、その他）
- priority: 緊急度を「高」「中」「低」のいずれかで返す
- answer: 社員への一次回答案（日本語、2〜3文程度）

問い合わせ:
{question}
"""


    # Gemini APIへ問い合わせを送信
    response = client.models.generate_content(

        # 使用するモデル
        model=MODEL,

        # Geminiへ送る文章
        contents=prompt,


        # 返却形式の設定
        config=types.GenerateContentConfig(

            # JSON形式で返すよう指定
            response_mime_type="application/json",

            # InquiryResultの形で返すよう指定
            response_schema=InquiryResult,
        ),
    )


    # GeminiのJSON結果を
    # InquiryResultオブジェクトとして取得
    parsed = response.parsed


    # SDKバージョンによって
    # (InquiryResult(...),)
    # のようなリスト・タプル形式になる場合がある
    #
    # category属性がなければ先頭要素を取得する
    if not hasattr(parsed, 'category'):
        parsed = parsed[0]


    # category / priority / answer を持った結果を返す
    return parsed