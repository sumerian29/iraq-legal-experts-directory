import base64
import json
import os
from typing import Any, Dict, List, Optional

import streamlit as st

# =========================
# CONFIGURATION
# =========================
st.set_page_config(
    page_title="Iraq Legal Experts Directory",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(APP_DIR, "data", "experts.json")

# Assets configuration
MUSIC_CANDIDATES = [
    os.path.join(APP_DIR, "assets", "audio", "ambient.mp3"),
    os.path.join(APP_DIR, "Music.mp3"),
    os.path.join(APP_DIR, "music.mp3"),
    os.path.join(APP_DIR, "ambient.mp3"),  # Added direct file check
]

DOCS_CANDIDATE_DIRS = [
    os.path.join(APP_DIR, "assets", "docs"),
    os.path.join(APP_DIR, "assets", "pdf"),
    os.path.join(APP_DIR, "docs"),
    APP_DIR,
]

BG_CANDIDATES = [
    os.path.join(APP_DIR, "hammurabi_bg.jpg"),
    os.path.join(APP_DIR, "assets", "images", "hammurabi_bg.jpg"),
    os.path.join(APP_DIR, "assets", "hammurabi_bg.jpg"),
    os.path.join(APP_DIR, "background.jpg"),
]

# =========================
# HELPER FUNCTIONS
# =========================
def file_first_existing(candidates: List[str]) -> Optional[str]:
    """Return the first existing file from candidates list."""
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return None

def safe_read_json(path: str) -> Dict[str, Any]:
    """Safely read JSON file, return empty dict if not exists."""
    if not os.path.exists(path):
        return {"experts": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        st.error(f"Error reading JSON file: {e}")
        return {"experts": []}

def b64_from_file(path: str) -> str:
    """Convert file to base64 string."""
    try:
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")
    except Exception as e:
        st.error(f"Error reading file: {e}")
        return ""

def resolve_doc_path(doc_path: str) -> Optional[str]:
    """Resolve document path to absolute path."""
    if not doc_path:
        return None
    
    # Check if absolute path exists
    if os.path.isabs(doc_path) and os.path.exists(doc_path):
        return doc_path
    
    # Check relative to app directory
    rel_path = os.path.join(APP_DIR, doc_path)
    if os.path.exists(rel_path):
        return rel_path
    
    # Check in candidate directories
    filename = os.path.basename(doc_path)
    for directory in DOCS_CANDIDATE_DIRS:
        candidate = os.path.join(directory, filename)
        if os.path.exists(candidate):
            return candidate
    
    return None

def normalize_expert(expert: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize expert data to ensure all fields exist."""
    result = expert.copy()
    
    # Ensure required fields
    result.setdefault("id", result.get("full_name", "").replace(" ", "_").lower())
    result.setdefault("full_name", "")
    result.setdefault("display_name", result.get("full_name"))
    result.setdefault("title", "")
    result.setdefault("title_en", result.get("title", ""))
    result.setdefault("nationality", "Iraqi")
    result.setdefault("location", "Iraq")
    result.setdefault("languages", ["Arabic"])
    result.setdefault("tags", [])
    result.setdefault("expertise", result.get("areas_of_expertise", []))
    result.setdefault("bio", result.get("bio_en", ""))
    result.setdefault("bio_en", result.get("bio", ""))
    result.setdefault("publications", [])
    result.setdefault("documents", [])
    result.setdefault("contributions", [])
    
    # Create display name with title if not already included
    display_name = result.get("display_name", "")
    title_en = result.get("title_en", "")
    if title_en and title_en not in display_name:
        result["display_name"] = f"{title_en} {display_name}".strip()
    
    return result

def inject_custom_css(bg_found: bool) -> None:
    """Inject custom CSS with Hammurabi background and cuneiform watermark."""
    css = """
    <style>
    /* Main background */
    body {
        background-color: #f0f8ff;
        margin: 0;
        padding: 0;
    }
    
    /* App container */
    .stApp {
        background: transparent;
    }
    
    /* Hammurabi side image */
    """
    
    # Add Hammurabi image if found
    bg_path = file_first_existing(BG_CANDIDATES)
    if bg_path and bg_found:
        try:
            bg_b64 = b64_from_file(bg_path)
            css += f"""
            .hammurabi-side-image {{
                position: fixed;
                left: 0;
                top: 0;
                bottom: 0;
                width: 280px;
                background-image: url("data:image/jpeg;base64,{bg_b64}");
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                opacity: 0.15;
                z-index: -2;
                border-right: 2px solid rgba(0, 60, 120, 0.1);
            }}
            """
        except:
            css += ".hammurabi-side-image { display: none; }"
    else:
        css += ".hammurabi-side-image { display: none; }"
    
    # Cuneiform watermark
    cuneiform_text = "𒆳𒀭𒈾𒆠 𒁉𒌑𒋗𒁀 𒅆𒁺𒉌 𒅗𒋛𒈠"
    css += f"""
    /* Cuneiform watermark */
    .cuneiform-watermark {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 5rem;
        font-weight: 900;
        color: rgba(0, 0, 0, 0.08);
        white-space: nowrap;
        z-index: -1;
        pointer-events: none;
        text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
        letter-spacing: 4px;
        font-family: 'Segoe UI', Arial, sans-serif;
    }}
    
    /* Main content area */
    .main-content {{
        margin-left: 300px;
        padding: 20px 40px 20px 30px;
        min-height: 100vh;
    }}
    
    @media (max-width: 768px) {{
        .main-content {{
            margin-left: 0;
            padding: 15px;
        }}
        .hammurabi-side-image {{
            display: none;
        }}
        .cuneiform-watermark {{
            font-size: 3rem;
        }}
    }}
    
    /* Header styling */
    .main-header {{
        background: linear-gradient(135deg, rgba(255,255,255,0.95), rgba(240,248,255,0.95));
        border-radius: 20px;
        padding: 25px 30px;
        margin-bottom: 30px;
        border-left: 5px solid #1e3a8a;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        backdrop-filter: blur(10px);
    }}
    
    .main-header h1 {{
        color: #1e3a8a;
        margin-bottom: 10px;
        font-size: 2.2rem;
    }}
    
    .main-header p {{
        color: #4b5563;
        font-size: 1.1rem;
        margin-bottom: 20px;
    }}
    
    /* Chip styling */
    .expertise-chip {{
        display: inline-block;
        background: rgba(30, 58, 138, 0.1);
        color: #1e3a8a;
        padding: 6px 14px;
        border-radius: 20px;
        margin-right: 8px;
        margin-bottom: 8px;
        font-size: 0.9rem;
        border: 1px solid rgba(30, 58, 138, 0.2);
    }}
    
    /* Panel styling */
    .content-panel {{
        background: rgba(255, 255, 255, 0.92);
        border-radius: 15px;
        padding: 25px;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
        border: 1px solid rgba(30, 58, 138, 0.1);
    }}
    
    .section-title {{
        color: #1e3a8a;
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 2px solid rgba(30, 58, 138, 0.2);
    }}
    
    /* Footer */
    .app-footer {{
        margin-top: 40px;
        padding: 20px;
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        background: rgba(255, 255, 255, 0.8);
        border-radius: 15px;
        border-top: 1px solid rgba(30, 58, 138, 0.1);
    }}
    
    /* Status indicators */
    .status-indicator {{
        display: inline-flex;
        align-items: center;
        padding: 6px 12px;
        border-radius: 10px;
        background: rgba(255, 255, 255, 0.8);
        margin-right: 10px;
        font-size: 0.85rem;
    }}
    
    .status-good {{
        color: #059669;
        background: rgba(5, 150, 105, 0.1);
    }}
    
    .status-warning {{
        color: #d97706;
        background: rgba(217, 119, 6, 0.1);
    }}
    
    /* Music player */
    .music-player {{
        background: rgba(30, 58, 138, 0.05);
        border-radius: 15px;
        padding: 15px;
        margin-top: 20px;
    }}
    </style>
    
    <div class="hammurabi-side-image"></div>
    <div class="cuneiform-watermark">{cuneiform_text}</div>
    """
    
    st.markdown(css, unsafe_allow_html=True)

def setup_music_player():
    """Setup and handle music player functionality."""
    st.session_state.setdefault("music_enabled", False)
    
    music_path = file_first_existing(MUSIC_CANDIDATES)
    
    # Music toggle button
    col1, col2 = st.columns([1, 4])
    with col1:
        button_label = "🔇 Music OFF" if not st.session_state.music_enabled else "🔊 Music ON"
        if st.button(button_label, use_container_width=True, type="primary"):
            st.session_state.music_enabled = not st.session_state.music_enabled
            st.rerun()
    
    # Display music status
    with col2:
        if music_path:
            if st.session_state.music_enabled:
                st.success("Ambient music is playing")
            else:
                st.info("Music is paused")
        else:
            st.warning("Music file not found. Add 'ambient.mp3' to assets/audio/")
    
    # Audio player
    if music_path and st.session_state.music_enabled:
        try:
            audio_bytes = open(music_path, "rb").read()
            st.audio(audio_bytes, format="audio/mp3", autoplay=True)
        except Exception as e:
            st.error(f"Error loading audio: {e}")

def filter_experts(experts: List[Dict[str, Any]], search_query: str, selected_tag: str, selected_expertise: str) -> List[Dict[str, Any]]:
    """Filter experts based on search criteria."""
    filtered = experts
    
    # Search query filter
    if search_query:
        search_lower = search_query.lower()
        filtered = [
            e for e in filtered
            if (search_lower in e.get("full_name", "").lower() or
                search_lower in e.get("display_name", "").lower() or
                search_lower in e.get("bio_en", "").lower() or
                any(search_lower in tag.lower() for tag in e.get("tags", [])) or
                any(search_lower in exp.lower() for exp in e.get("expertise", [])))
        ]
    
    # Tag filter
    if selected_tag and selected_tag != "All":
        filtered = [e for e in filtered if selected_tag in e.get("tags", [])]
    
    # Expertise filter
    if selected_expertise and selected_expertise != "All":
        filtered = [e for e in filtered if selected_expertise in e.get("expertise", [])]
    
    return filtered

def display_expert_details(expert: Dict[str, Any]):
    """Display detailed information about an expert."""
    st.markdown(f"## {expert.get('display_name', 'Expert Profile')}")
    
    # Basic information
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("**Nationality**")
        st.write(expert.get('nationality', 'Not specified'))
    
    with col2:
        st.markdown("**Location**")
        st.write(expert.get('location', 'Not specified'))
    
    with col3:
        st.markdown("**Languages**")
        st.write(", ".join(expert.get('languages', ['Not specified'])))
    
    # Expertise chips
    expertise_list = expert.get('expertise', [])
    if expertise_list:
        st.markdown("**Areas of Expertise**")
        chips_html = '<div style="margin: 10px 0;">'
        for exp in expertise_list:
            chips_html += f'<span class="expertise-chip">{exp}</span>'
        chips_html += '</div>'
        st.markdown(chips_html, unsafe_allow_html=True)
    
    # Tabs for detailed information
    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Contributions", "Publications", "Documents"])
    
    with tab1:
        bio = expert.get('bio_en', expert.get('bio', 'No biography available.'))
        st.write(bio)
    
    with tab2:
        contributions = expert.get('contributions', [])
        if contributions:
            for item in contributions:
                st.write(f"• {item}")
        else:
            st.write("No contributions listed.")
    
    with tab3:
        publications = expert.get('publications', [])
        if publications:
            for pub in publications:
                if isinstance(pub, dict):
                    title = pub.get('title', 'Untitled')
                    year = pub.get('year', '')
                    venue = pub.get('venue', '')
                    st.write(f"• **{title}**")
                    if year or venue:
                        st.write(f"  _{year}{' - ' if year and venue else ''}{venue}_")
                else:
                    st.write(f"• {pub}")
        else:
            st.write("No publications listed.")
    
    with tab4:
        documents = expert.get('documents', [])
        if not documents:
            st.info("No documents attached to this profile.")
        else:
            for i, doc in enumerate(documents):
                if isinstance(doc, dict):
                    doc_title = doc.get('title', f'Document {i+1}')
                    doc_file = doc.get('file', '')
                    doc_type = doc.get('type', 'pdf')
                else:
                    doc_title = f'Document {i+1}'
                    doc_file = str(doc)
                    doc_type = 'pdf'
                
                with st.expander(doc_title, expanded=(i == 0)):
                    resolved_path = resolve_doc_path(doc_file)
                    if resolved_path:
                        # Download button
                        try:
                            with open(resolved_path, "rb") as f:
                                st.download_button(
                                    label=f"📥 Download {os.path.basename(resolved_path)}",
                                    data=f.read(),
                                    file_name=os.path.basename(resolved_path),
                                    mime="application/pdf",
                                    use_container_width=True
                                )
                        except Exception as e:
                            st.error(f"Error accessing file: {e}")
                    else:
                        st.warning(f"Document not found: {doc_file}")

# =========================
# MAIN APP
# =========================
def main():
    # Load data
    data = safe_read_json(DATA_PATH)
    experts_raw = data.get("experts", [])
    experts = [normalize_expert(e) for e in experts_raw]
    
    # Check for background image
    bg_path = file_first_existing(BG_CANDIDATES)
    bg_found = bg_path is not None
    
    # Inject custom CSS
    inject_custom_css(bg_found)
    
    # Start main content area
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header section
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.markdown("# 🇮🇶 Iraq - Legal Experts & Academics Directory")
    st.markdown("### A modern platform inspired by Mesopotamia's heritage (Code of Hammurabi · Akkadian Era · Cuneiform Legacy)")
    
    # Status indicators
    col1, col2 = st.columns(2)
    with col1:
        status_class = "status-good" if bg_found else "status-warning"
        status_text = "✓ Background image found" if bg_found else "⚠ Background image not found"
        st.markdown(f'<div class="status-indicator {status_class}">{status_text}</div>', unsafe_allow_html=True)
    
    with col2:
        music_path = file_first_existing(MUSIC_CANDIDATES)
        music_status = "✓ Music file found" if music_path else "⚠ Music file not found"
        status_class = "status-good" if music_path else "status-warning"
        st.markdown(f'<div class="status-indicator {status_class}">{music_status}</div>', unsafe_allow_html=True)
    
    # Expertise chips
    st.markdown('<div style="margin-top: 20px;">', unsafe_allow_html=True)
    chips = ["⚖️ Legal Studies", "📚 Academic Research", "🏛️ Hammurabi Legacy", 
             "𒀭 Cuneiform", "🌍 International Law", "👨‍⚖️ Iraqi Experts"]
    chips_html = ""
    for chip in chips:
        chips_html += f'<span class="expertise-chip">{chip}</span>'
    st.markdown(chips_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close main-header
    
    # Music player section
    with st.container():
        st.markdown('<div class="music-player">', unsafe_allow_html=True)
        st.markdown("### 🎵 Ambient Music")
        setup_music_player()
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Filters section
    with st.expander("🔍 Search Filters", expanded=True):
        col1, col2, col3 = st.columns([2, 1.5, 1.5])
        
        with col1:
            search_query = st.text_input("Search by name, bio, expertise, or tags:", "")
        
        # Get unique tags and expertise for filters
        all_tags = sorted(set(tag for expert in experts for tag in expert.get("tags", [])))
        all_expertise = sorted(set(exp for expert in experts for exp in expert.get("expertise", [])))
        
        with col2:
            selected_tag = st.selectbox("Filter by tag:", ["All"] + all_tags)
        
        with col3:
            selected_expertise = st.selectbox("Filter by expertise:", ["All"] + all_expertise)
    
    # Filter experts
    filtered_experts = filter_experts(experts, search_query, selected_tag, selected_expertise)
    
    # Main content columns
    col_left, col_right = st.columns([1.2, 2.5], gap="large")
    
    with col_left:
        st.markdown('<div class="content-panel">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">👨‍⚖️ Experts List</div>', unsafe_allow_html=True)
        st.caption(f"Showing {len(filtered_experts)} of {len(experts)} experts")
        
        if not filtered_experts:
            st.info("No experts match your search criteria.")
            selected_expert_id = None
        else:
            # Create list of expert names for selection
            expert_options = [
                (expert.get("id", expert.get("full_name", "")), 
                 expert.get("display_name", expert.get("full_name", "Unnamed Expert")))
                for expert in filtered_experts
            ]
            
            # Store in session state
            if "selected_expert_index" not in st.session_state:
                st.session_state.selected_expert_index = 0
            
            # Adjust index if out of bounds
            if st.session_state.selected_expert_index >= len(expert_options):
                st.session_state.selected_expert_index = 0
            
            # Create radio buttons for selection
            expert_names = [name for _, name in expert_options]
            selected_name = st.radio(
                "Select an expert:",
                expert_names,
                index=st.session_state.selected_expert_index,
                label_visibility="collapsed"
            )
            
            # Get selected expert ID
            selected_expert_id = None
            for exp_id, exp_name in expert_options:
                if exp_name == selected_name:
                    selected_expert_id = exp_id
                    break
            
            # Update session state
            st.session_state.selected_expert_index = expert_names.index(selected_name)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col_right:
        st.markdown('<div class="content-panel">', unsafe_allow_html=True)
        
        if not selected_expert_id:
            st.markdown('<div class="section-title">👤 Expert Profile</div>', unsafe_allow_html=True)
            st.info("👈 Select an expert from the list to view their profile details")
        else:
            # Find the selected expert
            selected_expert = next(
                (expert for expert in experts 
                 if expert.get("id") == selected_expert_id or 
                    expert.get("full_name") == selected_expert_id),
                None
            )
            
            if selected_expert:
                display_expert_details(selected_expert)
            else:
                st.error("Selected expert not found in database.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown('<div class="app-footer">', unsafe_allow_html=True)
    st.markdown("### 🇮🇶 Iraq Legal Experts Directory")
    st.markdown("**Design & Development:** Consultant / Senior Chief Engineer Tareq Majeed Al-Karimi • Version 2.0")
    st.markdown("© 2024 All rights reserved • A platform inspired by the Code of Hammurabi - the first written law in history")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Close main content div
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
