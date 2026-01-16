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

# Assets
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
    if doc_path and os.path.isabs(doc_path) and os.path.exists(doc_path):
        return doc_path

    if doc_path:
        p0 = os.path.join(APP_DIR, doc_path)
        if os.path.exists(p0):
            return p0

    base = os.path.basename(doc_path) if doc_path else ""
    for d in DOCS_CANDIDATE_DIRS:
        p = os.path.join(d, base)
        if base and os.path.exists(p):
            return p
    return None


def normalize_expert(e: Dict[str, Any]) -> Dict[str, Any]:
    title_en = e.get("title_en") or e.get("title") or ""
    full_name = e.get("full_name") or e.get("name") or "غير معروف"
    display = e.get("display_name") or full_name

    if title_en and not display.lower().startswith(title_en.lower()):
        display = f"{title_en} {display}".strip()

    e_out = dict(e)
    e_out["full_name"] = full_name
    e_out["display_name"] = display
    e_out["title_en"] = title_en

    e_out.setdefault("nationality", e.get("nationality", "عراقي"))
    e_out.setdefault("location", e.get("location", "العراق"))
    e_out.setdefault("languages", e.get("languages", ["العربية"]))
    e_out.setdefault("tags", e.get("tags", []))
    e_out.setdefault("expertise", e.get("expertise", e.get("areas_of_expertise", [])))
    e_out.setdefault("bio_en", e.get("bio_en", e.get("bio", "")))
    e_out.setdefault("publications", e.get("publications", []))
    e_out.setdefault("documents", e.get("documents", []))
    return e_out


def css_bg_block() -> str:
    bg_path = file_first_existing(BG_CANDIDATES)
    
    css = """
    body {
        background: linear-gradient(135deg, #e6f7ff 0%, #cce7ff 50%, #b3d9ff 100%);
        background-attachment: fixed;
        margin: 0;
        padding: 0;
        min-height: 100vh;
    }
    """
    
    if bg_path:
        bg_b64 = b64_from_file(bg_path)
        css += f"""
        .hammurabi-vertical-side {{
            position: fixed;
            left: 0;
            top: 0;
            bottom: 0;
            width: 280px;
            z-index: -1;
            background-image: url("data:image/jpeg;base64,{bg_b64}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            opacity: 0.18;
            border-right: 3px solid rgba(0, 80, 150, 0.15);
            box-shadow: 5px 0 15px rgba(0, 0, 0, 0.1);
        }}
        """
    
    return css


