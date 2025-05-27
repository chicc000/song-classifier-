import streamlit as st
import pandas as pd

# 讀取歌曲資料
@st.cache_data
def load_songs(file):
    return pd.read_csv(file)

songs = load_songs("songs.csv")

st.title("簡易歌曲情緒推薦系統")

# 使用者輸入情緒
user_emotion = st.text_input("請輸入你想找的情緒（愉悅、悲傷、憤怒、平靜、煩躁）")

if user_emotion:
    filtered = songs[songs['emotion'] == user_emotion]
    if not filtered.empty:
        st.write(f"找到 {len(filtered)} 首情緒為『{user_emotion}』的歌曲：")
        for idx, row in filtered.iterrows():
            st.write(f"- {row['title']} by {row['artist']} [{row['genre']}]")
    else:
        st.write(f"抱歉，找不到情緒為『{user_emotion}』的歌曲。")
