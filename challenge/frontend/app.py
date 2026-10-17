"""
Learnify — E-Learning Platform Frontend
"""
import os
import streamlit as st
import requests

API = os.environ.get("API_BASE_URL", "http://localhost:8000/api").rstrip("/")

st.set_page_config(
    page_title="Learnify — Learn to Code",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS ───────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg:       #f6f7fb;
  --white:    #ffffff;
  --surface:  #eef1f8;
  --card:     #ffffff;
  --border:   #e4e8f1;
  --border-2: #d7dced;
  --accent:   #6366f1;
  --accent-d: #4f46e5;
  --accent2:  #ec4899;
  --green:    #10b981;
  --yellow:   #f59e0b;
  --ink:      #0f172a;
  --text:     #1e2538;
  --muted:    #697089;
  --shadow:   0 1px 2px rgba(16,24,40,.04), 0 6px 20px rgba(16,24,40,.06);
  --shadow-h: 0 2px 4px rgba(16,24,40,.05), 0 14px 36px rgba(79,70,229,.14);
  --radius:   16px;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif !important;
    -webkit-font-smoothing: antialiased;
}
[data-testid="stAppViewContainer"] > .main { padding-top: 0 !important; }
[data-testid="stSidebar"] { display: none; }
[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding: 0 2rem 4rem !important; max-width: 1140px !important; margin: 0 auto !important; }

/* Buttons */
.stButton > button {
    background: var(--accent) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 11px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: .01em !important;
    padding: .55rem 1.5rem !important;
    transition: transform .15s ease, box-shadow .15s ease, background .15s ease !important;
    box-shadow: 0 1px 2px rgba(16,24,40,.06), 0 4px 12px rgba(99,102,241,.22) !important;
}
.stButton > button:hover { background: var(--accent-d) !important; transform: translateY(-1px) !important; box-shadow: 0 2px 4px rgba(16,24,40,.08), 0 8px 22px rgba(79,70,229,.3) !important; }
.stButton > button:active { transform: translateY(0) !important; }

