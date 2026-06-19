# JSON形式をPythonの辞書型に変換するためのライブラリ
import json


# 環境変数を取得するためのライブラリ
#
# .envファイルからAPIキーを読み込むために使用

import os



# .envファイルを読み込むためのライブラリ

from dotenv import load_dotenv



# Gemini APIを利用するためのライブラリ

from google import genai





# =========================
# 環境設定読み込み
# =========================



# .envファイルの内容を読み込む
#
# 例:
#
# GEMINI_API_KEY=xxxxx
# GEMINI_MODEL=gemini-2.5-flash-lite

load_dotenv()







# =========================
# Geminiクライアント作成
# =========================



# Gemini APIへ接続するための設定
#
# APIキーを使って認証する

client = genai.Client(

    api_key=os.getenv(

        "GEMINI_API_KEY"

    )

)







# 使用するGeminiモデルを指定
#
# .envに設定があればそれを使用
#
# なければ
# gemini-2.5-flash-lite
# を使用

MODEL = os.getenv(

    "GEMINI_MODEL",

    "gemini-2.5-flash-lite"

)









# =========================
# Gemini分析処理
# =========================



# 問い合わせ内容をGeminiへ送り
# AI分析結果を返す関数
#
#
# 入力:
#   question
#
# 出力:
# {
#   "category":"給与",
#   "priority":"高",
#   "answer":"..."
# }

def analyze_with_gemini(

    question: str

):



    # Geminiへ送る指示文を作成
    #
    # AIに回答形式を指定することで
    # 後でJSONとして扱いやすくする

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








    # Gemini APIへリクエスト送信
    #
    # model:
    # 使用するAIモデル
    #
    # contents:
    # AIへ渡す質問内容

    response = client.models.generate_content(


        model=MODEL,


        contents=prompt


    )








    # Geminiから返ってきた文字列を取得

    text = response.text.strip()







    # =========================
    # JSON形式の整形
    # =========================


    # Geminiが以下のように返す場合がある
    #
    # ```json
    # {
    #  ...
    # }
    # ```
    #
    # このままだとjson.loadsできないため
    # 記号を削除する

    if text.startswith("```"):



        # ```json を削除

        text = text.replace(

            "```json",

            ""

        )



        # ``` を削除

        text = text.replace(

            "```",

            ""

        )



        # 前後の空白削除

        text = text.strip()







    # JSON文字列をPython辞書へ変換
    #
    # 例:
    #
    # JSON
    # {
    #  "category":"給与"
    # }
    #
    # ↓
    #
    # Python
    # {
    #  "category":"給与"
    # }

    return json.loads(text)