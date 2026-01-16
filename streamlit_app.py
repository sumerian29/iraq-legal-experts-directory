import streamlit as st
import json
import os

# --------------------------------------------------
# Basic config
# --------------------------------------------------
st.set_page_config(
    page_title="Iraq Legal Experts — Academic & Research Directory",
    layout="wide",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, "experts.json")
AUDIO_FILE = os.path.join(BASE_DIR, "assets", "audio", "ambient.mp3")

# --------------------------------------------------
# Load data
# --------------------------------------------------
with open(DATA_FILE, "r", encoding="utf-8") as f:
    experts = json.load(f)

# --------------------------------------------------
# Global CSS (background + cuneiform watermark)
# --------------------------------------------------
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(
            135deg,
            #eaf4ff 0%,
            #f7fbff 50%,
            #ffffff 100%
        );
    }

    .cuneiform-bg {
        position: fixed;
        top: 20%;
        left: -10%;
        font-size: 180px;
        color: rgba(0,0,0,0.12);
        transform: rotate(-45deg);
        z-index: 0;
        pointer-events: none;
        font-family: "Segoe UI Symbol", "Noto Sans Cuneiform", serif;
        white-space: nowrap;
    }

    .content-wrapper {
        position: relative;
        z-index: 1;
    }
    </style>

    <div class="cuneiform-bg">
        𒆠𒂗𒆤 𒀀𒈾 𒄿𒈾 𒁀𒀭 𒀸
    </div>
    """,
    unsafe_allow_html=True
)

# --------------------------------------------------
# Header
# --------------------------------------------------
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

st.title("Iraq Legal Experts — Academic & Research Directory")
st.markdown(
    "A modern academic hub inspired by Iraq’s Mesopotamian legal heritage "
    "(Hammurabi · Akkadian era · Cuneiform legacy)."
)

# --------------------------------------------------
# Ambient music (safe)
# --------------------------------------------------
with st.expander("🎵 Ambient Music (optional)", expanded=False):
    if os.path.exists(AUDIO_FILE):
        st.audio(AUDIO_FILE, loop=True)
    else:
        st.warning("Music file not found. Place it in: assets/audio/ambient.mp3")

# --------------------------------------------------
# Filters (no auto-filtering)
# --------------------------------------------------
st.subheader("Filters")

search_text = st.text_input("Search (name, bio, expertise)", "")
selected_tag = st.selectbox("Tag", ["All"])
# (Tag system reserved for future expansion)

# --------------------------------------------------
# Filter logic (safe)
# --------------------------------------------------
def match_expert(expert):
    if search_text.strip():
        blob = (
            expert.get("name", "") +
            expert.get("overview", "") +
            " ".join(expert.get("expertise", []))
        ).lower()
        if search_text.lower() not in blob:
            return False
    return True

filtered_experts = [e for e in experts if match_expert(e)]

# --------------------------------------------------
# Layout
# --------------------------------------------------
col_left, col_right = st.columns([1, 2])

# --------------------------------------------------
# Experts list
# --------------------------------------------------
with col_left:
    st.subheader("Experts")
    if not filtered_experts:
        st.info("No experts match the current filters.")
    else:
        names = [e["name"] for e in filtered_experts]
        selected_name = st.radio(
            "Select an expert",
            names,
            index=0
        )
        selected = next(e for e in filtered_experts if e["name"] == selected_name)

# --------------------------------------------------
# Profile view
# --------------------------------------------------
with col_right:
    if filtered_experts:
        st.subheader(selected["name"])

        st.markdown(f"**Nationality:** {selected.get('nationality', '—')}")
        st.markdown(f"**Location:** {selected.get('location', '—')}")
        st.markdown(f"**Languages:** {', '.join(selected.get('languages', [])) or '—'}")
        st.markdown(
            f"**Expertise:** {', '.join(selected.get('expertise', [])) or '—'}"
        )

        tabs = st.tabs(["Overview", "Publications", "Documents"])

        # Overview
        with tabs[0]:
            st.write(selected.get("overview", "No overview available."))

        # Publications (placeholder)
        with tabs[1]:
            st.info("Publications will be added in future updates.")

        # Documents (CV)
        with tabs[2]:
            cv = selected.get("cv")
            if cv:
                cv_path = os.path.join(BASE_DIR, cv)
                if os.path.exists(cv_path):
                    with open(cv_path, "rb") as f:
                        st.download_button(
                            "Download CV (PDF)",
                            f,
                            file_name=os.path.basename(cv_path),
                            mime="application/pdf"
                        )
                else:
                    st.warning("CV file referenced but not found in repository.")
            else:
                st.info("No documents available for this expert.")

# --------------------------------------------------
# Footer
# --------------------------------------------------
st.markdown("---")
st.caption(
    "Design & Development: Consultant / Senior Chief Engineer "
    "Tareq Majeed Al-Karimi"
)

st.markdown("</div>", unsafe_allow_html=True)
