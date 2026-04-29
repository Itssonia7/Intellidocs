import streamlit as st
import sys
import re
from pathlib import Path

# Logic setup
sys.path.append(str(Path(__file__).parent))
from retrieval import retrieve_context, generate_rationale

# 1. Page Configuration
st.set_page_config(page_title="BIS Executive | Discovery", page_icon="⚖️", layout="wide")

# 2. Executive "Modern Industrial Archive" CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* 3. The Subtle "Film Grain" Texture */
    body::before {
        content: "";
        position: fixed;
        top: 0; left: 0;
        width: 100vw; height: 100vh;
        opacity: 0.03;
        pointer-events: none;
        background-image: url('https://www.transparenttextures.com/patterns/felt.png');
        z-index: 9999;
    }

    /* Core Aesthetic: Parchment & Regulatory Navy */
    .stApp {
        background-color: #FDFCF8;
        color: #1A2B4C;
        font-family: 'Inter', sans-serif;
    }

    header { visibility: hidden; }
    .stDeployButton { display:none; }

    /* Glassmorphism Header */
    .nav-header {
        position: fixed;
        top: 0; left: 0; width: 100%;
        padding: 15px 40px;
        background: rgba(253, 252, 248, 0.8);
        backdrop-filter: blur(10px);
        border-bottom: 1px solid rgba(26, 43, 76, 0.1);
        z-index: 999;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* Results Cards: The "Digital Certificate" Look */
    .standard-card {
        background: #ffffff;
        border-radius: 24px;
        padding: 30px;
        margin-bottom: 25px;
        border: 1px solid rgba(26, 43, 76, 0.05);
        /* 1. Continuous Shadow Approach */
        box-shadow: 
            0 2px 4px rgba(0,0,0,0.02),
            0 10px 20px rgba(0,0,0,0.04),
            0 20px 40px rgba(0,0,0,0.06);
        transition: transform 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    
    .standard-card:hover {
        transform: translateY(-5px);
    }

    /* Gold Highlight for #1 Recommendation */
    .top-match {
        border: 2px solid #D4AF37 !important;
    }

    /* 2. Industrial IS Code Tag */
    .is-code-tag {
        font-family: 'JetBrains Mono', monospace;
        font-weight: bold;
        color: #1A2B4C;
        background: #E8EBF0;
        padding: 6px 14px;
        border-left: 4px solid #D4AF37;
        text-transform: uppercase;
        font-size: 14px;
        display: inline-block;
        margin-bottom: 10px;
    }

    /* Rationale Box: Hand-noted Memo */
    .rationale-memo {
        background-color: #F4F1EA;
        border-left: 4px solid #FF4B2B; /* Safety Orange */
        padding: 20px;
        font-style: italic;
        margin-top: 15px;
        border-radius: 4px;
    }

    /* Rulebook Viewport */
    .rulebook-viewport {
        background: #ffffff;
        border-radius: 12px;
        padding: 40px;
        height: 80vh;
        overflow-y: auto;
        border: 1px solid #E2E8F0;
        font-family: 'Libre Baskerville', serif;
        line-height: 1.8;
        box-shadow: inset 0 2px 10px rgba(0,0,0,0.05);
    }

    /* Headings */
    h1, h2, h3 {
        font-family: 'Libre Baskerville', serif;
        color: #1A2B4C;
        font-weight: 700;
    }

    /* Thought-Trace Loader Animation */
    @keyframes pulse-line {
        0% { width: 0%; opacity: 0; }
        50% { width: 100%; opacity: 1; }
        100% { width: 0%; opacity: 0; }
    }
    .loader-line {
        height: 2px;
        background: #D4AF37;
        animation: pulse-line 2s infinite;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TOP NAVIGATION ---
st.markdown("""
    <div class="nav-header">
        <div style="font-family:'Libre Baskerville'; font-size:20px; letter-spacing:1px;">
            <b>BIS</b> <span style="font-weight:200; opacity:0.6;">EXECUTIVE DISCOVERY</span>
        </div>
        <div style="font-family:'JetBrains Mono'; font-size:12px; opacity:0.7;">
            CORE_ENGINE: GEMINI_3.1 // STATUS: ENCRYPTED
        </div>
    </div>
    <div style="margin-top:100px;"></div>
""", unsafe_allow_html=True)

# --- MAIN LAYOUT ---
col_main, col_source = st.columns([6, 4], gap="large")

with col_main:
    st.markdown("<h1>Project Specification</h1>", unsafe_allow_html=True)
    st.caption("Submit material requirements for regulatory authentication.")
    
    query = st.text_area("", placeholder="e.g. Cold-rolled low carbon steel sheets for deep drawing...", label_visibility="collapsed", height=120)
    
    if st.button("AUTHENTICATE AGAINST ARCHIVES"):
        if query:
            # Thought-Trace Animation
            placeholder = st.empty()
            placeholder.markdown("""
                <div style="font-family:'JetBrains Mono'; color:#D4AF37; font-size:14px;">
                    > Analyzing IS Archives...
                    <div class="loader-line"></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Logic Execution
            context_data = retrieve_context(query)
            answer = generate_rationale(query, context_data)
            
            # Regex Cleanup
            clean_ans = str(answer)
            if "'text':" in clean_ans:
                match = re.search(r"'text':\s*'(.*?)'", clean_ans, re.DOTALL)
                if match: clean_ans = match.group(1).replace('\\n', '\n')
            
            placeholder.empty()
            st.session_state['context'] = context_data
            st.session_state['answer'] = clean_ans
            
    if 'answer' in st.session_state:
        st.markdown("<br><h3>Regulatory Findings</h3>", unsafe_allow_html=True)
        # Wrap the result in the "Digital Certificate" card
        st.markdown(f"""
            <div class="standard-card top-match">
                <div class="is-code-tag">OFFICIAL RECOMMENDATION</div>
                <div style="margin-top:10px;">{st.session_state['answer']}</div>
                <div class="rationale-memo">
                    <b>Compliance Note:</b> This recommendation is derived from SP 21:2005 
                    summaries for building material standards.
                </div>
            </div>
        """, unsafe_allow_html=True)

with col_source:
    st.markdown("<h3 style='text-align:right;'>Document Archive</h3>", unsafe_allow_html=True)
    if 'context' in st.session_state:
        st.markdown(f"""
            <div class="rulebook-viewport">
                <div style="font-size:10px; text-align:center; letter-spacing:3px; opacity:0.3; margin-bottom:20px;">
                    — AUTHENTICATED SOURCE MATERIAL —
                </div>
                {st.session_state['context']}
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
            <div class="rulebook-viewport" style="display:flex; align-items:center; justify-content:center; opacity:0.3;">
                <div style="text-align:center;">
                    📖<br>Awaiting Authentication...
                </div>
            </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><hr style='opacity:0.1;'><p style='text-align:center; font-family:\"JetBrains Mono\"; font-size:10px; opacity:0.4;'>SECURE REGULATORY NODE // SONIYA NANWANI // WCE CSE</p>", unsafe_allow_html=True)