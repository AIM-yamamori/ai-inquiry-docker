# =========================
# import
# =========================


# JSONファイル操作用

import json



# ファイルパス操作用

from pathlib import Path



# 日時取得用

from datetime import datetime









# =========================
# 保存場所設定
# =========================



# 保存するJSONファイル

#
# プロジェクト構成:
#
# data
#  └ inquiries.json
#

DATA_PATH = Path(

    "data/inquiries.json"

)









# =========================
# 問い合わせ履歴読み込み
# =========================


def load_inquiries():


    # ファイルが存在しない場合

    if not DATA_PATH.exists():


        return []







    try:



        # JSONファイルを開く

        with DATA_PATH.open(


            "r",


            encoding="utf-8"


        ) as f:



            # ファイル内容を確認

            data = f.read()





            # 空ファイルの場合

            if data == "":


                return []







            # JSON文字列
            #
            # ↓
            #
            # Python listへ変換

            return json.loads(data)






    except json.JSONDecodeError:



        # JSONが壊れている場合

        print(

            "JSONファイル読み込みエラー"

        )


        return []











# =========================
# JSON保存処理
# =========================


def save_json(data):



    # 保存フォルダ作成

    DATA_PATH.parent.mkdir(


        exist_ok=True

    )






    # JSON書き込み

    with DATA_PATH.open(


        "w",


        encoding="utf-8"


    ) as f:



        json.dump(


            data,


            f,



            # 日本語保存

            ensure_ascii=False,



            # 見やすく整形

            indent=2


        )









# =========================
# 問い合わせ保存
# =========================


def save_inquiry(


    question,


    category,


    priority,


    answer


):



    # 既存履歴取得

    inquiries = load_inquiries()








    # =====================
    # ID作成
    # =====================


    if len(inquiries) == 0:


        new_id = 1



    else:


        # 最大ID + 1

        new_id = max(


            item["id"]

            for item in inquiries


        ) + 1










    # 保存するデータ作成

    inquiry = {



        # 問い合わせID

        "id": new_id,





        # 作成日時

        "created_at":


            datetime.now()

            .strftime(

                "%Y-%m-%d %H:%M:%S"

            ),






        # 質問内容

        "question": question,





        # AI分類結果

        "category": category,





        # AI緊急度

        "priority": priority,





        # AI回答

        "answer": answer

    }











    # 一覧へ追加

    inquiries.append(


        inquiry


    )








    # JSON保存

    save_json(


        inquiries


    )







    # 保存したデータ返却

    return inquiry