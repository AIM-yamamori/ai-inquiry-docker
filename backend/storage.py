# JSONファイルを読み書きするためのライブラリ
import json


# ファイルパスを扱いやすくするライブラリ
from pathlib import Path


# 保存日時を取得するためのライブラリ
from datetime import datetime




# 問い合わせ履歴を保存するJSONファイルの場所
#
# プロジェクト:
#
# data/
#   └ inquiries.json
#
# に保存する

DATA_PATH = Path(
    "data/inquiries.json"
)





# =========================
# 問い合わせ履歴読み込み
# =========================


def load_inquiries():


    # JSONファイルが存在しない場合
    #
    # 初回起動時など
    #
    # 空のリストを返す

    if not DATA_PATH.exists():

        return []



    # JSONファイルを開く
    #
    # encoding="utf-8"
    # 日本語を正しく扱うため

    with DATA_PATH.open(

        "r",

        encoding="utf-8"

    ) as f:



        # JSONの内容を読み込み
        #
        # JSON
        # ↓
        # Pythonのlist/dictへ変換

        return json.load(f)









# =========================
# 問い合わせ保存
# =========================


def save_inquiry(

    question,

    category,

    priority,

    answer

):


    # 既存の問い合わせ一覧を取得

    inquiries = load_inquiries()





    # 新しいIDを作成
    #
    # 例:
    #
    # 既存データ3件
    # ↓
    # 新しいID = 4

    new_id = len(inquiries) + 1






    # 保存する1件分のデータを作成
    #
    # Geminiの結果と
    # ユーザー入力をまとめる

    inquiry = {


        # 問い合わせ番号

        "id": new_id,



        # 登録日時
        #
        # 例:
        # 2026-06-19 06:46:39

        "created_at":

        datetime.now()

        .strftime(

            "%Y-%m-%d %H:%M:%S"

        ),



        # ユーザーが入力した内容

        "question": question,



        # Geminiが判定したカテゴリ

        "category": category,



        # Geminiが判定した緊急度

        "priority": priority,



        # Geminiが生成した回答

        "answer": answer

    }






    # 作成した問い合わせを
    # 一覧へ追加

    #
    # 例:
    #
    # [
    #   問い合わせ1,
    #   問い合わせ2
    # ]

    inquiries.append(

        inquiry

    )






    # 保存先フォルダを作成
    #
    # dataフォルダがない場合でも
    # 自動作成する

    DATA_PATH.parent.mkdir(

        exist_ok=True

    )






    # JSONファイルへ保存

    with DATA_PATH.open(

        "w",

        encoding="utf-8"

    ) as f:



        json.dump(


            inquiries,


            f,


            # 日本語をそのまま保存

            ensure_ascii=False,


            # 見やすい形式で保存

            indent=2

        )






    # 保存した1件分のデータを返す
    #
    # main.py側で
    #
    # return save_inquiry()
    #
    # としてAPIレスポンスに利用する

    return inquiry