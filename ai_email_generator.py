import streamlit as st
import google.generativeai as genai
from google.genai import types
import pyperclip
import json
import re

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Email Generator",
    page_icon="✉️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Sans:wght@300;400;500;600&display=swap');

/* ══ FORCE LIGHT EVERYWHERE (MAIN CONTENT ONLY) ══ */
html, body,
[data-testid="stAppViewContainer"],
[data-testid="stAppViewBlockContainer"],
[data-testid="stMain"],
[data-testid="stMainBlockContainer"],
section.main,
.main > div,
.block-container,
[data-testid="column"] {
    background-color: #f5f3ef !important;
    background: #f5f3ef !important;
}

/* Limit main content elements from washing out the sidebar */
[data-testid="stMain"] [data-testid="stVerticalBlock"],
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #f5f3ef !important;
}

/* ══ GLOBAL TEXT ══ */
body, .stApp {
    font-family: 'DM Sans', sans-serif !important;
    color: #1a1a2e !important;
}

[data-testid="stMain"] * {
    color: #1a1a2e !important;
}

/* ══ LABELS ══ */
label,
.stTextInput > label,
.stTextArea > label,
.stSelectbox > label,
.stSlider > label,
[data-testid="stWidgetLabel"],
[data-testid="stWidgetLabel"] > div,
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] span {
    color: #1a1a2e !important;
    font-weight: 500 !important;
    font-size: 0.9rem !important;
}

/* ══ TEXT INPUTS ══ */
.stTextInput input,
.stTextArea textarea,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea {
    background-color: #ffffff !important;
    color: #1a1a2e !important;
    border: 1.5px solid #d6d0ca !important;
    border-radius: 8px !important;
    font-size: 0.9rem !important;
}
.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: #aaa49e !important;
}
.stTextInput input:focus,
.stTextArea textarea:focus {
    border-color: #c8533a !important;
    box-shadow: 0 0 0 3px rgba(200,83,58,0.12) !important;
    outline: none !important;
}

/* ══ SELECTBOX ══ */
.stSelectbox [data-baseweb="select"] > div:first-child,
[data-testid="stSelectbox"] [data-baseweb="select"] > div {
    background-color: #ffffff !important;
    border: 1.5px solid #d6d0ca !important;
    border-radius: 8px !important;
    color: #1a1a2e !important;
}
.stSelectbox [data-baseweb="select"] span,
.stSelectbox [data-baseweb="select"] div {
    color: #1a1a2e !important;
    background-color: transparent !important;
}
[data-baseweb="popover"],
[data-baseweb="menu"],
[role="listbox"] {
    background-color: #ffffff !important;
}
[data-baseweb="menu"] li,
[data-baseweb="menu"] [role="option"],
[role="option"] {
    color: #1a1a2e !important;
    background-color: #ffffff !important;
}
[data-baseweb="menu"] li:hover,
[role="option"]:hover {
    background-color: #fef0eb !important;
}

/* ══ SLIDER ══ */
.stSlider [data-testid="stThumbValue"],
.stSlider [data-testid="stTickBarMin"],
.stSlider [data-testid="stTickBarMax"] {
    color: #1a1a2e !important;
    font-size: 0.8rem !important;
}
.stSlider [role="slider"] {
    background-color: #c8533a !important;
}

/* ══ BUTTONS ══ */
.stButton > button,
.stDownloadButton > button {
    background-color: #c8533a !important;
    color: #ffffff !important;
    border: 2px solid #c8533a !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.92rem !important;
    padding: 0.55rem 1.2rem !important;
    transition: all 0.18s ease !important;
    font-family: 'DM Sans', sans-serif !important;
    width: 100% !important;
    cursor: pointer !important;
}
.stButton > button:hover,
.stDownloadButton > button:hover {
    background-color: #a83e28 !important;
    border-color: #a83e28 !important;
    box-shadow: 0 4px 14px rgba(200,83,58,0.35) !important;
    transform: translateY(-1px) !important;
    color: #ffffff !important;
}

