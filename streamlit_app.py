import base64
import json
import os
from typing import Any, Dict, List, Optional, Tuple

import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Iraq Legal Experts | Directory",
    page_icon="⚖️",
    layout="wide",
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "experts.json")

# Assets (keep compatibility with old folders if they exist)
MUSIC_CANDIDATES = [
    os.path.join(APP_DIR, "assets", "audio", "ambient.mp3"),
    os.path.join(APP_DIR, "assets", "audio", "Music.mp3"),
    os.path.join(APP_DIR, "Music.mp3"),
    os.path.join(APP_DIR, "music.mp3"),
]
DOCS_CANDIDATE_DIRS = [
    os.path.join(APP_DIR, "assets", "docs"),
    os.path.join(APP_DIR, "assets", "pdf"),
    os.path.join(APP_DIR, "assets"),
    APP_DIR,
]
BG_CANDIDATES = [
    os.path.join(APP_DIR, "assets", "images", "hammurabi_bg.jpg"),
    os.path.join(APP_DIR, "assets", "images", "background.jpg"),
    os.path.join(APP_DIR, "hammurabi_bg.jpg"),
    os.path.join(APP_DIR, "background.jpg"),
]


# =========================
# HELPERS
# =========================
def file_first_existing(candidates: List[str]) -> Optional[str]:
    for p in candidates:
        if p and os.path.exists(p):
            return p
    return None


