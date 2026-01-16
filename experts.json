import base64
import json
import os
from typing import Any, Dict, List, Optional

import streamlit as st

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="العراق - دليل الخبراء القانونيين والأكاديميين",
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


def css_bg_block(bg_path: Optional[str]) -> str:
    # الخلفية الأساسية - أزرق فاتح
    css = """
    body {
        background: linear-gradient(135deg, #e6f2ff 0%, #cce0ff 100%);
        background-attachment: fixed;
    }
    """
    
    if bg_path:
        bg_b64 = b64_from_file(bg_path)
        # صورة حمورابي بشكل عمودي على اليسار
        css += f"""
        .hammurabi-side-image {{
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 300px;
            z-index: -1;
            background-image: url("data:image/jpeg;base64,{bg_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.15;
            border-right: 2px solid rgba(0, 50, 100, 0.1);
        }}
        """
    
    return css


def inject_css(bg_path: Optional[str]) -> None:
    # جملة العلامة المائية الكبيرة
    watermark_text = "على ارضنا سن اول قانون للبشريه"
    
    st.markdown(
        f"""
        <style>
        {css_bg_block(bg_path)}
        
        /* العلامة المائية الكبيرة بزاوية 45 درجة */
        .large-arabic-watermark {{
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%) rotate(-45deg);
            z-index: -1;
            font-size: 4.5rem;
            font-weight: 900;
            color: rgba(0, 0, 0, 0.85);
            white-space: nowrap;
            opacity: 0.25;
            pointer-events: none;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
            letter-spacing: 2px;
            font-family: 'Arial', sans-serif;
        }}
        
        /* العلامة المائية السومرية الأصلية (مخفضة الحجم) */
        .cuneiform-watermark {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: -1;
            font-size: 1.8rem;
            font-weight: 700;
            color: rgba(0, 0, 0, 0.08);
            pointer-events: none;
            user-select: none;
        }}
        
        /* تحسين المساحة الرئيسية */
        .main-content {{
            margin-left: 320px;
            padding-right: 20px;
        }}
        
        /* تعديل الـ hero ليناسب التصميم الجديد */
        .hero {{
            background: rgba(255, 255, 255, 0.85);
            border-left: 4px solid #0066cc;
            border-radius: 0 16px 16px 0;
            margin-left: -20px !important;
            padding-left: 30px;
        }}
        
        /* تعديل الـ panels */
        .panel {{
            background: rgba(255, 255, 255, 0.9);
            border-left: 3px solid rgba(0, 102, 204, 0.3);
        }}
        
        /* تكييف المحتوى مع المساحة الجديدة */
        .stApp > div:first-child {{
            margin-left: 320px;
        }}
        
        /* إخفاء العلامة المائية القديمة */
        .cuneiform-watermark:first-of-type {{
            display: none;
        }}
        
        /* تحسينات عامة */
        .stApp {{
            color: #0f172a;
        }}
        
        /* Header card */
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
            margin-bottom: 8px;
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
        header[data-testid="stHeader"] {{
            background: transparent;
        }}
        
        /* Responsive adjustments */
        @media (max-width: 768px) {{
            .hammurabi-side-image {{
                display: none;
            }}
            .main-content {{
                margin-left: 20px;
            }}
            .large-arabic-watermark {{
                font-size: 2.5rem;
            }}
            .stApp > div:first-child {{
                margin-left: 20px;
            }}
        }}
        </style>
        
        <div class="hammurabi-side-image"></div>
        <div class="large-arabic-watermark">{watermark_text}</div>
        <div class="cuneiform-watermark">𒆳𒀭𒈾𒆠 𒁉𒌑𒋗𒁀 𒅆𒁺𒉌 𒅗𒋛𒈠</div>
        """,
        unsafe_allow_html=True,
    )


