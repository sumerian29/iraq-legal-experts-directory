import streamlit as st
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------- Page config ----------
st.set_page_config(
    page_title="Iraq Legal Experts — Academic & Research Directory",
    layout="wide"
)

# ---------- Styles ----------
st.markdown("""
<style>
body {
    background-color: #eef5ff;
}
.cuneiform {
    position: fixed;
    top: 20%;
    right: 3%;
    font-size: 70px;
    color: rgba(0,0,0,0.25);
    z-index: 0;
    user-select: none;
}
.hammurabi {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    opacity: 0.15;
    z-index: 0;
}
.content {
    position: relative;
    z-index: 1;
}
</style>
""", unsafe_allow_html=True)

# ---------- Background elements ----------
st.markdown(
    "<img src='assets/hammurabi_bg.jpg' class='hammurabi'>",
    unsafe_allow_html=True
)

st.markdown(
    "<div class='cuneiform'>𒁹𒀭𒈗𒆠𒂗𒆷𒀀𒈠𒊏</div>",
    unsafe_allow_html=True
)

# ---------- Load data ----------
with open(os.path.join(BASE_DIR, "experts.json"), encoding="utf-8") as f:
    data = json.load(f)["experts"]

# ---------- Header ----------
st.markdown("<div class='content'>", unsafe_allow_html=True)
st.title("Iraq Legal Experts — Academic & Research Directory")
st.caption("Inspired by Mesopotamian legal heritage (Hammurabi · Akkadian era · Cuneiform legacy)")

# ---------- Music ----------
audio_path = os.path.join(BASE_DIR, "assets/audio/ambient.mp3")
if os.path.exists(audio_path):
    st.audio(audio_path)
else:
    st.info("🎵 Ambient music optional — file not found.")

# ---------- Experts list ----------
st.subheader("Experts")

names = [e["full_name"] for e in data]
selected_name = st.radio("Select an expert", names)

selected = next(e for e in data if e["full_name"] == selected_name)

st.markdown("### Profile")
st.write(f"**Nationality:** {selected.get('nationality','—')}")
st.write(f"**Location:** {selected.get('location','—')}")
st.write(f"**Languages:** {', '.join(selected.get('languages', []))}")
st.write(f"**Expertise:** {', '.join(selected.get('expertise', []))}")

st.markdown("#### Overview")
st.write(selected.get("bio", "Biography will be added."))

st.markdown("#### Documents")
docs = selected.get("documents", [])
if docs:
    for d in docs:
        path = os.path.join(BASE_DIR, d["file"])
        if os.path.exists(path):
            with open(path, "rb") as f:
                st.download_button(d["title"], f, file_name=os.path.basename(path))
        else:
            st.warning(f"{d['title']} not available yet.")
else:
    st.info("No documents available.")

st.markdown("---")
st.caption("Design & Development: Consultant / Senior Chief Engineer Tareq Majeed Al-Karimi")
st.markdown("</div>", unsafe_allow_html=True)