/* ══ SIDEBAR — DARK THEME ══ */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
[data-testid="stSidebar"] [data-testid="stSidebarUserContent"],
[data-testid="stSidebar"] [data-testid="stVerticalBlock"],
[data-testid="stSidebar"] [data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stSidebar"] section {
    background-color: #141428 !important;
    background: #141428 !important;
}

/* Sidebar Text Visibility Rules */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
    color: #f0ede8 !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    font-family: 'DM Serif Display', serif !important;
    color: #faf8f5 !important;
}

/* Sidebar Form Controls UI Fixes */
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] [data-baseweb="input"] input,
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: rgba(255, 255, 255, 0.08) !important;
    border: 1.5px solid rgba(255, 255, 255, 0.18) !important;
    color: #f5f3ef !important;
    border-radius: 8px !important;
}

[data-testid="stSidebar"] .stTextInput input::placeholder {
    color: rgba(255, 255, 255, 0.35) !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] [data-testid="stSelectboxSelectedValue"],
[data-testid="stSidebar"] [data-baseweb="select"] span {
    color: #f0ede8 !important;
}

[data-testid="stSidebar"] .stSlider [data-testid="stThumbValue"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] {
    color: #f0ede8 !important;
}

[data-testid="stSidebar"] hr {
    border-color: rgba(255, 255, 255, 0.12) !important;
}

/* ══ STATUS PILLS ══ */
[data-testid="stSidebar"] .status-ok,
.status-ok {
    background-color: #d4edda !important;
    color: #155724 !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    display: inline-block !important;
}
[data-testid="stSidebar"] .status-ok * {
    color: #155724 !important;
}

[data-testid="stSidebar"] .status-err,
.status-err {
    background-color: #fde8e8 !important;
    color: #8b2c2c !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    display: inline-block !important;
}
[data-testid="stSidebar"] .status-err * {
    color: #8b2c2c !important;
}

/* ══ LAYOUT ══ */
#MainMenu, footer { visibility: hidden !important; }
.block-container { padding: 2rem 3rem !important; max-width: 1380px !important; }

/* ══ HERO ══ */
.hero {
    text-align: center;
    padding: 2.5rem 0 1.8rem;
    border-bottom: 1px solid #ddd8d2;
    margin-bottom: 2rem;
}
.hero-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 3rem !important;
    color: #1a1a2e !important;
    letter-spacing: -0.4px;
    margin: 0;
    line-height: 1.1;
}
.hero-title span { color: #c8533a !important; font-style: italic; }
.hero-sub {
    color: #6b6560 !important;
    font-size: 1rem;
    font-weight: 300;
    margin-top: 0.5rem;
}

/* ══ CARD ══ */
.card {
    background: #ffffff;
    border: 1px solid #ddd8d2;
    border-radius: 14px;
    padding: 1.6rem 1.8rem 1rem;
    box-shadow: 0 2px 14px rgba(26,26,46,0.06);
    margin-bottom: 1rem;
}
.card-title {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.1rem !important;
    color: #1a1a2e !important;
    margin-bottom: 0.8rem;
    display: block;
}

/* ══ EMAIL OUTPUT ══ */
.email-output {
    background: #fffcf8 !important;
    border: 1.5px solid #e8a87c;
    border-radius: 12px;
    padding: 1.6rem 1.8rem;
    font-size: 0.95rem;
    line-height: 1.8;
    color: #1a1a2e !important;
    white-space: pre-wrap;
    word-break: break-word;
    box-shadow: 0 2px 16px rgba(232,168,124,0.12);
}
.output-label {
    font-family: 'DM Serif Display', serif !important;
    font-size: 1.15rem !important;
    color: #1a1a2e !important;
    margin-bottom: 0.6rem;
    display: block;
}
.tone-chip {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    background: #f0ede8;
    color: #4a4540 !important;
    margin-right: 5px;
    margin-bottom: 10px;
    border: 1px solid #ddd8d2;
}

/* ══ HISTORY ITEMS ══ */
.history-item {
    border-left: 3px solid rgba(232,168,124,0.7);
    padding: 5px 10px;
    margin-bottom: 6px;
    font-size: 0.82rem;
    color: rgba(240,237,232,0.8) !important;
    border-radius: 0 6px 6px 0;
    background: rgba(255,255,255,0.04);
}

/* ══ OUTPUT PLACEHOLDER ══ */
.output-placeholder {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 440px;
    border: 2px dashed #ddd8d2;
    border-radius: 14px;
    text-align: center;
    padding: 2rem;
    background: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────────
if "history"         not in st.session_state: st.session_state.history = []
if "generated_email" not in st.session_state: st.session_state.generated_email = ""
if "api_configured"  not in st.session_state: st.session_state.api_configured = False

# ─── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✉️ AI Email Generator")
    st.markdown("---")
    st.markdown("### 🔑 API Configuration")

    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Get your free key at https://aistudio.google.com/",
    )

    if api_key:
        try:
            client_test = genai.Client(api_key=api_key)
            st.session_state.api_configured = True
            st.markdown('<span class="status-ok">✓ API Connected</span>', unsafe_allow_html=True)
        except Exception:
            st.session_state.api_configured = False
            st.markdown('<span class="status-err">✗ API Connection Failed</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-err">No key provided</span>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### ⚙️ Model Settings")

    model_choice = st.selectbox(
        "Gemini Model",
        ["models/gemma-4-31b-it"],
        index=0,
    )
    temperature = st.slider("Creativity", 0.0, 1.0, 0.7, 0.05)
    max_tokens = st.slider("Max Length (tokens)", 200, 2000, 800, 50)

    st.markdown("---")
    st.markdown("### 📋 Recent Generations")

    if st.session_state.history:
        for i, item in enumerate(reversed(st.session_state.history[-5:])):
            st.markdown(
                f'<div class="history-item">#{len(st.session_state.history)-i} · {item["type"]} · {item["tone"]}</div>',
                unsafe_allow_html=True,
            )
        if st.button("🗑 Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.markdown(
            '<p style="color:rgba(240,237,232,0.5);font-size:0.85rem;">No emails generated yet.</p>',
            unsafe_allow_html=True,
        )

# ─── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1 class="hero-title">AI <span>Email</span> Generator</h1>
    <p class="hero-sub">Craft compelling emails in seconds — powered by Google Gemini</p>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1], gap="large")

