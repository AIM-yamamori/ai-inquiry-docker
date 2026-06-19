import json
import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


client = genai.Client(
    api_key=os.getenv(
        "GEMINI_API_KEY"
    )
)


MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash-lite"
)



def analyze_with_gemini(question: str):


    prompt = f"""

以下のJSON形式だけで返してください。

{{
 "category":"",
 "priority":"",
 "answer":""
}}


カテゴリ:

勤怠
休暇
給与
経費精算
社員情報変更
その他


緊急度:

高
中
低


問い合わせ:

{question}

"""


    response = client.models.generate_content(

        model=MODEL,

        contents=prompt

    )


    text = response.text.strip()



    # ```json を除去
    if text.startswith("```"):

        text = text.replace(
            "```json",
            ""
        )

        text = text.replace(
            "```",
            ""
        )

        text = text.strip()



    return json.loads(text)