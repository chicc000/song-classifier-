import streamlit as st
import re
from collections import Counter

# 情緒詞庫：詞 -> 情緒
# 多字詞放前面優先判斷
emotion_phrases = {
    "強顏歡笑": "悲傷",
    "淚流滿面": "悲傷",
    "怒火中燒": "憤怒",
    "心如止水": "平靜",
    "熱淚盈眶": "愉悅",
    "心煩意亂": "煩躁"
}

# 單字或短詞情緒詞庫
emotion_words = {
    "歡笑": "愉悅",
    "淚": "悲傷",
    "怒": "憤怒",
    "心": "平靜",
    "熱": "愉悅",
    "煩": "煩躁",
    "悲": "悲傷",
    "快樂": "愉悅",
    "難過": "悲傷",
    "生氣": "憤怒",
    "寧靜": "平靜",
    "焦躁": "煩躁"
}

def classify_lyrics_emotion(lyrics):
    lyrics = lyrics.replace("\n", "")
    # 先判斷多字詞
    detected_emotions = []
    for phrase, emo in emotion_phrases.items():
        if phrase in lyrics:
            detected_emotions.append(emo)
            lyrics = lyrics.replace(phrase, "")  # 移除避免重複計算

    # 剩餘用單詞判斷
    for word, emo in emotion_words.items():
        count = lyrics.count(word)
        detected_emotions.extend([emo] * count)

    if not detected_emotions:
        return "無法判斷"

    # 統計出現最多的情緒
    emotion_count = Counter(detected_emotions)
    main_emotion = emotion_count.most_common(1)[0][0]
    return main_emotion

st.title("歌詞情緒判斷示範")

lyrics_input = st.text_area("請輸入歌詞文本")

if st.button("判斷情緒"):
    if not lyrics_input.strip():
        st.warning("請輸入歌詞後再按判斷")
    else:
        emotion = classify_lyrics_emotion(lyrics_input)
        st.success(f"判斷的主要情緒是：{emotion}")