def safe_read_json(path: str) -> Dict[str, Any]:
    if not os.path.exists(path):
        return {"experts": []}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def b64_from_file(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def resolve_doc_path(doc_path: str) -> Optional[str]:
    # Accept absolute
    if doc_path and os.path.isabs(doc_path) and os.path.exists(doc_path):
        return doc_path

    # Try relative to app dir
    if doc_path:
        p0 = os.path.join(APP_DIR, doc_path)
        if os.path.exists(p0):
            return p0

    # Try docs candidate dirs
    base = os.path.basename(doc_path) if doc_path else ""
    for d in DOCS_CANDIDATE_DIRS:
        p = os.path.join(d, base)
        if base and os.path.exists(p):
            return p
    return None


def normalize_expert(e: Dict[str, Any]) -> Dict[str, Any]:
    # Backward compatibility with older schema keys
    title_en = e.get("title_en") or e.get("title") or ""
    full_name = e.get("full_name") or e.get("name") or "Unknown"
    display = e.get("display_name") or full_name

    # If title not included in display, prepend
    if title_en and not display.lower().startswith(title_en.lower()):
        display = f"{title_en} {display}".strip()

    e_out = dict(e)
    e_out["full_name"] = full_name
    e_out["display_name"] = display
    e_out["title_en"] = title_en

    # Fill commonly used fields
    e_out.setdefault("nationality", e.get("nationality", "Iraqi"))
    e_out.setdefault("location", e.get("location", "Iraq"))
    e_out.setdefault("languages", e.get("languages", ["Arabic"]))
    e_out.setdefault("tags", e.get("tags", []))
    e_out.setdefault("expertise", e.get("expertise", e.get("areas_of_expertise", [])))
    e_out.setdefault("bio_en", e.get("bio_en", e.get("bio", "")))
    e_out.setdefault("publications", e.get("publications", []))
    e_out.setdefault("documents", e.get("documents", []))
    return e_out


def css_bg_block() -> str:
    bg_path = file_first_existing(BG_CANDIDATES)
    if bg_path:
        bg_b64 = b64_from_file(bg_path)
        return f"""
        body {{
            background:
              radial-gradient(1200px 600px at 10% 0%, rgba(59,130,246,0.18), transparent 60%),
              radial-gradient(900px 500px at 90% 10%, rgba(245,158,11,0.14), transparent 55%),
              linear-gradient(135deg, rgba(240,248,255,1) 0%, rgba(255,251,235,1) 55%, rgba(236,254,255,1) 100%);
            background-attachment: fixed;
        }}
        .app-bg-image {{
            position: fixed;
            inset: 0;
            z-index: -2;
            background-image: url("data:image/jpeg;base64,{bg_b64}");
            background-size: cover;
            background-position: center;
            opacity: 0.16;
            filter: saturate(0.9) contrast(1.05);
        }}
        """
    # fallback (no image)
    return """
    body {
        background:
          radial-gradient(1200px 600px at 10% 0%, rgba(59,130,246,0.20), transparent 60%),
          radial-gradient(900px 500px at 90% 10%, rgba(245,158,11,0.16), transparent 55%),
          linear-gradient(135deg, rgba(240,248,255,1) 0%, rgba(255,251,235,1) 55%, rgba(236,254,255,1) 100%);
        background-attachment: fixed;
    }
    """


def inject_css() -> None:
    # Cuneiform watermark (decorative). Large, transparent, rotated 45°.
    # NOTE: This is used as a stylized Sumerian/cuneiform statement watermark.
    cuneiform_watermark = "𒆳𒀭𒈾𒆠 𒁉𒌑𒋗𒁀 𒅆𒁺𒉌 𒅗𒋛𒈠"
    st.markdown(
        f"""
        <style>
        {css_bg_block()}

        /* Layer for optional bg image */
        .app-bg-image {{ pointer-events:none; }}

        /* Make Streamlit containers transparent-ish */
        .stApp {{
            color: #0f172a;
        }}

        /* Header card */
        .hero {{
            background: rgba(255,255,255,0.78);
            border: 1px solid rgba(15,23,42,0.08);
            box-shadow: 0 18px 45px rgba(15,23,42,0.10);
            border-radius: 18px;
            padding: 18px 20px;
            margin: 8px 0 14px 0;
            backdrop-filter: blur(10px);
        }}

        .hero h1 {{
            margin: 0;
            font-size: 28px;
            letter-spacing: -0.4px;
            color: #0f172a;
        }}

        .hero p {{
            margin: 6px 0 0 0;
            color: rgba(15,23,42,0.70);
            font-size: 13px;
        }}

        /* Chips */
        .chip {{
            display:inline-flex;
            gap:8px;
            align-items:center;
            padding: 6px 10px;
            border-radius: 999px;
            border: 1px solid rgba(15,23,42,0.10);
            background: rgba(255,255,255,0.60);
            box-shadow: 0 6px 18px rgba(15,23,42,0.06);
            font-size: 12px;
            color: #0f172a;
            margin-right: 8px;
        }}

        /* Panels */
        .panel {{
            background: rgba(255,255,255,0.72);
            border: 1px solid rgba(15,23,42,0.08);
            border-radius: 16px;
            padding: 16px;
            box-shadow: 0 12px 35px rgba(15,23,42,0.08);
            backdrop-filter: blur(10px);
        }}

        /* Make section titles clear */
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #0f172a;
            margin: 4px 0 10px 0;
        }}

        /* Watermark */
        .cuneiform-watermark {{
            position: fixed;
            inset: -10%;
            z-index: -1;
            display: flex;
            align-items: center;
            justify-content: center;
            pointer-events: none;
            transform: rotate(-45deg);
            font-size: clamp(42px, 6vw, 92px);
            font-weight: 700;
            color: rgba(15,23,42,0.08);
            letter-spacing: 6px;
            text-align: center;
            line-height: 1.2;
            user-select: none;
            filter: blur(0.2px);
        }}

        /* Footer */
        .footer {{
            margin-top: 20px;
            padding: 14px 6px 6px 6px;
            color: rgba(15,23,42,0.55);
            font-size: 12px;
            text-align: center;
        }}

        /* Streamlit label contrast */
        label, .stMarkdown, .stText, .stCaption {{
            color: #0f172a !important;
        }}

        /* Remove extra top white gap (if any) */
        header[data-testid=\"stHeader\"] {{
            background: transparent;
        }}
        </style>

        <div class="app-bg-image"></div>
        <div class="cuneiform-watermark">{cuneiform_watermark}</div>
        """,
        unsafe_allow_html=True,
    )


def header_block(music_on: bool, bg_found: bool) -> None:
    st.markdown(
        """
        <div class="hero">
          <h1>Iraq Legal Experts — Academic & Research Directory</h1>
          <p>A modern hub inspired by Iraq’s Mesopotamian legacy (Hammurabi · Akkadian era · Cuneiform heritage).</p>
          <div style="margin-top:10px;">
            <span class="chip">⚖️ Legal Scholarship</span>
            <span class="chip">📚 Research & Studies</span>
            <span class="chip">🏛️ Hammurabi Legacy</span>
            <span class="chip">𒀭 Cuneiform</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Small status line (optional)
    col1, col2, col3 = st.columns([1.2, 1.2, 2.6])
    with col1:
        st.caption(f"Background image: {'Found ✅' if bg_found else 'Not found (using light-blue fallback)'}")
    with col2:
        st.caption(f"Music: {'ON ✅' if music_on else 'OFF'}")
    with col3:
        st.caption("Privacy: avoid publishing personal contact details unless officially public & permitted.")


def audio_block(music_path: Optional[str]) -> bool:
    st.session_state.setdefault("music_on", False)

    c1, c2, c3 = st.columns([0.8, 0.8, 3.0])
    with c1:
        if st.button("🔊 Toggle Music", use_container_width=True):
            st.session_state.music_on = not st.session_state.music_on
    with c2:
        st.write("")

    if not music_path:
        st.warning("Music file not found. Expected one of: assets/audio/ambient.mp3 (recommended).")
        st.caption("Tip: create folder assets/audio/ and put ambient.mp3 inside it.")
        st.session_state.music_on = False
        return False

    # Try autoplay (only after user gesture toggle). Some browsers may still block autoplay.
    if st.session_state.music_on:
        b64 = b64_from_file(music_path)
        st.components.v1.html(
            f"""
            <audio autoplay loop>
              <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            </audio>
            """,
            height=0,
        )
        # Also show a small fallback player (in case autoplay is blocked)
        with st.expander("Audio player (fallback)", expanded=False):
            st.audio(open(music_path, "rb").read(), format="audio/mp3")

    return bool(st.session_state.music_on)


def filter_experts(experts: List[Dict[str, Any]], q: str, tag: str, area: str) -> List[Dict[str, Any]]:
    ql = (q or "").strip().lower()
    out = []
    for e in experts:
        hay = " ".join(
            [
                e.get("display_name", ""),
                e.get("full_name", ""),
                e.get("bio_en", ""),
                " ".join(e.get("tags", []) or []),
                " ".join(e.get("expertise", []) or []),
            ]
        ).lower()
        if ql and ql not in hay:
            continue
        if tag != "All" and tag not in (e.get("tags") or []):
            continue
        if area != "All" and area not in (e.get("expertise") or []):
            continue
        out.append(e)
    return out


def pdf_iframe_viewer(pdf_path: str, height: int = 720) -> None:
    # Render PDF in an iframe using base64 to avoid pdf.js errors
    pdf_b64 = b64_from_file(pdf_path)
    st.markdown(
        f"""
        <iframe
            src="data:application/pdf;base64,{pdf_b64}"
            width="100%"
            height="{height}"
            style="border: 1px solid rgba(15,23,42,0.10); border-radius: 14px; background: rgba(255,255,255,0.60);"
        ></iframe>
        """,
        unsafe_allow_html=True,
    )


# =========================
# APP
# =========================
inject_css()

data = safe_read_json(DATA_PATH)
experts_raw = data.get("experts", [])
experts = [normalize_expert(e) for e in experts_raw]

music_path = file_first_existing(MUSIC_CANDIDATES)
bg_found = file_first_existing(BG_CANDIDATES) is not None

music_on = audio_block(music_path)
header_block(music_on, bg_found)

# Filters (top)
with st.expander("Filters", expanded=True):
    f1, f2, f3 = st.columns([1.4, 1.2, 1.2])
    with f1:
        q = st.text_input("Search (name, bio, expertise, tags)", "")
    all_tags = sorted({t for e in experts for t in (e.get("tags") or [])})
    all_areas = sorted({a for e in experts for a in (e.get("expertise") or [])})
    with f2:
        tag = st.selectbox("Tags", ["All"] + all_tags, index=0)
    with f3:
        area = st.selectbox("Expertise", ["All"] + all_areas, index=0)

filtered = filter_experts(experts, q, tag, area)

left, right = st.columns([1.1, 2.4], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Experts</div>', unsafe_allow_html=True)
    st.caption(f"Showing {len(filtered)} of {len(experts)}")

    if not filtered:
        st.info("No experts match the selected filters.")
        selected_id = None
    else:
        options = [(e.get("id", e.get("full_name")), e.get("display_name", e.get("full_name"))) for e in filtered]
        # Build a radio label list
        labels = [lbl for _, lbl in options]
        ids = [i for i, _ in options]
        st.session_state.setdefault("selected_idx", 0)
        if st.session_state.selected_idx >= len(labels):
            st.session_state.selected_idx = 0
        selected_label = st.radio("Select an expert", labels, index=st.session_state.selected_idx)
        selected_id = ids[labels.index(selected_label)]
        st.session_state.selected_idx = labels.index(selected_label)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if not selected_id:
        st.markdown('<div class="section-title">Profile</div>', unsafe_allow_html=True)
        st.write("Select an expert to view details.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        expert = next((e for e in experts if (e.get("id") == selected_id or e.get("full_name") == selected_id)), None)
        if not expert:
            st.error("Selected expert not found.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-title">{expert.get("display_name","")}</div>', unsafe_allow_html=True)

            # Key facts row
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("Nationality")
                st.write(expert.get("nationality", "—"))
            with c2:
                st.caption("Location")
                st.write(expert.get("location", "—"))
            with c3:
                st.caption("Languages")
                st.write(", ".join(expert.get("languages") or []) or "—")

            exp = expert.get("expertise") or []
            if exp:
                st.caption("Areas of expertise")
                st.write(", ".join(exp))

            tabs = st.tabs(["Overview", "Bio & Contributions", "Publications", "Documents"])

            with tabs[0]:
                bio = expert.get("bio_en") or "Academic profile placeholder — add verified details and publications."
                st.write(bio)

            with tabs[1]:
                contrib = expert.get("contributions") or []
                if isinstance(contrib, list) and contrib:
                    for item in contrib:
                        st.write(f"• {item}")
                else:
                    st.write("—")

            with tabs[2]:
                pubs = expert.get("publications") or []
                if pubs:
                    for p in pubs:
                        title = p.get("title") if isinstance(p, dict) else str(p)
                        year = p.get("year") if isinstance(p, dict) else None
                        venue = p.get("venue") if isinstance(p, dict) else None
                        line = f"• {title}"
                        meta = " — ".join([x for x in [str(year) if year else "", venue or ""] if x])
                        if meta.strip():
                            line += f" ({meta})"
                        st.write(line)
                else:
                    st.write("—")

            with tabs[3]:
                docs = expert.get("documents") or []
                if not docs:
                    st.info("No documents attached for this profile.")
                else:
                    # Show the first PDF as preview (if available) + download buttons
                    for d in docs:
                        if isinstance(d, dict):
                            dtitle = d.get("title", "Document")
                            dfile = d.get("file", "")
                            dtype = d.get("type", "pdf")
                        else:
                            dtitle = "Document"
                            dfile = str(d)
                            dtype = "pdf"

                        resolved = resolve_doc_path(dfile)
                        st.subheader(dtitle)

                        if not resolved:
                            st.error(f"File not found: {dfile}")
                            st.caption("Tip: Put PDFs into assets/docs/ (recommended).")
                            continue

                        # Download button
                        with open(resolved, "rb") as f:
                            st.download_button(
                                label=f"Download ({os.path.basename(resolved)})",
                                data=f.read(),
                                file_name=os.path.basename(resolved),
                                mime="application/pdf" if dtype.lower() == "pdf" else "application/octet-stream",
                            )

                        # Preview
                        if dtype.lower() == "pdf":
                            pdf_iframe_viewer(resolved, height=760)

            st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    """
    <div class="footer">
      Design & Development: Consultant / Senior Chief Engineer Tareq Majeed Al-Karimi
    </div>
    """,
    unsafe_allow_html=True,
)
