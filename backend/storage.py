# JSONファイルを扱うためのライブラリ
import json

# ファイルパス操作用
from pathlib import Path

# 登録日時取得用
from datetime import datetime



# 問い合わせ履歴を保存する場所
#
# Dockerでは：
# ホスト
#   data/inquiries.json
#
# ↓ volume
#
# コンテナ
#   /app/data/inquiries.json
#
DATA_PATH = Path("data/inquiries.json")




# 保存済み問い合わせ一覧を読み込む関数
def load_inquiries():


    # JSONファイルが存在しない場合
    # 初回起動時など
    # 空の配列を返す
    if not DATA_PATH.exists():

        return []



    # JSONファイルを読み込み
    with DATA_PATH.open(
        "r",
        encoding="utf-8"
    ) as f:


        # JSON → Pythonのリストへ変換して返す
        return json.load(f)






# 新しい問い合わせを保存する関数
#
# 引数:
# question  : 問い合わせ内容
# category  : AIが判定したカテゴリ
# priority  : AIが判定した緊急度
# answer    : AIが生成した回答案
#
def save_inquiry(
    question,
    category,
    priority,
    answer
):


    # 現在保存されている問い合わせを取得
    inquiries = load_inquiries()



    # IDを発行
    #
    # 現在件数 + 1
    #
    # 例:
    # 3件保存済み
    # ↓
    # 新しいID = 4
    #
    new_id = len(inquiries) + 1




    # 保存する1件分のデータを作成
    item = {

        # 問い合わせ番号
        "id": new_id,


        # 登録日時
        "created_at":
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),


        # 入力された問い合わせ
        "question": question,


        # Gemini分類結果
        "category": category,


        # Gemini緊急度
        "priority": priority,


        # Gemini回答案
        "answer": answer
    }




    # 新しい問い合わせを追加
    inquiries.append(item)




    # 保存先フォルダがなければ作成
    #
    # data/
    #   inquiries.json
    #
    DATA_PATH.parent.mkdir(
        exist_ok=True
    )




    # JSONファイルへ書き込み
    with DATA_PATH.open(
        "w",
        encoding="utf-8"
    ) as f:


        json.dump(

            # 保存するデータ
            inquiries,

            # 日本語をそのまま保存
            ensure_ascii=False,

            # 見やすい形式で保存
            indent=2,

            fp=f
        )



    # 保存した1件分を返す
    #
    # FastAPI → Streamlitへ返される
    return item