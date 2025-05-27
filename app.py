import streamlit as st
import pandas as pd

# 載入歌曲資料
@st.cache_data
def load_songs(file):
    return pd.read_csv(file)

songs = load_songs("songs.csv")

st.title("歌詞情緒分析與歌曲推薦")

# 使用者輸入歌詞
lyrics = st.text_area("請輸入歌詞文本")

def simple_lyrics_emotion_classifier(text):
    # 簡易詞彙情緒判斷詞庫
    happy_words = ["開心", "快樂", "愉悅", "幸福", "笑", "陽光", "美好"]
    sad_words = ["悲傷", "難過", "淚", "哭", "孤單", "絕望", "傷心"]
    angry_words = ["憤怒", "生氣", "怒", "恨", "爆炸", "吼"]
    calm_words = ["平靜", "安靜", "冷靜", "放鬆", "寧靜"]
    restless_words = ["煩躁", "焦躁", "急", "慌", "不安"]

    text = text.replace("，", "").replace("。", "").replace("！", "").replace("？", "")
    
    counts = {
        "愉悅": sum(text.count(w) for w in happy_words),
        "悲傷": sum(text.count(w) for w in sad_words),
        "憤怒": sum(text.count(w) for w in angry_words),
        "平靜": sum(text.count(w) for w in calm_words),
        "煩躁": sum(text.count(w) for w in restless_words)
    }

    # 找出最高分情緒
    max_emotion = max(counts, key=counts.get)
    if counts[max_emotion] == 0:
        return "無法判斷"
    return max_emotion

if st.button("分析情緒並推薦歌曲"):
    if not lyrics.strip():
        st.warning("請輸入歌詞！")
    else:
        emotion = simple_lyrics_emotion_classifier(lyrics)
        st.write(f"系統判斷情緒為：**{emotion}**")

        if emotion != "無法判斷":
            filtered = songs[songs['emotion'] == emotion]
            if not filtered.empty:
                st.write(f"推薦以下情緒為『{emotion}』的歌曲：")
                for idx, row in filtered.iterrows():
                    st.write(f"- {row['title']} by {row['artist']} [{row['genre']}]")
            else:
                st.write(f"抱歉，找不到情緒為『{emotion}』的歌曲。")