def header_block(music_on: bool, bg_found: bool) -> None:
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(
            """
            <div class="hero">
              <h1>🇮🇶 العراق - دليل الخبراء القانونيين والأكاديميين</h1>
              <p>منصة حديثة تستلهم إرث بلاد الرافدين العريق (حمورابي · العصر الأكادي · التراث المسماري)</p>
              <div style="margin-top:15px;">
                <span class="chip">⚖️ الدراسات القانونية</span>
                <span class="chip">📚 الأبحاث والدراسات</span>
                <span class="chip">🏛️ إرث حمورابي</span>
                <span class="chip">𒀭 الكتابة المسمارية</span>
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    with col2:
        st.markdown(
            """
            <div style="text-align: right; padding: 15px; background: rgba(255,255,255,0.8); 
                        border-radius: 10px; border-right: 4px solid #0066cc;">
                <h4 style="margin:0; color:#0066cc;">⚖️</h4>
                <p style="margin:5px 0; font-size:12px; color:#333;">
                أرض القانون الأول<br>للبشرية
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    
    # سطر الحالة
    st.markdown("---")
    col1, col2, col3 = st.columns([1.2, 1.2, 2.6])
    with col1:
        st.caption(f"صورة الخلفية: {'موجودة ✅' if bg_found else 'غير موجودة (يتم استخدام الخلفية الزرقاء)'}")
    with col2:
        st.caption(f"الموسيقى: {'مفعلة ✅' if music_on else 'غير مفعلة'}")
    with col3:
        st.caption("الخصوصية: تجنب نشر معلومات التواصل الشخصية إلا إذا كانت متاحة رسمياً وبإذن.")


def audio_block(music_path: Optional[str]) -> bool:
    st.session_state.setdefault("music_on", False)

    c1, c2, c3 = st.columns([0.8, 0.8, 3.0])
    with c1:
        if st.button("🔊 تشغيل/إيقاف الموسيقى", use_container_width=True):
            st.session_state.music_on = not st.session_state.music_on
    with c2:
        st.write("")

    if not music_path:
        st.warning("لم يتم العثور على ملف الموسيقى. المتوقع: assets/audio/ambient.mp3 (مستحسن).")
        st.caption("نصيحة: قم بإنشاء مجلد assets/audio/ ووضع ملف ambient.mp3 بداخله.")
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
        with st.expander("مشغل الصوت (احتياطي)", expanded=False):
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
# قراءة البيانات أولاً
data = safe_read_json(DATA_PATH)
experts_raw = data.get("experts", [])
experts = [normalize_expert(e) for e in experts_raw]

# العثور على الملفات
music_path = file_first_existing(MUSIC_CANDIDATES)
bg_path = file_first_existing(BG_CANDIDATES)
bg_found = bg_path is not None

# حقن CSS مع تمرير مسار الخلفية
inject_css(bg_path)

# تشغيل الموسيقى
music_on = audio_block(music_path)

# رأس الصفحة
header_block(music_on, bg_found)

# الفلاتر
with st.expander("الفلاتر", expanded=True):
    f1, f2, f3 = st.columns([1.4, 1.2, 1.2])
    with f1:
        q = st.text_input("بحث (الاسم، السيرة، الخبرة، الوسوم)", "")
    all_tags = sorted({t for e in experts for t in (e.get("tags") or [])})
    all_areas = sorted({a for e in experts for a in (e.get("expertise") or [])})
    with f2:
        tag = st.selectbox("الوسوم", ["الكل"] + all_tags, index=0)
    with f3:
        area = st.selectbox("مجال الخبرة", ["الكل"] + all_areas, index=0)

filtered = filter_experts(experts, q, tag, area)

# المحتوى الرئيسي
st.markdown('<div class="main-content">', unsafe_allow_html=True)

left, right = st.columns([1.1, 2.4], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">الخبراء</div>', unsafe_allow_html=True)
    st.caption(f"عرض {len(filtered)} من أصل {len(experts)}")

    if not filtered:
        st.info("لا يوجد خبراء يطابقون الفلاتر المحددة.")
        selected_id = None
    else:
        options = [(e.get("id", e.get("full_name")), e.get("display_name", e.get("full_name"))) for e in filtered]
        # Build a radio label list
        labels = [lbl for _, lbl in options]
        ids = [i for i, _ in options]
        st.session_state.setdefault("selected_idx", 0)
        if st.session_state.selected_idx >= len(labels):
            st.session_state.selected_idx = 0
        selected_label = st.radio("اختر خبير", labels, index=st.session_state.selected_idx)
        selected_id = ids[labels.index(selected_label)]
        st.session_state.selected_idx = labels.index(selected_label)

    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)

    if not selected_id:
        st.markdown('<div class="section-title">الملف الشخصي</div>', unsafe_allow_html=True)
        st.write("يرجى اختيار خبير لعرض التفاصيل.")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        expert = next((e for e in experts if (e.get("id") == selected_id or e.get("full_name") == selected_id)), None)
        if not expert:
            st.error("الخبير المحدد غير موجود.")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-title">{expert.get("display_name","")}</div>', unsafe_allow_html=True)

            # Key facts row
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("الجنسية")
                st.write(expert.get("nationality", "—"))
            with c2:
                st.caption("الموقع")
                st.write(expert.get("location", "—"))
            with c3:
                st.caption("اللغات")
                st.write(", ".join(expert.get("languages") or []) or "—")

            exp = expert.get("expertise") or []
            if exp:
                st.caption("مجالات الخبرة")
                st.write(", ".join(exp))

            tabs = st.tabs(["نظرة عامة", "السيرة والمساهمات", "المنشورات", "الوثائق"])

            with tabs[0]:
                bio = expert.get("bio_en") or "ملف أكاديمي - يرجى إضافة التفاصيل والمنشورات الموثقة."
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
                    st.info("لا توجد وثائق مرفقة لهذا الملف.")
                else:
                    # Show the first PDF as preview (if available) + download buttons
                    for d in docs:
                        if isinstance(d, dict):
                            dtitle = d.get("title", "وثيقة")
                            dfile = d.get("file", "")
                            dtype = d.get("type", "pdf")
                        else:
                            dtitle = "وثيقة"
                            dfile = str(d)
                            dtype = "pdf"

                        resolved = resolve_doc_path(dfile)
                        st.subheader(dtitle)

                        if not resolved:
                            st.error(f"الملف غير موجود: {dfile}")
                            st.caption("نصيحة: ضع ملفات PDF في مجلد assets/docs/ (مستحسن).")
                            continue

                        # Download button
                        with open(resolved, "rb") as f:
                            st.download_button(
                                label=f"تحميل ({os.path.basename(resolved)})",
                                data=f.read(),
                                file_name=os.path.basename(resolved),
                                mime="application/pdf" if dtype.lower() == "pdf" else "application/octet-stream",
                            )

                        # Preview
                        if dtype.lower() == "pdf":
                            pdf_iframe_viewer(resolved, height=760)

            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # إغلاق main-content

st.markdown(
    """
    <div class="footer">
      التصميم والتطوير: المستشار / كبير المهندسين طارق مجيد الكريمي
    </div>
    """,
    unsafe_allow_html=True,
)
