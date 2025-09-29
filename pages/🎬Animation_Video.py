import streamlit as st
import os
import streamlit.components.v1 as components

st.set_page_config(layout="wide")
st.title("🎮 Pollution Awareness — Game")
st.write("لعبة تفاعلية للتوعية بالتلوث. ضع ملفات اللعبة داخل `assets/game/index.html` وملفات الدعم في نفس المجلد.")

game_path = "assets/game/index.html"
if os.path.exists(game_path):
    with open(game_path, 'r', encoding='utf-8') as f:
        html = f.read()
    components.html(html, height=700, scrolling=True)
else:
    st.warning("لم أجد ملفات اللعبة المحلية داخل `assets/game/`.")
    video_path = "assets/pollution.mp4"
    if os.path.exists(video_path):
        with open(video_path, "rb") as f:
            st.video(f)
    else:
        st.info("ضع ملف `assets/game/index.html` لعرض اللعبة أو ضع `assets/pollution.mp4` لعرض فيديو بديل.")
