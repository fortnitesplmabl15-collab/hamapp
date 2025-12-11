import streamlit as st
import pandas as pd
import os
from datetime import datetime

# --- 設定: 画像やデータを保存する場所を作る ---
PHOTO_DIR = "photos"
DATA_FILE = "diary.csv"

# フォルダがなければ作る
if not os.path.exists(PHOTO_DIR):
    os.makedirs(PHOTO_DIR)

# データファイル(CSV)がなければ作る（項目行だけ作成）
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["日付", "内容", "画像パス"])
    df.to_csv(DATA_FILE, index=False)

# --- ここから画面を作る ---
st.title("🐹 ハムスター観察日記")

# 1. 入力フォーム
with st.container():
    st.subheader("📝 新しい日記を書く")
    
    # 日付、テキスト、画像入力
    date = st.date_input("日付", datetime.now())
    content = st.text_area("今日の様子", placeholder="例：回し車で元気に走ってた！")
    photo = st.file_uploader("写真を追加 (任意)", type=['jpg', 'png', 'jpeg'])

    if st.button("日記を保存する"):
        image_path = None
        
        # 写真がアップロードされていたら保存処理
        if photo is not None:
            # ファイル名を「日付_ファイル名」にして重複を防ぐ
            file_name = f"{date}_{photo.name}"
            save_path = os.path.join(PHOTO_DIR, file_name)
            
            # 画像を書き出す
            with open(save_path, "wb") as f:
                f.write(photo.getbuffer())
            image_path = save_path
        
        # データをCSVに追加保存
        new_data = pd.DataFrame({
            "日付": [date],
            "内容": [content],
            "画像パス": [image_path] # 画像がない場合はNoneになる
        })
        
        # 追記モードで保存
        new_data.to_csv(DATA_FILE, mode='a', header=False, index=False)
        st.success("保存しました！🐹")

# 2. 過去の日記を表示
st.divider() # 仕切り線
st.subheader("📖 過去の記録")

# CSVを読み込んで新しい順に並べ替え
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    
    # データがある場合のみ表示
    if not df.empty:
        # 新しい日付が上に来るように逆順にする
        for index, row in df[::-1].iterrows():
            with st.expander(f"{row['日付']} の日記"):
                st.write(row['内容'])
                # 画像があれば表示
                if pd.notna(row['画像パス']):
                    st.image(row['画像パス'])
    else:
        st.info("まだ日記がありません。")