# ── LEFT: Form ──────────────────────────────────────────────────────────────────
with col_left:
    st.markdown('<div class="card"><span class="card-title">📝 Email Details</span>', unsafe_allow_html=True)

    email_type = st.selectbox(
        "Email Type",
        [
            "Professional Business",
            "Sales & Outreach",
            "Job Application / Cover Letter",
            "Follow-Up",
            "Apology / Complaint Resolution",
            "Newsletter",
            "Thank You",
            "Meeting Request",
            "Cold Outreach",
            "Internal Team Update",
            "Custom",
        ],
    )
    tone = st.selectbox(
        "Tone",
        ["Formal", "Semi-Formal", "Friendly", "Persuasive",
         "Empathetic", "Urgent", "Concise", "Enthusiastic"],
    )
    recipient    = st.text_input("Recipient Name / Role",   placeholder="e.g. Sarah, HR Manager at Acme Corp")
    sender       = st.text_input("Your Name / Role",        placeholder="e.g. John Doe, Product Manager")
    subject_hint = st.text_input("Email Subject (or hint)", placeholder="e.g. Partnership Proposal for Q3")
    key_points   = st.text_area(
        "Key Points / Context",
        placeholder=(
            "• Main purpose of the email\n"
            "• Specific details, numbers, or dates\n"
            "• Desired outcome or call-to-action\n"
            "• Background info the AI should know"
        ),
        height=160,
    )
    extra = st.text_area(
        "Additional Instructions (optional)",
        placeholder="e.g. Keep it under 150 words, include a P.S., avoid jargon…",
        height=80,
    )

    generate_btn = st.button("✨  Generate Email", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Helpers ────────────────────────────────────────────────────────────────────
def build_prompt():
    return f"""Generate a clean, professional email using these parameters:
- Type: {email_type}
- Tone: {tone}
- Recipient: {recipient or 'Recipient'}
- Sender: {sender or 'Sender'}
- Subject Hint: {subject_hint or 'Not specified'}
- Points: {key_points or 'Not specified'}
- Extra: {extra or 'None'}
"""

def run_generation(temp_override=None):
    client = genai.Client(api_key=api_key)
    
    # Restrictive JSON Instruction
    system_instruction = (
        "You are a backend programmatic copywriting engine. You must output a JSON object "
        "containing exactly two root keys: 'subject' and 'body'. Do not output any markdown text, "
        "bold syntax (**), asterisks (*), code block ticks (```), introductory pleasantries, "
        "checklists, or self-correction logs. The output must parse strictly as valid JSON."
    )
    
    response = client.models.generate_content(
        model=model_choice,
        contents=build_prompt(),
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=temp_override if temp_override is not None else temperature,
            max_output_tokens=max_tokens,
            response_mime_type="application/json",
        )
    )
    
    raw_response = response.text
    
    try:
        # Load structured parameters explicitly
        data = json.loads(raw_response)
        subject_line = data.get("subject", "").strip()
        body_text = data.get("body", "").strip()
        
        # Assemble perfectly flat text representation
        clean_text = f"Subject: {subject_line}\n\n{body_text}"
    except Exception:
        # Clean up text fallbacks if anything unexpected trips up the parsing structure
        clean_text = re.sub(r'\*+', '', raw_response)
        clean_text = re.sub(r'```[a-zA-Z]*', '', clean_text)
            
    return clean_text.strip()

