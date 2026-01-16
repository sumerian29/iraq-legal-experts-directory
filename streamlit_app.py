# ===============================
# Iraq Legal Experts Directory
# Final Clean Version (Streamlit Cloud Safe)
# ===============================

import json
import os
import streamlit as st

# -------------------------------
# Page config
# -------------------------------
st.set_page_config(
    page_title="Iraq Legal Experts — Academic & Research Directory",
    page_icon="⚖️",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_PATH = os.path.join(BASE_DIR, "experts.json")
MUSIC_PATH = os.path.join(BASE_DIR, "assets", "audio", "ambient.mp3")
BG_IMAGE_PATH = os.path.join(BASE_DIR, "hammurabi_bg.jpg")

# -------------------------------
# Utilities
# -------------------------------
def load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f).get("experts", [])

def safe_list(x):
    if isinstance(x, list):
        return x
    if isinstance(x, str):
        return [x]
    return []

# -------------------------------
# Background + Watermark
# -------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #eef5ff, #fffaf0);
}
.cuneiform-watermark {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%) rotate(-45deg);
    font-size: 110px;
    color: rgba(0,0,0,0.05);
    z-index: 0;
    white-space: nowrap;
    pointer-events: none;
    user-select: none;
    font-family: "Segoe UI Symbol","Noto Sans Cuneiform",serif;
}
.block {
    background: rgba(255,255,255,0.75);
    border-radius: 18px;
    padding: 18px;
    box-shadow: 0 20px 45px rgba(0,0,0,0.08);
    backdrop-filter: blur(10px);
}
footer, header {visibility: hidden;}
</style>

<div class="cuneiform-watermark">
𒆳𒂗𒆠 𒁹𒅗𒁺𒌑 𒅗𒋗𒁺
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Header
# -------------------------------
st.markdown("""
<div class="block">
<h1>Iraq Legal Experts — Academic & Research Directory</h1>
<p>
A modern academic hub inspired by Iraq’s Mesopotamian legal heritage
(Hammurabi · Akkadian era · Cuneiform legacy).
</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------
# Music (manual play – Cloud safe)
# -------------------------------
with st.expander("🎵 Ambient Music (optional)"):
    if os.path.exists(MUSIC_PATH):
        st.audio(MUSIC_PATH)
    else:
        st.info("Music file not found. Place it at: assets/audio/ambient.mp3")

# -------------------------------
# Load experts
# -------------------------------
experts = load_data()

# -------------------------------
# Filters
# -------------------------------
st.markdown("### Filters")

search = st.text_input("Search (name, bio, expertise)").lower()

all_tags = sorted(
    {t for e in experts for t in safe_list(e.get("tags"))}
)

tag = st.selectbox("Tag", ["All"] + all_tags)

# -------------------------------
# Filtering logic (FIXED)
# -------------------------------
filtered = experts

if search:
    filtered = [
        e for e in filtered
        if search in e.get("full_name","").lower()
        or search in e.get("bio_en","").lower()
    ]

if tag != "All":
    filtered = [
        e for e in filtered
        if tag in safe_list(e.get("tags"))
    ]

# -------------------------------
# Layout
# -------------------------------
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### Experts")
    if not filtered:
        st.warning("No experts match the selected filters.")
    names = [e["full_name"] for e in filtered]
    selected = st.radio("Select an expert", names)

with col2:
    expert = next(e for e in filtered if e["full_name"] == selected)
    st.markdown(f"## {expert['full_name']}")
    st.write("**Nationality:**", expert.get("nationality","Iraqi"))
    st.write("**Location:**", expert.get("location","Iraq"))
    st.write("**Languages:**", ", ".join(safe_list(expert.get("languages"))))
    st.write("**Expertise:**", ", ".join(safe_list(expert.get("expertise"))))
    st.markdown("### Overview")
    st.write(expert.get("bio_en",""))

# -------------------------------
# Footer
# -------------------------------
st.markdown("""
<div style="text-align:center; margin-top:40px; opacity:0.7;">
Design & Development: Consultant / Senior Chief Engineer Tareq Majeed Al-Karimi
</div>
""", unsafe_allow_html=True)
