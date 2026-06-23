# =========================
# import
# =========================


# JSON文字列をPython辞書へ変換するため
import json


# 環境変数取得用
import os



# .env読み込み用

from dotenv import load_dotenv



# Gemini API利用ライブラリ

from google import genai





# =========================
# 環境設定読み込み
# =========================



# .envファイルを読み込む
#
# 例:
#
# GEMINI_API_KEY=xxxx
# GEMINI_MODEL=gemini-2.5-flash-lite

load_dotenv()






# =========================
# Geminiクライアント作成
# =========================



# APIキー取得

API_KEY = os.getenv(

    "GEMINI_API_KEY"

)





# APIキーが存在しない場合

if not API_KEY:


    raise ValueError(

        "GEMINI_API_KEYが設定されていません"

    )






# Gemini APIへ接続するクライアント作成

client = genai.Client(

    api_key=API_KEY

)







# 使用するモデル取得

MODEL = os.getenv(

    "GEMINI_MODEL",

    "gemini-2.5-flash-lite"

)









# =========================
# Gemini分析処理
# =========================



def analyze_with_gemini(

    question: str

):


    """
    問い合わせ内容をGeminiで分析する

    入力:
        question
        例:
        "交通費について"


    出力:

    {
        "category":"経費精算",
        "priority":"中",
        "answer":"回答内容"
    }

    """







    # =========================
    # Geminiへ渡すプロンプト作成
    # =========================


    prompt = f"""


あなたは社内問い合わせ対応AIです。


必ずJSON形式だけで返してください。


形式:

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



問い合わせ内容:

{question}

"""









    try:



        # =========================
        # Gemini API呼び出し
        # =========================


        response = client.models.generate_content(


            model=MODEL,


            contents=prompt


        )






        # Gemini回答取得

        text = response.text.strip()






        # =========================
        # JSON整形
        # =========================


        # Geminiが

        #
        # ```json
        # {}
        # ```
        #
        # の形式で返した場合
        # 記号を削除する


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







        # =========================
        # JSON → Python辞書
        # =========================


        result = json.loads(text)








        # =========================
        # 必須項目確認
        # =========================


        # キーが存在しない場合の対策

        return {


            "category":

                result.get(

                    "category",

                    "その他"

                ),



            "priority":

                result.get(

                    "priority",

                    "中"

                ),



            "answer":

                result.get(

                    "answer",

                    "回答を作成できませんでした"

                )

        }








    # Gemini APIエラー

    except Exception as e:



        print(

            "Gemini Error:",

            e

        )



        # FastAPI側で500にしないため
        # エラー内容をJSONで返す

        return {


            "category":

                "その他",



            "priority":

                "低",



            "answer":

                "AI回答生成中にエラーが発生しました"

        }