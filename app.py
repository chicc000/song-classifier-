import streamlit as st
import pandas as pd

# 載入歌曲資料，假設 songs.csv 有 title, artist, emotion, genre 欄位
@st.cache_data
def load_songs(file):
    return pd.read_csv(file)

songs = load_songs("songs.csv")

def simple_lyrics_emotion_classifier(text):
    happy_words = ["開心", "快樂", "愉悅", "幸福", "笑", "陽光", "美好", "happy", "joy", "glad"]
    sad_words = ["悲傷", "難過", "淚", "哭", "孤單", "絕望", "傷心", "sad", "cry", "tear"]
    angry_words = ["憤怒", "生氣", "怒", "恨", "爆炸", "吼", "angry", "mad", "hate"]
    calm_words = ["平靜", "安靜", "冷靜", "放鬆", "寧靜", "calm", "quiet", "relax"]
    restless_words = ["煩躁", "焦躁", "急", "慌", "不安", "restless", "anxious", "nervous"]

    text = text.lower().replace("，", "").replace("。", "").replace("！", "").replace("？", "")

    counts = {
        "愉悅": sum(text.count(w) for w in happy_words),
        "悲傷": sum(text.count(w) for w in sad_words),
        "憤怒": sum(text.count(w) for w in angry_words),
        "平靜": sum(text.count(w) for w in calm_words),
        "煩躁": sum(text.count(w) for w in restless_words)
    }

    max_emotion = max(counts, key=counts.get)
    if counts[max_emotion] == 0:
        return "無法判斷"
    return max_emotion

st.title("歌詞情緒分析與歌曲推薦")

input_lyrics = st.text_area("請輸入歌詞文本")

if st.button("分析情緒並推薦歌曲"):
    if not input_lyrics.strip():
        st.warning("請先輸入歌詞內容")
    else:
        emotion = simple_lyrics_emotion_classifier(input_lyrics)
        if emotion == "無法判斷":
            st.info("無法判斷歌曲情緒，請試著輸入更多歌詞內容或其他歌詞片段")
        else:
            st.success(f"判斷歌曲情緒為：『{emotion}』")
            filtered = songs[songs['emotion'] == emotion]
            if filtered.empty:
                st.write(f"抱歉，找不到情緒為『{emotion}』的歌曲。")
            else:
                st.write(f"推薦以下情緒為『{emotion}』的歌曲：")
                for _, row in filtered.iterrows():
                    st.write(f"- {row['title']} by {row['artist']} [{row.get('genre', '未知曲風')}]")
