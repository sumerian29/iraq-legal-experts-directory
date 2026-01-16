import streamlit as st
import json
import os

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Iraq Legal Experts — Academic & Research Directory",
    layout="wide"
)

# ---------------- PATHS ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "experts.json")
BG_IMAGE = os.path.join(BASE_DIR, "assets", "images", "hammurabi_bg.jpg")
AUDIO_PATH = os.path.join(BASE_DIR, "assets", "audio", "ambient.mp3")

# ---------------- LOAD DATA ----------------
with open(DATA_PATH, "r", encoding="utf-8") as f:
    experts = json.load(f)

# ---------------- STYLE ----------------
st.markdown(
    f"""
    <style>
    body {{
        background: #eaf4ff;
    }}
    .app-bg {{
        position: fixed;
        inset: 0;
        background-image: url("{BG_IMAGE}");
        background-size: cover;
        background-position: center;
        opacity: 0.08;
        z-index: -2;
    }}
    .cuneiform {{
        position: fixed;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 110px;
        font-weight: 800;
        color: rgba(0,0,0,0.18);
        transform: rotate(-45deg);
        z-index: -1;
        pointer-events: none;
    }}
    </style>

    <div class="app-bg"></div>
    <div class="cuneiform">
        𒆳𒆳𒀭𒀀𒁲𒀭𒋫𒀀𒀭
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------- HEADER ----------------
st.title("Iraq Legal Experts — Academic & Research Directory")
st.caption(
    "A modern academic hub inspired by Iraq’s Mesopotamian legal heritage "
    "(Hammurabi · Akkadian era · Cuneiform legacy)."
)

# ---------------- MUSIC ----------------
with st.expander("🎵 Ambient Music (optional)"):
    if os.path.exists(AUDIO_PATH):
        st.audio(AUDIO_PATH)
    else:
        st.warning("Music file not found. Place it in assets/audio/ambient.mp3")

# ---------------- FILTERS ----------------
st.subheader("Filters")

search = st.text_input("Search (name, bio, expertise)")
tags = sorted({tag for e in experts for tag in e.get("tags", [])})
selected_tag = st.selectbox("Tag", ["All"] + tags)

# ---------------- FILTER LOGIC ----------------
def match(expert):
    if search:
        text = (expert["name"] + expert.get("overview", "")).lower()
        if search.lower() not in text:
            return False
    if selected_tag != "All":
        if selected_tag not in expert.get("tags", []):
            return False
    return True

filtered = [e for e in experts if match(e)]

# ---------------- LAYOUT ----------------
col1, col2 = st.columns([1, 3])

with col1:
    st.subheader("Experts")
    for i, e in enumerate(filtered):
        if st.radio(
            "Select an expert",
            options=[x["name"] for x in filtered],
            index=0,
            key="expert_radio"
        ):
            selected = next(x for x in filtered if x["name"] == e["name"])
            break
    else:
        selected = None

with col2:
    if selected:
        st.header(selected["name"])
        st.write(f"**Nationality:** {selected['nationality']}")
        st.write(f"**Location:** {selected['location']}")
        st.write(f"**Languages:** {', '.join(selected['languages'])}")
        st.write(f"**Expertise:** {selected['expertise']}")

        tab1, tab2, tab3 = st.tabs(
            ["Overview", "Publications", "Documents"]
        )

        with tab1:
            st.write(selected.get("overview", "—"))

        with tab2:
            for p in selected.get("publications", []):
                st.markdown(f"- {p}")

        with tab3:
            if "cv" in selected:
                st.download_button(
                    "Download CV (PDF)",
                    open(os.path.join(BASE_DIR, selected["cv"]), "rb"),
                    file_name=os.path.basename(selected["cv"])
                )

    else:
        st.info("Select an expert to view details.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "Design & Development: Consultant / Senior Chief Engineer "
    "Tareq Majeed Al-Karimi"
)