def inject_css() -> None:
    watermark_text = "على ارضنا سن اول قانون للبشريه"
    
    st.markdown(
        f"""
        <style>
        {css_bg_block()}
        
        /* العلامة المائية الكبيرة */
        .large-arabic-watermark {{
            position: fixed;
            top: 50%;
            left: calc(50% + 140px);
            transform: translate(-50%, -50%) rotate(-45deg);
            z-index: -1;
            font-size: 4.8rem;
            font-weight: 900;
            color: rgba(0, 0, 0, 0.92);
            white-space: nowrap;
            opacity: 0.22;
            pointer-events: none;
            text-shadow: 3px 3px 6px rgba(255, 255, 255, 0.8);
            letter-spacing: 3px;
            font-family: 'Arial', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            width: 200%;
            text-align: center;
        }}
        
        /* العلامة المائية السومرية */
        .cuneiform-watermark {{
            position: fixed;
            bottom: 25px;
            right: 25px;
            z-index: -1;
            font-size: 2rem;
            font-weight: 700;
            color: rgba(0, 0, 0, 0.10);
            pointer-events: none;
            user-select: none;
            opacity: 0.5;
        }}
        
        /* المحتوى الرئيسي */
        .main-content-container {{
            margin-left: 300px;
            padding: 20px 40px 20px 20px;
            min-height: 100vh;
        }}
        
        /* الـ header الرئيسي */
        .main-hero {{
            background: rgba(255, 255, 255, 0.92);
            border-radius: 0 20px 20px 0;
            padding: 25px 30px;
            margin: 10px 0 25px -20px;
            border-left: 6px solid #0066cc;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
            backdrop-filter: blur(10px);
        }}
        
        .main-hero h1 {{
            margin: 0 0 10px 0;
            font-size: 2.1rem;
            color: #003366;
            font-weight: 700;
            line-height: 1.3;
        }}
        
        .main-hero p {{
            margin: 0;
            color: #444;
            font-size: 1.05rem;
            line-height: 1.5;
        }}
        
        /* Chips */
        .chip {{
            display: inline-flex;
            align-items: center;
            padding: 8px 14px;
            border-radius: 25px;
            border: 1px solid rgba(0, 102, 204, 0.3);
            background: rgba(255, 255, 255, 0.85);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            font-size: 0.9rem;
            color: #0066cc;
            margin-right: 10px;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        
        /* Panels */
        .panel {{
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid rgba(0, 102, 204, 0.15);
            border-radius: 18px;
            padding: 22px;
            box-shadow: 0 10px 35px rgba(0, 0, 0, 0.06);
            backdrop-filter: blur(8px);
            margin-bottom: 20px;
        }}
        
        .section-title {{
            font-size: 1.4rem;
            font-weight: 700;
            color: #003366;
            margin: 0 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid rgba(0, 102, 204, 0.2);
        }}
        
        /* Footer */
        .footer {{
            margin-top: 40px;
            padding: 20px;
            color: rgba(0, 51, 102, 0.6);
            font-size: 0.9rem;
            text-align: center;
            background: rgba(255, 255, 255, 0.7);
            border-radius: 15px;
            border-top: 1px solid rgba(0, 102, 204, 0.1);
        }}
        
        /* Streamlit adjustments */
        .stApp {{
            background: transparent;
        }}
        
        header[data-testid="stHeader"] {{
            background: transparent;
        }}
        
        /* تحسينات للعربية */
        .arabic-text {{
            font-family: 'Arial', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            direction: rtl;
            text-align: right;
        }}
        
        /* Responsive design */
        @media (max-width: 1024px) {{
            .hammurabi-vertical-side {{
                width: 200px;
                opacity: 0.12;
            }}
            .main-content-container {{
                margin-left: 220px;
                padding: 15px;
            }}
            .large-arabic-watermark {{
                font-size: 3.5rem;
                left: calc(50% + 110px);
            }}
        }}
        
        @media (max-width: 768px) {{
            .hammurabi-vertical-side {{
                display: none;
            }}
            .main-content-container {{
                margin-left: 0;
                padding: 15px;
            }}
            .large-arabic-watermark {{
                font-size: 2.5rem;
                left: 50%;
                opacity: 0.15;
            }}
            .main-hero {{
                margin-left: 0;
                border-radius: 20px;
            }}
        }}
        
        /* زر الموسيقى */
        .music-button {{
            background: linear-gradient(135deg, #0066cc, #004d99);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }}
        
        .music-button:hover {{
            background: linear-gradient(135deg, #004d99, #003366);
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 102, 204, 0.3);
        }}
        </style>
        
        <div class="hammurabi-vertical-side"></div>
        <div class="large-arabic-watermark">{watermark_text}</div>
        <div class="cuneiform-watermark">𒆳𒀭𒈾𒆠 𒁉𒌑𒋗𒁀 𒅆𒁺𒉌 𒅗𒋛𒈠</div>
        """,
        unsafe_allow_html=True,
    )