/* Inputs */
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    background: var(--white) !important;
    color: var(--text) !important;
    border: 1.5px solid var(--border-2) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input::placeholder { color: #9aa1b5 !important; }
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus { border-color: var(--accent) !important; box-shadow: 0 0 0 3px rgba(99,102,241,.14) !important; }
input[type="password"] { font-family: 'JetBrains Mono', monospace !important; }

h1,h2,h3,h4 { font-family: 'Inter', sans-serif !important; font-weight: 800 !important; letter-spacing: -.02em !important; color: var(--ink) !important; }
p, li, span { font-family: 'Inter', sans-serif !important; }
code { font-family: 'JetBrains Mono', monospace !important; background: var(--surface) !important; padding: 2px 6px !important; border-radius: 6px !important; color: var(--accent-d) !important; font-size: .85em !important; }
hr { border-color: var(--border) !important; }
a { color: var(--accent) !important; text-decoration: none !important; }
a:hover { color: var(--accent-d) !important; }

/* Top nav */
.topnav {
    background: rgba(255,255,255,.85);
    backdrop-filter: saturate(180%) blur(12px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: .85rem 1.4rem;
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin: 1rem 0 .25rem;
    box-shadow: var(--shadow);
    position: sticky; top: .5rem; z-index: 100;
}
.topnav-logo { font-size: 1.4rem; font-weight: 900; color: var(--ink); letter-spacing: -.03em; }
.topnav-logo span { color: var(--accent); }
.topnav-links { display: flex; gap: 1.8rem; }
.topnav-links a { color: var(--muted) !important; font-weight: 600; font-size: .92rem; transition: color .15s; }
.topnav-links a:hover, .topnav-links a.active { color: var(--accent) !important; }

/* Hero */
.hero-section {
    background: linear-gradient(135deg, #4f46e5 0%, #6366f1 45%, #a855f7 100%);
    border-radius: 24px;
    padding: 3.6rem 3rem;
    margin: 1.25rem 0 2.25rem;
    color: #fff;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 48px rgba(79,70,229,.28);
}
.hero-section::before {
    content: '';
    position: absolute;
    top: -45%; right: -8%;
    width: 480px; height: 480px;
    background: radial-gradient(circle, rgba(255,255,255,.16), transparent 70%);
    border-radius: 50%;
}
.hero-section h1 { color: #fff !important; font-size: 2.7rem; margin-bottom: .5rem; line-height: 1.12; letter-spacing: -.03em; }
.hero-section p { color: rgba(255,255,255,.9) !important; font-size: 1.08rem; max-width: 540px; margin-bottom: 1.5rem; line-height: 1.6; }
.hero-badge { display: inline-block; background: rgba(255,255,255,.16); border: 1px solid rgba(255,255,255,.28); border-radius: 50px; padding: 5px 15px; font-size: .8rem; font-weight: 600; color: #fff !important; margin-bottom: 1.1rem; backdrop-filter: blur(4px); }

/* Course card */
.course-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.4rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    cursor: pointer;
    height: 100%;
}
.course-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-h); border-color: var(--border-2); }
.course-emoji { font-size: 2.5rem; margin-bottom: .75rem; display: block; }
.course-card h4 { font-size: 1rem; margin: 0 0 .3rem; color: var(--ink); }
.course-card .instructor { color: var(--muted); font-size: .82rem; margin-bottom: .6rem; }

.badge { display: inline-block; padding: 3px 11px; border-radius: 50px; font-size: .74rem; font-weight: 700; margin-right: 4px; letter-spacing: .01em; }
.badge-beginner { background: #dcfce7; color: #15803d; }
.badge-intermediate { background: #dbeafe; color: #1d4ed8; }
.badge-advanced { background: #fef3c7; color: #b45309; }
.badge-expert { background: #fce7f3; color: #be185d; }
.badge-free { background: #dcfce7; color: #15803d; }
.badge-paid { background: #eef2ff; color: #4338ca; }
.price-tag { font-weight: 800; font-size: 1rem; color: var(--accent); }
.stars { color: var(--yellow); font-size: .85rem; }
.stat-row { display: flex; gap: .75rem; align-items: center; margin-top: .5rem; font-size: .8rem; color: var(--muted); }

.topic-header { display: flex; align-items: center; gap: .85rem; margin: 2.5rem 0 1.1rem; }
.topic-header h3 { margin: 0; font-size: 1.3rem; }
.topic-pill { background: var(--surface); border: 1px solid var(--border); border-radius: 50px; padding: 4px 14px; font-size: .8rem; font-weight: 700; color: var(--accent); }
.coming-soon-card {
    background: linear-gradient(135deg, #f8f9fe, #eef2ff);
    border: 1.5px dashed var(--border-2);
    border-radius: var(--radius);
    padding: 2rem;
    text-align: center;
    color: var(--muted);
}

.teacher-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.6rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease;
}
.teacher-card:hover { transform: translateY(-3px); box-shadow: var(--shadow-h); }
.teacher-avatar { font-size: 3rem; margin-bottom: .5rem; }

.stat-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.5rem;
    border: 1px solid var(--border);
    text-align: center;
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease;
}
.stat-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-h); }
.stat-card .val { font-size: 2rem; font-weight: 900; color: var(--accent); letter-spacing: -.02em; }
.stat-card .lab { color: var(--muted); font-size: .85rem; font-weight: 600; margin-top: .2rem; }

.feature-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.6rem;
    border: 1px solid var(--border);
    box-shadow: var(--shadow);
    transition: transform .18s ease, box-shadow .18s ease;
}
.feature-card:hover { transform: translateY(-2px); box-shadow: var(--shadow-h); }
.feature-icon { font-size: 2rem; margin-bottom: .5rem; }

.page-header {
    padding: 1.5rem 0 1rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2rem;
}
.page-header h2 { margin: 0 0 .25rem; font-size: 1.9rem; }
.page-header p { color: var(--muted); margin: 0; }

.chat-bubble-user {
    background: var(--accent);
    color: #fff !important;
    border-radius: 18px 18px 4px 18px;
    padding: .7rem 1rem;
    margin: .4rem 0 .4rem auto;
    max-width: 70%;
    display: table;
    font-size: .93rem;
    box-shadow: 0 4px 12px rgba(99,102,241,.22);
}
.chat-bubble-bot {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 18px 18px 18px 4px;
    padding: .7rem 1rem;
    margin: .4rem 0;
    max-width: 80%;
    font-size: .93rem;
    box-shadow: var(--shadow);
}
.chat-meta { font-size: .74rem; color: var(--muted); margin-bottom: .2rem; font-weight: 700; }

.code-output {
    background: #0f172a;
    color: #e2e8f0;
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    font-family: 'JetBrains Mono', monospace;
    font-size: .85rem;
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.6;
    border: 1px solid #1e293b;
}

.api-key-banner {
    background: linear-gradient(135deg, #eef2ff, #e0f2fe);
    border: 1px solid var(--border-2);
    border-radius: 14px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: .75rem;
}

.course-detail-hero {
    background: linear-gradient(135deg, #0f172a, #312e81);
    border-radius: 20px;
    padding: 2.5rem;
    color: #fff;
    margin-bottom: 2rem;
    box-shadow: 0 16px 40px rgba(15,23,42,.25);
}
.course-detail-hero h2 { color: #fff !important; font-size: 1.9rem; margin-bottom: .5rem; }
.course-detail-hero p { color: rgba(255,255,255,.78) !important; line-height: 1.6; }
.syllabus-item {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 11px;
    padding: .8rem 1rem;
    margin-bottom: .5rem;
    display: flex;
    align-items: center;
    gap: .75rem;
    transition: border-color .15s ease;
}
.syllabus-item:hover { border-color: var(--border-2); }

.search-bar-wrap {
    background: var(--card);
    border-radius: 50px;
    border: 1.5px solid var(--border-2);
    box-shadow: var(--shadow);
    padding: .5rem .5rem .5rem 1.2rem;
    display: flex;
    align-items: center;
    gap: .5rem;
    transition: border-color .2s;
}
.search-bar-wrap:focus-within { border-color: var(--accent); }

.footer-strip {
    background: var(--ink);
    color: rgba(255,255,255,.62);
    text-align: center;
    padding: 1.5rem;
    border-radius: var(--radius);
    margin-top: 4rem;
    font-size: .85rem;
}

/* Search */
.search-hero {
    background: linear-gradient(135deg, #0f172a 0%, #312e81 100%);
    border-radius: 20px;
    padding: 2.4rem 2rem;
    margin-bottom: 2rem;
    color: #fff;
    box-shadow: 0 16px 40px rgba(15,23,42,.22);
}
.search-hero h2 { color: #fff !important; margin: 0 0 .25rem; font-size: 1.6rem; }
.search-hero p  { color: rgba(255,255,255,.68) !important; margin: 0 0 1.2rem; font-size: .9rem; }
.search-summary {
    background: var(--surface);
    border-left: 4px solid var(--accent);
    border-radius: 0 10px 10px 0;
    padding: .75rem 1rem;
    margin-bottom: 1.5rem;
    font-size: .9rem;
    color: var(--text);
}
.result-section-title {
    font-size: .72rem;
    font-weight: 800;
    letter-spacing: .1em;
    text-transform: uppercase;
    color: var(--muted);
    margin: 1.8rem 0 .75rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.result-section-title::after { content: ''; flex: 1; height: 1px; background: var(--border); }
.search-course-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1.1rem 1.3rem;
    margin-bottom: .75rem;
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease;
    cursor: pointer;
}
.search-course-card:hover { border-color: var(--border-2); box-shadow: var(--shadow-h); transform: translateX(3px); }
.search-card-emoji { font-size: 2rem; flex-shrink: 0; margin-top: .1rem; }
.search-card-body { flex: 1; min-width: 0; }
.search-card-title { font-weight: 800; font-size: .97rem; margin-bottom: .2rem; color: var(--ink); }
.search-card-meta  { font-size: .78rem; color: var(--muted); margin-bottom: .35rem; }
.search-card-reason { font-size: .82rem; color: var(--accent); font-weight: 600; }
.search-card-price { font-weight: 800; font-size: .92rem; color: var(--accent); flex-shrink: 0; text-align: right; white-space: nowrap; }
.search-teacher-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 1rem 1.3rem;
    margin-bottom: .75rem;
    display: flex;
    gap: 1rem;
    align-items: center;
    transition: border-color .18s ease, box-shadow .18s ease, transform .18s ease;
    cursor: pointer;
}
.search-teacher-card:hover { border-color: var(--border-2); box-shadow: var(--shadow-h); transform: translateX(3px); }
.search-no-results { text-align: center; padding: 3rem 1rem; color: var(--muted); }
.search-no-results .icon { font-size: 3rem; margin-bottom: .5rem; }

/* Nav buttons row */
[data-testid="stButton"] button { font-size: .88rem !important; }
[data-testid="stButton"] button img,
[data-testid="stButton"] button span[role="img"] {
    font-size: 1rem !important;
    width: 1rem !important;
    height: 1rem !important;
    display: inline-block !important;
    vertical-align: middle !important;
}

/* Hide streamlit chrome */
#MainMenu, footer, [data-testid="stToolbar"] { display: none !important; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_course_id" not in st.session_state:
    st.session_state.selected_course_id = None
if "selected_teacher_id" not in st.session_state:
    st.session_state.selected_teacher_id = None
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_results" not in st.session_state:
    st.session_state.search_results = None

def nav(page, course_id=None, teacher_id=None):
    st.session_state.page = page
    st.session_state.selected_course_id = course_id
    st.session_state.selected_teacher_id = teacher_id

def do_search(query: str):
    """Trigger an AI search and navigate to the search results page."""
    st.session_state.search_query = query
    st.session_state.search_results = None   # will be fetched on the search page
    nav("search")

def api_get(path):
    try:
        return requests.get(f"{API}{path}", timeout=6).json()
    except:
        return None

def api_post(path, payload):
    try:
        return requests.post(f"{API}{path}", json=payload, timeout=45).json()
    except Exception as e:
        return {"error": str(e)}

# ── Top Nav ───────────────────────────────────────────────────────────────────
page = st.session_state.page

def nav_link(label, target):
    active = "active" if page == target else ""
    return f'<a class="{active}" href="#" onclick="void(0)">{label}</a>'

st.markdown(f"""
<div class="topnav">
  <div class="topnav-logo">Learn<span>ify</span></div>
  <div class="topnav-links">
    {nav_link("Home", "home")}
    {nav_link("Courses", "courses")}
    {nav_link("Instructors", "teachers")}
    {nav_link("About", "about")}
    {nav_link("Assistant", "chatbot")}
    {nav_link("Code Review", "code_review")}
  </div>
  <div style="font-size:.85rem;color:var(--muted);font-weight:600">🔑 {("Key set ✓" if st.session_state.api_key else "No API key")}</div>
</div>
""", unsafe_allow_html=True)

# Nav buttons (hidden behind styled nav visually; real navigation via columns)
nb_cols = st.columns([1,1,1,1,1,1,1,1,1])
with nb_cols[1]:
    if st.button("🏠 Home", key="nb_home", use_container_width=True): nav("home")
with nb_cols[2]:
    if st.button("📚 Courses", key="nb_courses", use_container_width=True): nav("courses")
with nb_cols[3]:
    if st.button("👤 Instructors", key="nb_teachers", use_container_width=True): nav("teachers")
with nb_cols[4]:
    if st.button("About", key="nb_about", use_container_width=True): nav("about")
with nb_cols[5]:
    if st.button("💬 Assistant", key="nb_chat", use_container_width=True): nav("chatbot")
with nb_cols[6]:
    if st.button("🛠 Code Review", key="nb_cr", use_container_width=True): nav("code_review")
with nb_cols[7]:
    if st.button("⚙ Settings", key="nb_settings", use_container_width=True): nav("settings")

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

# ── API key warning ───────────────────────────────────────────────────────────
if not st.session_state.api_key and page not in ("home","about","courses","teachers","course_detail","teacher_detail","settings","code_review"):
    st.warning("⚠️ Some features require a Gemini API key. Go to **Settings** to add yours.", icon="🔑")

page = st.session_state.page  # re-read after nav buttons

# ══════════════════════════════════════════════════════════════════════════════
# HOME
# ══════════════════════════════════════════════════════════════════════════════
if page == "home":
    st.markdown("""
    <div class="hero-section">
      <div class="hero-badge">✨ New courses added every month</div>
      <h1>Learn to Code.<br>Build Real Things.</h1>
      <p>Structured courses, hands-on projects, and an AI-powered assistant to help you every step of the way.</p>
    </div>
    """, unsafe_allow_html=True)

    # Search bar
    st.markdown("### 🔍 What do you want to learn today?")
    s_col1, s_col2 = st.columns([5,1])
    with s_col1:
        search_q = st.text_input("search_home", placeholder="e.g. Python for beginners, React, SQL...", label_visibility="collapsed")
    with s_col2:
        do_search_btn = st.button("Search", key="home_search", use_container_width=True)

    if do_search_btn and search_q.strip():
        if not st.session_state.api_key:
            st.info("💡 Add your Gemini API key in **Settings** to use AI-powered search.")
        else:
            do_search(search_q.strip())
            st.rerun()

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Stats row
    s1,s2,s3,s4 = st.columns(4)
    for col, val, lab in zip([s1,s2,s3,s4], ["10+","4","500+","4.8★"], ["Courses","Expert Instructors","Happy Students","Avg Rating"]):
        with col:
            st.markdown(f'<div class="stat-card"><div class="val">{val}</div><div class="lab">{lab}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Featured courses
    st.markdown("### 🌟 Popular Courses")
    courses = api_get("/courses") or []
    featured = [c for c in courses if c.get("students",0) > 500][:6]
    cols = st.columns(3)
    for i, c in enumerate(featured):
        with cols[i % 3]:
            level_cls = f"badge-{c['level'].lower()}"
            price_str = "Free" if c['price']==0 else f"${c['price']:.2f}"
            stars = "⭐" * int(round(c.get("rating",4.5)))
            if st.button(f"**{c['thumbnail_emoji']} {c['title']}**\n\n_{c['instructor']}_", key=f"feat_{c['id']}", use_container_width=True):
                nav("course_detail", course_id=c["id"])
            st.markdown(f"""
            <div style="margin-top:-8px;margin-bottom:1rem;padding:.5rem .3rem">
              <span class="badge {level_cls}">{c['level']}</span>
              <span style="font-size:.8rem;color:var(--muted);margin-left:.5rem">{c['duration']} · {price_str}</span>
            </div>""", unsafe_allow_html=True)

    # Why Learnify
    st.markdown("### 💡 Why Learnify?")
    f1,f2,f3 = st.columns(3)
    features = [
        ("🤖", "AI Learning Assistant", "Ask Lia anything — from syntax questions to career advice. Available 24/7."),
        ("🔧", "Code Review Tool", "Paste your code and get instant feedback with best-practice suggestions."),
        ("🏗️", "Project-Based", "Every course ends with a real project you can add to your portfolio."),
    ]
    for col, (icon, title, desc) in zip([f1,f2,f3], features):
        with col:
            st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><strong>{title}</strong><p style="color:var(--muted);font-size:.88rem;margin:.4rem 0 0">{desc}</p></div>', unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# COURSES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "courses":
    st.markdown('<div class="page-header"><h2>📚 All Courses</h2><p>Choose a path and start building today.</p></div>', unsafe_allow_html=True)

    courses = api_get("/courses") or []
    if not courses:
        st.error("Could not load courses. Make sure the backend is running.")
        st.stop()

    # Search
    s1, s2 = st.columns([4,1])
    with s1:
        search_q = st.text_input("course_search", placeholder="Search courses or topics with AI…", label_visibility="collapsed")
    with s2:
        do_ai_search = st.button("🔍 AI Search", key="course_ai_search", use_container_width=True)

    if do_ai_search and search_q.strip():
        if not st.session_state.api_key:
            st.info("💡 Add your Gemini API key in **Settings** to use AI-powered search.")
        else:
            do_search(search_q.strip())
            st.rerun()

    # Group by topic
    topics = {}
    for c in courses:
        t = c.get("topic", "Other")
        topics.setdefault(t, []).append(c)

    # Topic order
    topic_order = ["Programming Fundamentals", "Frontend Development", "Backend Development", "Low-Level Programming"]
    topic_icons = {
        "Programming Fundamentals": ("🧩", "Build the foundation every developer needs"),
        "Frontend Development":     ("🎨", "Create beautiful, interactive user interfaces"),
        "Backend Development":      ("🔧", "Power the server side of modern applications"),
        "Low-Level Programming":    ("🔩", "Go deep into systems and hardware"),
    }

    level_cls_map = {"Beginner":"badge-beginner","Intermediate":"badge-intermediate","Advanced":"badge-advanced","Expert":"badge-expert"}

    for topic in topic_order:
        icon, tagline = topic_icons.get(topic, ("📂",""))
        st.markdown(f"""
        <div class="topic-header">
          <span style="font-size:1.6rem">{icon}</span>
          <div>
            <h3>{topic}</h3>
            <span style="color:var(--muted);font-size:.85rem">{tagline}</span>
          </div>
        </div>""", unsafe_allow_html=True)

        topic_courses = topics.get(topic, [])
        published = [c for c in topic_courses if c.get("is_published",1)]
        coming_soon = [c for c in topic_courses if not c.get("is_published",1)]

        if not published and not coming_soon:
            continue

        if published:
            cols = st.columns(min(len(published), 3))
            for i, c in enumerate(published):
                with cols[i % 3]:
                    level_cls = level_cls_map.get(c["level"], "badge-intermediate")
                    price_str = "Free" if c["price"]==0 else f"${c['price']:.2f}"
                    if st.button(f"{c['thumbnail_emoji']}  {c['title']}", key=f"c_{c['id']}", use_container_width=True):
                        nav("course_detail", course_id=c["id"])
                    st.markdown(f"""
                    <div style="margin-top:-6px;margin-bottom:.8rem;padding:0 .2rem">
                      <div style="font-size:.8rem;color:var(--muted);margin-bottom:.2rem">{c['instructor']}</div>
                      <span class="badge {level_cls}">{c['level']}</span>
                      <span class="badge {'badge-free' if c['price']==0 else 'badge-paid'}">{price_str}</span>
                      <div style="font-size:.78rem;color:var(--muted);margin-top:.2rem">⏱ {c['duration']} · 👥 {c['students']:,} students · ⭐ {c['rating']}</div>
                    </div>""", unsafe_allow_html=True)

        if coming_soon:
            for c in coming_soon:
                st.markdown(f"""
                <div class="coming-soon-card">
                  <span style="font-size:2rem">{c['thumbnail_emoji']}</span>
                  <p style="margin:.5rem 0 .2rem;font-weight:700;color:var(--text)">{c['title']}</p>
                  <p style="margin:0;font-size:.85rem">{c['description']}</p>
                  <span class="badge badge-advanced" style="margin-top:.5rem;display:inline-block">Coming Soon</span>
                </div>""", unsafe_allow_html=True)

        st.markdown("<hr>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# COURSE DETAIL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "course_detail":
    cid = st.session_state.selected_course_id
    if not cid:
        nav("courses"); st.rerun()

    course = api_get(f"/courses/{cid}")
    if not course:
        st.error("Course not found."); st.stop()

    if st.button("← Back to Courses", key="back_courses"):
        nav("courses"); st.rerun()

    level_cls_map = {"Beginner":"badge-beginner","Intermediate":"badge-intermediate","Advanced":"badge-advanced","Expert":"badge-expert"}
    level_cls = level_cls_map.get(course["level"], "badge-intermediate")
    price_str = "Free" if course["price"]==0 else f"${course['price']:.2f}"

    st.markdown(f"""
    <div class="course-detail-hero">
      <div style="font-size:3rem;margin-bottom:.5rem">{course['thumbnail_emoji']}</div>
      <h2>{course['title']}</h2>
      <p>{course['long_description']}</p>
      <div style="display:flex;gap:1rem;flex-wrap:wrap;margin-top:1rem">
        <span class="badge {level_cls}">{course['level']}</span>
        <span style="color:rgba(255,255,255,.7);font-size:.88rem">👨‍🏫 {course['instructor']}</span>
        <span style="color:rgba(255,255,255,.7);font-size:.88rem">⏱ {course['duration']}</span>
        <span style="color:rgba(255,255,255,.7);font-size:.88rem">👥 {course['students']:,} students</span>
        <span style="color:rgba(255,255,255,.7);font-size:.88rem">⭐ {course['rating']}/5.0</span>
      </div>
    </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns([2,1])

    with col1:
        st.markdown("### What you'll learn")
        # Synthesize a curriculum from the course data
        sample_syllabus = {
            "Python Essentials": ["Setting up your Python environment","Variables, data types & operators","Control flow: if/else, loops","Functions & scope","Lists, dicts, sets & tuples","File I/O and error handling","Object-oriented programming","Final project: CLI app"],
            "C Programming Masterclass": ["Compilers, build systems & GCC","Variables, types & operators","Pointers and memory model","Arrays, strings & structs","Dynamic memory allocation","File I/O","Preprocessor & macros","Final project: data structures library"],
            "HTML & CSS Fundamentals": ["HTML document structure","Semantic HTML5 elements","CSS selectors & specificity","Box model & layout","Flexbox deep dive","CSS Grid","Responsive design & media queries","Final project: portfolio site"],
            "JavaScript Deep Dive": ["Variables, types & coercion","Functions & closures","The DOM & events","Asynchronous JS & Promises","Fetch API & REST","ES6+ features","Modules & bundlers","Final project: weather app"],
            "React from Zero to Hero": ["JSX & component basics","Props & state","Event handling","Hooks: useState, useEffect","React Router","Context API","Fetching data","Final project: full CRUD app"],
            "Node.js & Express API": ["Node.js runtime & npm","Express basics & routing","Middleware","REST API design","Authentication with JWT","MongoDB & Mongoose","Error handling","Final project: REST API"],
            "FastAPI & Python Backend": ["FastAPI basics & routing","Pydantic models","Path & query params","Async Python","Database with SQLAlchemy","Auth & OAuth2","Docker basics","Final project: deployed API"],
            "Database Design & SQL": ["Relational model & tables","CRUD operations","Filtering & sorting","Joins","Aggregation & GROUP BY","Indexes & performance","Transactions","Final project: multi-table schema"],
        }
        syllabus = sample_syllabus.get(course["title"], [
            "Introduction and environment setup",
            "Core concepts and fundamentals",
            "Hands-on practice exercises",
            "Intermediate techniques",
            "Advanced patterns and best practices",
            "Real-world project work",
            "Testing and debugging",
            "Final capstone project",
        ])
        for i, item in enumerate(syllabus, 1):
            st.markdown(f"""<div class="syllabus-item">
              <span style="background:var(--surface);border-radius:8px;padding:2px 8px;font-size:.8rem;font-weight:700;color:var(--accent)">{i:02d}</span>
              <span style="font-size:.92rem">{item}</span>
            </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div style="background:white;border:1.5px solid var(--border);border-radius:16px;padding:1.5rem;box-shadow:var(--shadow);position:sticky;top:80px">
          <div style="font-size:1.8rem;font-weight:900;color:var(--accent);margin-bottom:.2rem">{price_str}</div>
          <div style="color:var(--muted);font-size:.85rem;margin-bottom:1rem">{"One-time payment · lifetime access" if course['price']>0 else "Completely free · no card needed"}</div>
          <div style="font-size:.88rem;color:var(--muted);line-height:2">
            ✅ {course['duration']} of content<br>
            ✅ Hands-on projects<br>
            ✅ Certificate of completion<br>
            ✅ AI assistant support<br>
            ✅ Lifetime updates
          </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
        if st.button("🚀 Enroll Now", key="enroll", use_container_width=True):
            st.success("🎉 Enrolled! You can now access all course materials.")

        st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

        # Instructor mini-card
        teachers_data = api_get("/teachers") or []
        instructor = next((t for t in teachers_data if t["name"] == course["instructor"]), None)
        if instructor:
            st.markdown(f"""
            <div style="background:var(--surface);border-radius:12px;padding:1rem;margin-top:.5rem">
              <div style="font-size:.75rem;font-weight:700;color:var(--muted);margin-bottom:.4rem">YOUR INSTRUCTOR</div>
              <div style="display:flex;align-items:center;gap:.6rem">
                <span style="font-size:1.6rem">{instructor['avatar_emoji']}</span>
                <div>
                  <div style="font-weight:700;font-size:.9rem">{instructor['name']}</div>
                  <div style="font-size:.78rem;color:var(--muted)">{instructor['courses_count']} courses</div>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TEACHERS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "teachers":
    st.markdown('<div class="page-header"><h2>👨‍🏫 Meet Our Instructors</h2><p>Learn from experienced professionals who love teaching.</p></div>', unsafe_allow_html=True)

    teachers = api_get("/teachers") or []
    if not teachers:
        st.error("Could not load instructors."); st.stop()

    cols = st.columns(2)
    for i, t in enumerate(teachers):
        with cols[i % 2]:
            if st.button(f"{t['avatar_emoji']}  {t['name']}", key=f"t_{t['id']}", use_container_width=True):
                nav("teacher_detail", teacher_id=t["id"])
            st.markdown(f"""
            <div style="margin-top:-6px;margin-bottom:1rem;padding:0 .2rem">
              <div style="font-size:.85rem;color:var(--muted);margin-bottom:.3rem">{t['bio'][:120]}…</div>
              <div style="font-size:.8rem;color:var(--accent);font-weight:700">{t['courses_count']} courses · {t['expertise'].split(',')[0].strip()}</div>
            </div>""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# TEACHER DETAIL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "teacher_detail":
    tid = st.session_state.selected_teacher_id
    if not tid:
        nav("teachers"); st.rerun()

    teacher = api_get(f"/teachers/{tid}")
    if not teacher:
        st.error("Instructor not found."); st.stop()

    if st.button("← Back to Instructors", key="back_teachers"):
        nav("teachers"); st.rerun()

    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown(f'<div style="font-size:5rem;text-align:center;padding:1rem">{teacher["avatar_emoji"]}</div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f"## {teacher['name']}")
        st.markdown(f"<p style='color:var(--muted)'>{teacher['bio']}</p>", unsafe_allow_html=True)
        st.markdown(f"**Expertise:** {teacher['expertise']}")
        st.markdown(f"**{teacher['courses_count']}** courses on Learnify")
        st.markdown(f"📧 {teacher['email']}  ·  🐦 {teacher['twitter']}  ·  💼 {teacher['linkedin']}")

    st.markdown("---")
    st.markdown("### Courses by this instructor")
    all_courses = api_get("/courses") or []
    t_courses = [c for c in all_courses if c["instructor"] == teacher["name"]]
    if t_courses:
        cols = st.columns(min(len(t_courses), 3))
        for i, c in enumerate(t_courses):
            with cols[i % 3]:
                if st.button(f"{c['thumbnail_emoji']} {c['title']}", key=f"tc_{c['id']}", use_container_width=True):
                    nav("course_detail", course_id=c["id"])
                st.caption(f"{c['level']} · {'Free' if c['price']==0 else '$'+str(c['price'])}")


# ══════════════════════════════════════════════════════════════════════════════
# ABOUT
# ══════════════════════════════════════════════════════════════════════════════
elif page == "about":
    st.markdown('<div class="page-header"><h2>About Learnify</h2><p>Our story, our mission, and the people behind the platform.</p></div>', unsafe_allow_html=True)

    # Hero statement
    st.markdown("""
    <div style="background:linear-gradient(135deg,#6c47ff,#9b71ff);border-radius:20px;padding:2.5rem 2.5rem;color:white;margin-bottom:2rem">
      <h2 style="color:white!important;font-size:2rem;margin-bottom:.75rem">
        We believe everyone deserves a world-class programming education.
      </h2>
      <p style="color:rgba(255,255,255,.85)!important;font-size:1.05rem;max-width:680px;line-height:1.7;margin:0">
        Learnify was built by developers who remembered exactly how hard it was to learn to code —
        the confusing tutorials, the outdated documentation, the Stack Overflow rabbit holes at 2am.
        We wanted something better. So we built it.
      </p>
    </div>
    """, unsafe_allow_html=True)

    # Story
    st.markdown("### Our Story")
    st.markdown("""
    It started in late 2022 in a shared apartment in Algiers, with three engineers, two laptops, and one very strong opinion:
    online programming education was broken. Not because the knowledge wasn't out there — it was — but because it was
    scattered, inconsistent, and almost never designed with the learner's frustration in mind.

    We spent six months interviewing over 200 self-taught developers across North Africa and Europe, asking them a simple
    question: *what would have made learning to code easier for you?* The answers converged on a few themes —
    structure, feedback, relevance, and someone (or something) to ask when you're stuck at 11pm and your mentor
    is asleep.

    Learnify launched its first three courses in April 2023. Within four months we had over 500 enrolled students.
    Today we host more than 25 courses across four learning tracks, taught by instructors with decades of combined
    industry experience. We are still small, fully remote, and deeply opinionated about what good education looks like.
    """)

    st.markdown("---")

    # Stats row
    st.markdown("### By the Numbers")
    s1, s2, s3, s4, s5 = st.columns(5)
    for col, val, lab in zip([s1,s2,s3,s4,s5],
        ["25+", "4", "500+", "4.8 ★", "3"],
        ["Courses", "Expert Instructors", "Students Enrolled", "Average Rating", "Learning Tracks"]):
        with col:
            st.markdown(f'<div class="stat-card"><div class="val">{val}</div><div class="lab">{lab}</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Philosophy
    st.markdown("### Our Teaching Philosophy")
    st.markdown("""
    We have a strong point of view about how programming should be taught, and it influences every decision we make.

    **Projects over slides.** Every Learnify course ends with a real, deployable project — not a quiz, not a multiple-choice
    exam, not a certificate you print and forget. We think the most valuable thing we can give you is something you can
    actually show to an employer or a collaborator.

    **Depth over breadth.** We would rather teach one topic well than skim ten topics poorly. Our courses are longer than
    average because we don't skip the hard parts. We cover edge cases, common mistakes, debugging strategies, and
    the kind of nuance that separates a working prototype from production-ready code.

    **Accessibility without compromise.** Our beginner courses are genuinely beginner-friendly — no assumed knowledge,
    no jargon without explanation. But beginner-friendly does not mean watered-down. We trust our students to rise to
    the level we set for them, and they consistently do.

    **Learning is not a solo sport.** Even in an asynchronous, self-paced format, we believe students learn better
    when they have somewhere to turn. That's why every Learnify account includes access to Lia, our learning assistant,
    and the community forum where thousands of students ask and answer questions every day.
    """)

    st.markdown("---")

    # Values
    st.markdown("### What We Stand For")
    v1, v2, v3 = st.columns(3)
    for col, icon, title, desc in zip([v1, v2, v3],
        ["🎯", "🤝", "🔬"],
        ["Quality Without Compromise", "Student-Centered Always", "Honest & Transparent"],
        [
            "Every course goes through a rigorous editorial review before it's published. "
            "Instructors revise until the bar is met — no exceptions.",
            "We measure our success by your outcomes, not our content library size. "
            "If a course isn't helping people learn, we pull it and rework it.",
            "We tell you exactly what a course covers, how long it takes, and what level "
            "you need to be to benefit from it. No inflated promises.",
        ]):
        with col:
            st.markdown(f"""
            <div class="feature-card" style="height:100%">
              <div class="feature-icon">{icon}</div>
              <strong>{title}</strong>
              <p style="color:var(--muted);font-size:.88rem;margin:.4rem 0 0;line-height:1.6">{desc}</p>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.markdown("---")

    # Instructors teaser
    st.markdown("### Our Instructors")
    st.markdown("""
    We are extremely selective about who teaches on Learnify. Every instructor on the platform has passed a multi-stage
    review process that evaluates not just their technical depth, but their ability to explain things clearly to someone
    who doesn't already know them. That second part is surprisingly rare.

    Our current instructors bring experience from Google, embedded systems engineering, Y-Combinator-backed startups,
    and professional security research. They have published open-source libraries, spoken at international conferences,
    and — most importantly — they know how to teach.

    You can browse all instructor profiles on the [Instructors](#) page.
    """)

    st.markdown("---")

    # Platform features — subtle AI mentions
    st.markdown("### Platform Features")
    st.markdown("""
    Learnify is more than a video library. We have built several tools around the course content to support your
    learning at every stage.

    **Structured Learning Tracks** group courses into coherent paths — Programming Fundamentals, Frontend Development,
    Backend Development, and Low-Level Programming — so you always know what to study next and why.

    **The course search** lets you describe what you're looking for in plain language and surfaces the most relevant
    results across our entire catalog, making it easy to find exactly the right course even if you don't know the
    precise terminology yet.

    **Lia**, our learning assistant, is available on every page to answer quick questions between lessons — whether
    that's a syntax question, a concept you want explained differently, or just a recommendation for what to study next.

    **The code reviewer** is a tool available to all enrolled students. Upload a Python script and receive structured
    feedback on issues found, suggested improvements, and best practices — useful for assignments, personal projects,
    or just double-checking your work before sharing it.

    These tools are designed to feel like having a knowledgeable friend available at any hour, not a replacement
    for the deep work of actually learning.
    """)

    st.markdown("---")

    # Roadmap
    st.markdown("### What's Coming")
    st.markdown("""
    We're actively developing new content and platform features. On the course side, we have several tracks in
    preparation including Rust systems programming, DevOps and CI/CD, and an advanced low-level programming sequence
    covering assembly, operating systems internals, and embedded C. These will roll out progressively over the
    next two quarters.

    On the platform side, we are working on collaborative exercises, peer code review, and a structured project
    submission system with instructor feedback. We are also expanding our community features to make it easier
    to connect with other learners at the same stage of their journey.

    If you have suggestions, we genuinely read every email at **hello@learnify.io**.
    """)

    st.markdown("---")

    # Team
    st.markdown("### The Team")
    st.markdown("""
    Learnify is built and run by a small, fully remote team spread across Algeria, France, and the United Kingdom.
    We are a mix of engineers, educators, and designers who share one conviction: that the gap between
    "I want to learn to code" and "I can build things professionally" is smaller than most people think,
    and that the right learning environment can close it faster than almost anything else.

    We're hiring. If you care about education and you can build things, we'd love to talk.
    Send a note to **team@learnify.io**.
    """)


# ══════════════════════════════════════════════════════════════════════════════
# CHATBOT  (strict one-turn — zero memory, UI resets on every send)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "chatbot":
    st.markdown(
        '<div class="page-header"><h2>🤖 Lia — Your Learning Assistant</h2>'
        '<p>Ask me anything about programming, courses, or your learning journey.</p></div>',
        unsafe_allow_html=True,
    )

    if not st.session_state.api_key:
        st.markdown("""<div class="api-key-banner">
          🔑 <span><strong>API key required</strong> — Go to <em>Settings</em> to add your Gemini API key.</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to Settings →"): nav("settings"); st.rerun()
        st.stop()

    # Single-exchange state — replaced entirely on every submit
    if "lia_prompt" not in st.session_state:
        st.session_state.lia_prompt = ""
    if "lia_reply" not in st.session_state:
        st.session_state.lia_reply = ""

    # ── Input form (clears itself after submit) ───────────────────────────────
    with st.form("lia_form", clear_on_submit=True):
        user_msg = st.text_input(
            "lia_input",
            placeholder="Type your question and press Ask…",
            label_visibility="collapsed",
        )
        cols = st.columns([5, 1])
        with cols[1]:
            sent = st.form_submit_button("Ask →", use_container_width=True)

    if sent and user_msg.strip():
        # Hard reset — wipe previous prompt & reply before making the new call
        st.session_state.lia_prompt = user_msg.strip()
        st.session_state.lia_reply  = ""
        with st.spinner("Lia is thinking…"):
            resp = api_post("/chat", {
                "api_key": st.session_state.api_key,
                "message": st.session_state.lia_prompt,
            })
            st.session_state.lia_reply = (
                resp.get("response")
                or resp.get("detail", "Something went wrong. Please try again.")
            )
        st.rerun()

    # ── Display area ──────────────────────────────────────────────────────────
    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)

    if st.session_state.lia_prompt:
        # Show the single current exchange (user → Lia)
        st.markdown(
            f'<div class="chat-bubble-user">'
            f'<div class="chat-meta">You</div>'
            f'{st.session_state.lia_prompt}'
            f'</div>',
            unsafe_allow_html=True,
        )
        if st.session_state.lia_reply:
            st.markdown(
                f'<div class="chat-bubble-bot">'
                f'<div class="chat-meta">🤖 Lia</div>'
                f'{st.session_state.lia_reply}'
                f'</div>',
                unsafe_allow_html=True,
            )
    else:
        # Welcome state — shown before the first question
        st.markdown(
            '<div class="chat-bubble-bot">'
            '<div class="chat-meta">🤖 Lia</div>'
            "Hi! I'm Lia, your Learnify learning assistant. "
            "Type a question above and I'll do my best to help. 😊"
            "</div>",
            unsafe_allow_html=True,
        )

    # ── New question button — explicitly resets state ─────────────────────────
    if st.session_state.lia_prompt:
        st.markdown("<div style='height:.75rem'></div>", unsafe_allow_html=True)
        if st.button("🔄 Ask a new question"):
            st.session_state.lia_prompt = ""
            st.session_state.lia_reply  = ""
            st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# CODE REVIEW (hidden feature — accessible via direct navigation)
# ══════════════════════════════════════════════════════════════════════════════
elif page == "code_review":
    st.markdown('<div class="page-header"><h2>🛠️ Python Code Review</h2><p>Upload your Python file and get instant feedback from our senior instructor AI.</p></div>', unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.markdown("""<div class="api-key-banner">
          🔑 <span><strong>API key required</strong> — add your Gemini API key in Settings to use Code Review.</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Go to Settings →"): nav("settings"); st.rerun()
        st.stop()

    uploaded = st.file_uploader("Upload a Python file (.py)", type=["py"])

    source = ""
    fname = "script.py"
    if uploaded:
        source = uploaded.read().decode("utf-8", errors="replace")
        fname = uploaded.name
        st.code(source[:1500] + ("…" if len(source) > 1500 else ""), language="python")

    if source and st.button("🔍 Review My Code", use_container_width=True):
        with st.spinner("Analysing your code…"):
            resp = api_post("/review-code", {"api_key": st.session_state.api_key, "code": source, "filename": fname})
            if "feedback" in resp:
                st.markdown("### 📋 Feedback")
                st.markdown(f'<div class="code-output">{resp["feedback"]}</div>', unsafe_allow_html=True)
            elif "detail" in resp:
                st.error(resp["detail"])


# ══════════════════════════════════════════════════════════════════════════════
# SETTINGS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "settings":
    st.markdown('<div class="page-header"><h2>⚙️ Settings</h2><p>Configure your Learnify experience.</p></div>', unsafe_allow_html=True)

    st.markdown("### 🔑 Gemini API Key")
    st.markdown("""
    Learnify uses Google Gemini to power the AI assistant, code reviewer, and smart search.
    Your key is held in this browser session and sent to the Learnify backend with each
    request so it can call Gemini on your behalf. It is never stored on disk.

    Get a free key at [aistudio.google.com](https://aistudio.google.com) (free tier available).
    """)

    new_key = st.text_input(
        "Your Gemini API key",
        value=st.session_state.api_key,
        type="password",
        placeholder="AIza...",
    )

    c1, c2 = st.columns([1,4])
    with c1:
        if st.button("Save Key", use_container_width=True):
            st.session_state.api_key = new_key.strip()
            if st.session_state.api_key:
                st.success("✅ API key saved for this session.")
            else:
                st.info("API key cleared.")

    st.markdown("---")
    st.markdown("### 🛠️ Developer Tools")
    st.markdown("These tools are available to logged-in users:")

    t1, t2 = st.columns(2)
    with t1:
        st.markdown("""<div class="feature-card">
          <div class="feature-icon">🔧</div>
          <strong>Python Code Review</strong>
          <p style="color:var(--muted);font-size:.88rem;margin:.3rem 0 .6rem">Upload a .py file and get detailed feedback.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Open Code Review →", key="open_cr"):
            nav("code_review"); st.rerun()

    with t2:
        st.markdown("""<div class="feature-card">
          <div class="feature-icon">🔍</div>
          <strong>AI-Powered Search</strong>
          <p style="color:var(--muted);font-size:.88rem;margin:.3rem 0 .6rem">Smart course search using natural language.</p>
        </div>""", unsafe_allow_html=True)
        if st.button("Search Courses →", key="open_search"):
            nav("search"); st.rerun()

    st.markdown("---")
    st.caption("Learnify v2.0 · Built with FastAPI & Streamlit")

# ══════════════════════════════════════════════════════════════════════════════
# SEARCH RESULTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "search":
    q = st.session_state.search_query

    st.markdown(f"""
    <div class="search-hero">
      <h2>🔍 Search Results</h2>
      <p>AI-powered search across all courses and instructors</p>
    </div>
    """, unsafe_allow_html=True)

    # Search bar at the top so users can refine
    s1, s2 = st.columns([5, 1])
    with s1:
        new_q = st.text_input("refine_search", value=q, label_visibility="collapsed", placeholder="Refine your search…")
    with s2:
        refine_btn = st.button("Search", key="refine_search_btn", use_container_width=True)

    if refine_btn and new_q.strip() and new_q.strip() != q:
        st.session_state.search_query = new_q.strip()
        st.session_state.search_results = None
        st.rerun()

    if not st.session_state.api_key:
        st.markdown("""<div class="api-key-banner">
          🔑 <span><strong>API key required</strong> — Go to <em>Settings</em> to add your Gemini API key.</span>
        </div>""", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 5])
        with c1:
            if st.button("Settings →"): nav("settings"); st.rerun()
        st.stop()

    # Fetch results if not yet cached for this query
    if st.session_state.search_results is None or st.session_state.search_results.get("_query") != q:
        with st.spinner(f'Searching for "{q}"…'):
            raw = api_post("/search", {"api_key": st.session_state.api_key, "query": q})
            raw["_query"] = q
            st.session_state.search_results = raw

    res = st.session_state.search_results
    if not res:
        st.error("Search failed. Please check your API key and try again.")
        st.stop()

    # Handle API errors
    if "detail" in res:
        st.error(f"Error: {res['detail']}")
        st.stop()

    # If backend fell back to raw text (JSON parse failed)
    if "raw" in res and not res.get("courses") and not res.get("teachers"):
        st.markdown(f'<div class="search-summary">💬 {res.get("summary","Results:")}</div>', unsafe_allow_html=True)
        st.markdown(res["raw"])
        if st.button("← Back"): nav("courses"); st.rerun()
        st.stop()

    summary   = res.get("summary", "")
    courses   = res.get("courses", [])
    teachers  = res.get("teachers", [])
    total     = len(courses) + len(teachers)

    # Summary bar
    if summary:
        st.markdown(f'<div class="search-summary">✨ {summary}</div>', unsafe_allow_html=True)

    if total == 0:
        st.markdown("""
        <div class="search-no-results">
          <div class="icon">🔍</div>
          <strong>No results found</strong><br>
          <span>Try different keywords, or browse all courses below.</span>
        </div>""", unsafe_allow_html=True)
        if st.button("Browse all courses →"): nav("courses"); st.rerun()
        st.stop()

    level_cls_map = {
        "Beginner": "badge-beginner", "Intermediate": "badge-intermediate",
        "Advanced": "badge-advanced", "Expert": "badge-expert",
    }

    # ── Course results ────────────────────────────────────────────────────────
    if courses:
        st.markdown(f'<div class="result-section-title">📚 Courses &nbsp;·&nbsp; {len(courses)} found</div>', unsafe_allow_html=True)
        for c in courses:
            price_str   = "Free" if c.get("price", 0) == 0 else f"${c['price']:.2f}"
            level       = c.get("level", "")
            level_cls   = level_cls_map.get(level, "badge-intermediate")
            reason      = c.get("match_reason", "")
            emoji       = c.get("thumbnail_emoji", "📘")
            instructor  = c.get("instructor", "")
            duration    = c.get("duration", "")
            rating      = c.get("rating", 0)
            students    = c.get("students", 0)
            cid         = c.get("id")

            # Clickable card via button (overlaid visually)
            btn_key = f"sr_course_{cid}_{c.get('title','')[:10]}"
            col_card, col_btn = st.columns([10, 1])
            with col_card:
                st.markdown(f"""
                <div class="search-course-card">
                  <div class="search-card-emoji">{emoji}</div>
                  <div class="search-card-body">
                    <div class="search-card-title">{c.get('title','')}</div>
                    <div class="search-card-meta">
                      👨‍🏫 {instructor} &nbsp;·&nbsp;
                      <span class="badge {level_cls}">{level}</span> &nbsp;·&nbsp;
                      ⏱ {duration} &nbsp;·&nbsp;
                      👥 {students:,} students &nbsp;·&nbsp;
                      ⭐ {rating}
                    </div>
                    {f'<div class="search-card-reason">✦ {reason}</div>' if reason else ''}
                  </div>
                  <div class="search-card-price">{price_str}</div>
                </div>""", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:60px'></div>", unsafe_allow_html=True)
                if st.button("View →", key=btn_key, use_container_width=True) and cid:
                    nav("course_detail", course_id=cid)
                    st.rerun()

    # ── Teacher results ───────────────────────────────────────────────────────
    if teachers:
        st.markdown(f'<div class="result-section-title">👨‍🏫 Instructors &nbsp;·&nbsp; {len(teachers)} found</div>', unsafe_allow_html=True)
        for t in teachers:
            reason      = t.get("match_reason", "")
            avatar      = t.get("avatar_emoji", "👤")
            expertise   = t.get("expertise", "")
            n_courses   = t.get("courses_count", 0)
            tid         = t.get("id")

            col_card, col_btn = st.columns([10, 1])
            with col_card:
                st.markdown(f"""
                <div class="search-teacher-card">
                  <span style="font-size:2.2rem;flex-shrink:0">{avatar}</span>
                  <div style="flex:1;min-width:0">
                    <div class="search-card-title">{t.get('name','')}</div>
                    <div class="search-card-meta">{expertise}</div>
                    <div class="search-card-meta">{n_courses} courses on Learnify</div>
                    {f'<div class="search-card-reason">✦ {reason}</div>' if reason else ''}
                  </div>
                </div>""", unsafe_allow_html=True)
            with col_btn:
                st.markdown("<div style='height:50px'></div>", unsafe_allow_html=True)
                if st.button("View →", key=f"sr_teacher_{tid}", use_container_width=True) and tid:
                    nav("teacher_detail", teacher_id=tid)
                    st.rerun()

    st.markdown("<div style='height:.5rem'></div>", unsafe_allow_html=True)
    if st.button("← Browse all courses"):
        nav("courses"); st.rerun()


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer-strip">
  © 2026 Learnify · <a href="#" style="color:rgba(255,255,255,.5)">Terms</a> · <a href="#" style="color:rgba(255,255,255,.5)">Privacy</a> · hello@learnify.io
</div>
""", unsafe_allow_html=True)