# ─── Generate ───────────────────────────────────────────────────────────────────
if generate_btn:
    if not st.session_state.api_configured:
        st.error("⚠️ Please enter a valid Gemini API key in the sidebar first.")
    elif not key_points.strip():
        st.warning("⚠️ Please fill in the Key Points / Context field.")
    else:
        with col_right:
            with st.spinner("✍️ Composing your email…"):
                try:
                    result = run_generation()
                    st.session_state.generated_email = result
                    st.session_state.history.append({
                        "type": email_type, "tone": tone,
                        "subject": subject_hint, "email": result,
                    })
                except Exception as e:
                    st.error(f"Generation failed: {e}")

# ── RIGHT: Output ────────────────────────────────────────────────────────────────
with col_right:
    if st.session_state.generated_email:
        st.markdown('<span class="output-label">📨 Generated Email</span>', unsafe_allow_html=True)
        st.markdown(
            f'<span class="tone-chip">{email_type}</span><span class="tone-chip">{tone}</span>',
            unsafe_allow_html=True,
        )
        st.markdown(
            f'<div class="email-output">{st.session_state.generated_email}</div>',
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.download_button(
                "⬇ Download .txt",
                data=st.session_state.generated_email,
                file_name=f"email_{email_type.replace(' ','_').lower()}.txt",
                mime="text/plain",
                use_container_width=True,
            )
        with c2:
            if st.button("📋 Copy to Clipboard", use_container_width=True):
                try:
                    pyperclip.copy(st.session_state.generated_email)
                    st.success("Copied!")
                except Exception:
                    st.info("Select the text above and copy manually.")
        with c3:
            if st.button("🔄 Regenerate", use_container_width=True):
                if st.session_state.api_configured:
                    with st.spinner("Regenerating…"):
                        try:
                            result = run_generation(temp_override=min(temperature + 0.15, 1.0))
                            st.session_state.generated_email = result
                            st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")

        words = len(st.session_state.generated_email.split())
        st.caption(f"📊 ~{words} words · {len(st.session_state.generated_email)} characters")

    else:
        st.markdown("""
        <div class="output-placeholder">
            <div style="font-size:3.5rem; margin-bottom:1rem;">✉️</div>
            <div style="font-size:1.1rem; font-weight:600; color:#1a1a2e; margin-bottom:0.5rem;">
                Your email will appear here
            </div>
            <div style="font-size:0.9rem; color:#7a7570; font-weight:300;">
                Fill in the details on the left and click<br>
                <strong style="color:#c8533a;">✨ Generate Email</strong>
            </div>
        </div>
        """, unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("""
<p style="text-align:center; color:#a09a94; font-size:0.82rem;">
    Powered by <strong>Google Gemini AI</strong> · Built with Streamlit ·
    <a href="https://aistudio.google.com/" target="_blank" style="color:#c8533a; text-decoration:none;">
        Get your free API key →
    </a>
</p>
""", unsafe_allow_html=True)