def header_block(music_on: bool, bg_found: bool) -> None:
    st.markdown(
        """
        <div class="main-hero">
            <h1>🇮🇶 العراق - دليل الخبراء القانونيين والأكاديميين</h1>
            <p>منصة وطنية تستلهم إرث بلاد الرافدين العريق (شريعة حمورابي · العصر الأكادي · تراث الكتابة المسمارية)</p>
            <div style="margin-top: 20px;">
                <span class="chip">⚖️ الدراسات القانونية</span>
                <span class="chip">📚 الأبحاث العلمية</span>
                <span class="chip">🏛️ إرث حمورابي</span>
                <span class="chip">𒀭 الكتابة المسمارية</span>
                <span class="chip">🌍 القانون الدولي</span>
                <span class="chip">🧑‍⚖️ الخبراء العراقيون</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    
    # معلومات الحالة
    col1, col2, col3 = st.columns([1.2, 1.2, 2])
    with col1:
        st.caption(f"📷 صورة الخلفية: {'موجودة ✅' if bg_found else 'غير موجودة'}")
    with col2:
        st.caption(f"🎵 الموسيقى: {'مفعلة ✅' if music_on else 'غير مفعلة'}")
    with col3:
        st.caption("🔒 الخصوصية: المعلومات المنشورة معتمدة رسمياً")


def audio_block(music_path: Optional[str]) -> bool:
    st.session_state.setdefault("music_on", False)
    
    col1, col2 = st.columns([1, 4])
    with col1:
        button_text = "🔇 إيقاف الموسيقى" if st.session_state.music_on else "🔊 تشغيل الموسيقى"
        if st.button(button_text, use_container_width=True, type="primary"):
            st.session_state.music_on = not st.session_state.music_on
    
    if not music_path:
        st.session_state.music_on = False
        return False
    
    if st.session_state.music_on:
        b64 = b64_from_file(music_path)
        st.components.v1.html(
            f"""
            <audio autoplay loop style="display: none;">
                <source src="data:audio/mpeg;base64,{b64}" type="audio/mpeg">
            </audio>
            """,
            height=0,
        )
        
        with st.expander("🎵 مشغل الموسيقى", expanded=False):
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
        if tag != "الكل" and tag not in (e.get("tags") or []):
            continue
        if area != "الكل" and area not in (e.get("expertise") or []):
            continue
        out.append(e)
    return out


def pdf_iframe_viewer(pdf_path: str, height: int = 720) -> None:
    pdf_b64 = b64_from_file(pdf_path)
    st.markdown(
        f"""
        <iframe
            src="data:application/pdf;base64,{pdf_b64}"
            width="100%"
            height="{height}"
            style="border: 1px solid rgba(0,102,204,0.2); border-radius: 12px; background: white;"
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

st.markdown('<div class="main-content-container">', unsafe_allow_html=True)

music_on = audio_block(music_path)
header_block(music_on, bg_found)

# الفلاتر
with st.expander("🔍 فلاتر البحث", expanded=True):
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    with col1:
        q = st.text_input("بحث (الاسم، السيرة، الخبرة، الوسوم)", "")
    all_tags = sorted({t for e in experts for t in (e.get("tags") or [])})
    all_areas = sorted({a for e in experts for a in (e.get("expertise") or [])})
    with col2:
        tag = st.selectbox("الوسوم", ["الكل"] + all_tags, index=0)
    with col3:
        area = st.selectbox("مجال الخبرة", ["الكل"] + all_areas, index=0)

filtered = filter_experts(experts, q, tag, area)

# المحتوى الرئيسي
left, right = st.columns([1.2, 2.5], gap="large")

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">👨‍⚖️ قائمة الخبراء</div>', unsafe_allow_html=True)
    st.caption(f"عرض {len(filtered)} من أصل {len(experts)} خبير")
    
    if not filtered:
        st.info("⚠️ لا توجد نتائج تطابق معايير البحث")
        selected_id = None
    else:
        options = [(e.get("id", e.get("full_name")), e.get("display_name", e.get("full_name"))) for e in filtered]
        labels = [lbl for _, lbl in options]
        ids = [i for i, _ in options]
        
        st.session_state.setdefault("selected_idx", 0)
        if st.session_state.selected_idx >= len(labels):
            st.session_state.selected_idx = 0
        
        selected_label = st.radio(
            "اختر خبيراً من القائمة:",
            labels,
            index=st.session_state.selected_idx,
            label_visibility="collapsed"
        )
        selected_id = ids[labels.index(selected_label)]
        st.session_state.selected_idx = labels.index(selected_label)
    
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    
    if not selected_id:
        st.markdown('<div class="section-title">👤 الملف الشخصي</div>', unsafe_allow_html=True)
        st.info("👈 اختر خبيراً من القائمة لعرض تفاصيله")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        expert = next((e for e in experts if (e.get("id") == selected_id or e.get("full_name") == selected_id)), None)
        if not expert:
            st.error("❌ الخبير المحدد غير موجود")
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-title">{expert.get("display_name","")}</div>', unsafe_allow_html=True)
            
            # المعلومات الأساسية
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("**الجنسية**")
                st.write(expert.get("nationality", "—"))
            with col2:
                st.markdown("**المكان**")
                st.write(expert.get("location", "—"))
            with col3:
                st.markdown("**اللغات**")
                st.write(", ".join(expert.get("languages") or []) or "—")
            
            # مجالات الخبرة
            exp = expert.get("expertise") or []
            if exp:
                st.markdown("**مجالات التخصص**")
                st.write(", ".join(exp))
            
            # تبويبات التفاصيل
            tabs = st.tabs(["📖 نظرة عامة", "🏆 المساهمات", "📚 المنشورات", "📄 الوثائق"])
            
            with tabs[0]:
                bio = expert.get("bio_en") or expert.get("bio", "معلومات السيرة غير متوفرة حالياً.")
                st.write(bio)
            
            with tabs[1]:
                contrib = expert.get("contributions") or []
                if contrib:
                    for item in contrib:
                        st.write(f"• {item}")
                else:
                    st.write("—")
            
            with tabs[2]:
                pubs = expert.get("publications") or []
                if pubs:
                    for p in pubs:
                        if isinstance(p, dict):
                            title = p.get("title", "")
                            year = p.get("year", "")
                            venue = p.get("venue", "")
                            if title:
                                line = f"• **{title}**"
                                if year or venue:
                                    line += f" ({year}{' - ' if year and venue else ''}{venue})"
                                st.write(line)
                        else:
                            st.write(f"• {p}")
                else:
                    st.write("—")
            
            with tabs[3]:
                docs = expert.get("documents") or []
                if not docs:
                    st.info("📭 لا توجد وثائق مرفقة لهذا الملف")
                else:
                    for i, d in enumerate(docs):
                        if isinstance(d, dict):
                            dtitle = d.get("title", f"الوثيقة {i+1}")
                            dfile = d.get("file", "")
                            dtype = d.get("type", "pdf")
                        else:
                            dtitle = f"الوثيقة {i+1}"
                            dfile = str(d)
                            dtype = "pdf"
                        
                        resolved = resolve_doc_path(dfile)
                        
                        with st.expander(f"📄 {dtitle}", expanded=(i == 0)):
                            if not resolved:
                                st.error(f"الملف غير موجود: {dfile}")
                                st.caption("⚠️ تأكد من وجود الملف في مجلد assets/docs/")
                                continue
                            
                            # زر التحميل
                            with open(resolved, "rb") as f:
                                st.download_button(
                                    label=f"📥 تحميل {os.path.basename(resolved)}",
                                    data=f.read(),
                                    file_name=os.path.basename(resolved),
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                            
                            # معاينة PDF
                            if dtype.lower() == "pdf":
                                pdf_iframe_viewer(resolved, height=600)
            
            st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)  # إغلاق main-content-container

# الفوتر
st.markdown(
    """
    <div class="footer">
        <div style="margin-bottom: 10px;">
            <strong>🇮🇶 العراق - دليل الخبراء القانونيين والأكاديميين</strong>
        </div>
        <div>
            التصميم والتطوير: المستشار / كبير المهندسين طارق مجيد الكريمي • الإصدار 2.0
        </div>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #666;">
            جميع الحقوق محفوظة © 2024 • منصة تستلهم إرث شريعة حمورابي أول قانون مكتوب في التاريخ
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
