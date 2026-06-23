# =========================
# import
# =========================


# FastAPIでAPIサーバーを作成するためのライブラリ

from fastapi import FastAPI, HTTPException



# JSONデータの形式チェック用

from pydantic import BaseModel





# Gemini分析処理を読み込む

from backend.gemini import (

    analyze_with_gemini

)




# JSON保存・読み込み処理を読み込む

from backend.storage import (

    save_inquiry,

    load_inquiries

)








# =========================
# FastAPIアプリ作成
# =========================


# このappがAPIサーバーになる

app = FastAPI()







# =========================
# 受信データ形式定義
# =========================



# Streamlitから送られてくるJSON形式


# 例:
#
# {
#   "question":"交通費について"
# }


class InquiryRequest(BaseModel):


    # 問い合わせ内容

    question: str










# =========================
# 動作確認API
# =========================



# GET /
#
# API起動確認用

@app.get("/")

def root():


    return {


        "message":

            "API is running"


    }









# =========================
# 問い合わせ分析API
# =========================



# POST /analyze
#
# 処理の流れ
#
# Streamlit
#      ↓
# FastAPI
#      ↓
# Gemini API
#      ↓
# JSON保存
#      ↓
# 結果返却


@app.post("/analyze")


def analyze_inquiry(


    request: InquiryRequest


):



    try:



        # =====================
        # ① Geminiで分析
        # =====================


        # ユーザー入力をGeminiへ送信

        ai_result = analyze_with_gemini(


            request.question


        )







        # =====================
        # ② データ保存
        # =====================



        # Gemini結果をJSONへ保存

        saved_data = save_inquiry(


            # ユーザー入力

            question=request.question,



            # カテゴリ

            # 取得できない場合はその他

            category=ai_result.get(

                "category",

                "その他"

            ),



            # 緊急度

            priority=ai_result.get(

                "priority",

                "低"

            ),



            # AI回答

            answer=ai_result.get(

                "answer",

                "回答なし"

            )

        )







        # =====================
        # ③ 結果返却
        # =====================


        # StreamlitへJSONとして返す

        return saved_data








    except Exception as e:



        # サーバーログへ表示

        print(

            "Analyze Error:",

            e

        )



        # フロント側へエラー通知

        raise HTTPException(


            status_code=500,


            detail="問い合わせ分析に失敗しました"


        )












# =========================
# 問い合わせ一覧取得API
# =========================



# GET /inquiries
#
# 保存済み問い合わせ一覧を取得


@app.get("/inquiries")


def get_inquiries():



    try:



        # JSON読み込み

        inquiries = load_inquiries()





        # =====================
        # 新しい順に並び替え
        # =====================


        # idが大きいものを先頭へ

        inquiries.sort(

            key=lambda x: x["id"],

            reverse=True

        )





        return inquiries





    except Exception as e:



        print(

            "Load Error:",

            e

        )



        raise HTTPException(


            status_code=500,


            detail="履歴取得に失敗しました"


        )













# =========================
# 問い合わせ詳細取得API
# =========================



# GET /inquiries/{id}
#
# 指定したIDの詳細取得
#
# 例:
#
# /inquiries/2


@app.get("/inquiries/{inquiry_id}")


def get_inquiry_detail(


    inquiry_id: int


):



    # 全データ取得

    inquiries = load_inquiries()






    # ID検索

    for inquiry in inquiries:



        if inquiry["id"] == inquiry_id:



            return inquiry







    # 該当なしの場合

    raise HTTPException(


        status_code=404,


        detail="問い合わせが見つかりません"


    )