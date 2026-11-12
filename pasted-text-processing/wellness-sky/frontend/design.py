"""Wellness Sky design system."""

import streamlit as st
import streamlit.components.v1 as components

COLORS = {
    "ink": "#17324D",
    "muted": "#5C7184",
    "sky": "#DDF3F5",
    "lavender": "#EEE8FA",
    "mint": "#E7F5EE",
    "coral": "#FDE9E4",
    "gold": "#F5C96B",
    "surface": "#FFFFFF",
    "background": "#F7FAFC",
}


def apply_design() -> None:
    theme = st.session_state.get("theme", "Sky")
    palettes = {
        "Sky": (
            "#EEF7FA", "#FFFFFF", "#17324D", "#5B78C6", "#DDF3F5", "#EEE8FA",
            "https://images.unsplash.com/photo-1470770841072-f978cf4d019e?auto=format&fit=crop&w=2400&q=85",
        ),
        "Lavender": (
            "#F8F3FF", "#FFFFFF", "#2B2142", "#8A62C9", "#F0E7FF", "#FFEAF4",
            "https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=2400&q=85",
        ),
        "Amber": (
            "#EAF1F5", "#FFFFFF", "#102235", "#2457A6", "#D8F3F0", "#FFF0C7",
            "https://images.unsplash.com/photo-1500534623283-312aade485b7?auto=format&fit=crop&w=2400&q=85",
        ),
    }
    background, surface, ink, accent, sky, lavender, background_image = palettes.get(theme, palettes["Sky"])
    st.markdown(
        f"""<style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Space+Mono:wght@400;700&display=swap');
        :root {{ --ink:{ink}; --muted:#5C7184; --sky:{sky}; --lav:{lavender}; --accent:{accent}; --surface:{surface}; }}
        html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {{ min-height:100%; overflow-y:auto !important; }}
        .stApp {{ background:transparent; color:var(--ink); overflow:visible !important; }}
        .stApp::before {{ content:""; position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.92;
          background-image:linear-gradient(180deg, rgba(4,12,16,.02), rgba(9,17,20,.10) 84%), url("{background_image}");
          background-size:cover; background-position:center; filter:saturate(1.12) contrast(1.04); animation:slow-pan 24s ease-in-out infinite alternate; }}
        .stApp::after {{ content:""; position:fixed; inset:0; z-index:0; pointer-events:none;
          background:radial-gradient(circle at 18% 22%, rgba(52,221,202,.10), transparent 25%),
          radial-gradient(circle at 82% 55%, rgba(135,91,224,.15), transparent 30%),
          linear-gradient(180deg, rgba(5,12,16,.03), rgba(5,10,14,.08)); }}
        [data-testid="stAppViewContainer"], [data-testid="stHeader"] {{ position:relative; z-index:1; }}
        [data-testid="stSidebar"] {{ background:linear-gradient(180deg, rgba(8,19,24,.98), rgba(11,26,32,.96)); border-right:1px solid rgba(79,222,202,.35); backdrop-filter:blur(20px); }}
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {{ color:#F4F7F1 !important; }}
        [data-testid="stSidebarNav"] a, [data-testid="stSidebarNav"] span, [data-testid="stSidebarNav"] p {{ color:#F4F7F1 !important; opacity:1 !important; }}
        [data-testid="stSidebarNav"] a {{ background:rgba(255,255,255,.06); border:1px solid transparent; }}
        [data-testid="stSidebarNav"] a[aria-current="page"] {{ background:linear-gradient(90deg, rgba(72,218,197,.30), rgba(128,91,180,.28)); border-color:rgba(125,236,215,.48); }}
        .block-container {{ padding-top:2.5rem; padding-bottom:4rem; max-width:1200px; }}
        h1,h2,h3 {{ color:#F3F4EC; letter-spacing:-.035em; font-family:Fraunces, Georgia, serif; text-shadow:0 3px 20px rgba(0,0,0,.32); }}
        h1 {{ font-size:clamp(2.4rem,5vw,4.2rem) !important; }}
        p, label, button, input, textarea, [data-testid="stMarkdownContainer"] {{ font-family:'DM Sans',sans-serif; color:#F4F7F1; text-shadow:0 1px 3px rgba(0,0,0,.72); }}
        input, textarea, [data-baseweb="select"] * {{ text-shadow:none !important; color:#111827 !important; -webkit-text-fill-color:#111827; }}
        .hero {{ position:relative; overflow:hidden; min-height:270px; display:flex; flex-direction:column; justify-content:center;
          border-radius:12px; padding:3rem; background:linear-gradient(110deg, rgba(6,23,29,.30), rgba(34,30,55,.26)),
          url("{background_image}") center/cover; margin-bottom:1.8rem; border:1px solid rgba(255,255,255,.24);
          box-shadow:0 20px 55px rgba(0,0,0,.14), inset 0 1px rgba(255,255,255,.18); backdrop-filter:blur(5px); animation:float-in .65s ease-out both; }}
        .hero:before, .hero:after {{ content:""; position:absolute; border-radius:50%; pointer-events:none; opacity:.5; }}
        .hero:before {{ width:180px; height:180px; right:-40px; top:-70px; background:#FFD98A; filter:blur(2px); animation: drift 8s ease-in-out infinite; }}
        .hero:after {{ width:90px; height:90px; right:115px; bottom:-48px; background:#FFFFFF; box-shadow:40px 10px #FFFFFF, 76px 2px #FFFFFF; }}
        .hero h1 {{ position:relative; z-index:1; margin:0 0 .4rem; text-shadow:0 3px 12px rgba(0,0,0,.55); }}
        .hero p, .hero .eyebrow {{ position:relative; z-index:1; }}
        .card {{ background:linear-gradient(145deg, rgba(20,48,53,.38), rgba(28,29,53,.34)); border:1px solid rgba(255,255,255,.20); border-radius:10px; padding:1.35rem;
                height:100%; box-shadow:0 14px 35px rgba(0,0,0,.14), inset 0 1px rgba(255,255,255,.12); backdrop-filter:blur(5px) saturate(1.2); transition:transform .3s ease, box-shadow .3s ease; animation:float-in .5s ease-out both; }}
        .card:hover {{ transform:translateY(-7px) rotate(.3deg); box-shadow:0 22px 40px rgba(42,219,196,.16); }}
        .eyebrow {{ color:#82E4D2; text-transform:uppercase; font-family:'Space Mono',monospace; font-weight:700; font-size:.7rem; letter-spacing:.13em; }}
        .metric {{ font-size:2rem; font-weight:800; color:#F3F4EC; }}
        .safety {{ background:rgba(89,65,41,.38); border:1px solid rgba(255,213,147,.45); border-radius:10px; padding:1rem; backdrop-filter:blur(5px); }}
        .tag {{ background:rgba(137,105,192,.35); border:1px solid rgba(255,255,255,.18); border-radius:4px; padding:.25rem .65rem; margin-right:.25rem; font-size:.8rem; }}
        [data-testid="stButton"] button, [data-testid="stFormSubmitButton"] button, [data-testid="stDownloadButton"] button {{ border-radius:4px; border:1px solid rgba(119,224,205,.65); background:linear-gradient(135deg, #315C61, #735B82); color:#F4F7F1 !important; font-weight:700; transition:transform .2s ease, box-shadow .2s ease; }}
        [data-testid="stButton"] button:hover, [data-testid="stFormSubmitButton"] button:hover, [data-testid="stDownloadButton"] button:hover {{ transform:translateY(-2px); box-shadow:0 8px 18px color-mix(in srgb, var(--accent) 25%, transparent); }}
        [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {{ border-radius:6px; background:rgba(20,48,53,.72); color:#111827 !important; -webkit-text-fill-color:#111827; caret-color:#111827; border:1px solid rgba(255,255,255,.20); box-shadow:inset 0 1px rgba(255,255,255,.12); backdrop-filter:blur(5px); }}
        [data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder {{ color:rgba(244,247,241,.68); -webkit-text-fill-color:rgba(244,247,241,.68); }}
        [data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {{ border-color:#82E4D2; outline:none; }}
        [data-testid="stSelectbox"] [data-baseweb="select"], [data-testid="stMultiSelect"] [data-baseweb="select"] {{ border-radius:6px; background:rgba(20,48,53,.72); color:#F3F4EC; border:1px solid rgba(255,255,255,.20); box-shadow:inset 0 1px rgba(255,255,255,.12); backdrop-filter:blur(5px); }}
        [data-testid="stSelectbox"] [data-baseweb="select"] > div, [data-testid="stMultiSelect"] [data-baseweb="select"] > div {{ border:0 !important; background:transparent !important; }}
        [data-testid="stSelectbox"] label, [data-testid="stMultiSelect"] label {{ border:0 !important; background:transparent !important; }}
        [data-testid="stSelectbox"] svg, [data-testid="stMultiSelect"] svg {{ fill:#F4F7F1; }}
        [data-testid="stButton"] button[kind="secondary"] {{ background:transparent; border:0; color:#B8F4E8 !important; box-shadow:none; text-decoration:underline; font-weight:500; }}
        [data-testid="stButton"] button[kind="secondary"]:hover {{ background:transparent; box-shadow:none; transform:none; color:#F5C96B !important; }}
        [data-testid="stSlider"] [role="slider"] {{ background:#82E4D2; }}
        [data-testid="stMetric"] {{ background:rgba(13,32,38,.34); border-radius:8px; padding:1rem; border:1px solid rgba(255,255,255,.18); backdrop-filter:blur(5px); }}
        [data-testid="stIFrame"] {{ position:fixed !important; right:18px !important; bottom:18px !important; width:48px !important; height:48px !important; z-index:9999 !important; background:transparent !important; border:0 !important; }}
        [data-testid="stSidebarNav"] {{ padding-top:1rem; }}
        [data-testid="stSidebarNav"] li {{ border-radius:14px; margin:.2rem 0; transition:transform .2s ease, background .2s ease; }}
        [data-testid="stSidebarNav"] li:hover {{ transform:translateX(5px); background:var(--lav); }}
        .stProgress > div > div {{ background:linear-gradient(90deg, var(--accent), #F4B6D2); }}
        .stCaption {{ color:var(--muted); }}
        @keyframes float-in {{ from {{ opacity:0; transform:translateY(12px); }} to {{ opacity:1; transform:translateY(0); }} }}
        @keyframes drift {{ 0%,100% {{ transform:translate(0,0) rotate(0deg); }} 50% {{ transform:translate(-18px,12px) rotate(8deg); }} }}
        @keyframes slow-pan {{ from {{ background-position:48% 45%; }} to {{ background-position:53% 55%; }} }}
        @media (prefers-reduced-motion: reduce) {{ *, *:before, *:after {{ animation-duration:.01ms !important; transition-duration:.01ms !important; }} }}
        </style>""",
        unsafe_allow_html=True,
    )


def card(title: str, body: str, tone: str = "surface") -> None:
    color = COLORS.get(tone, COLORS["surface"])
    st.markdown(f'<div class="card" style="background:{color}"><div class="eyebrow">{title}</div><p>{body}</p></div>', unsafe_allow_html=True)


def safety_panel() -> None:
    st.markdown(
        '<div class="safety"><strong>Need urgent support?</strong><br>'
        "If you may be in immediate danger, call local emergency services. "
        'In the US or Canada, call or text <strong>988</strong>.</div>',
        unsafe_allow_html=True,
    )


def music_moment() -> None:
    """Render a tiny fixed speaker toggle with a browser-safe fallback."""
    if not st.session_state.get("sound_enabled", True):
        return
    components.html(
        """<style>
        html, body { margin:0; padding:0; overflow:hidden; background:transparent; }
        #wellness-ambience { position:fixed; inset:0; display:flex; align-items:center; justify-content:center; }
        #volume-toggle { border:1px solid rgba(255,255,255,.9); border-radius:50%; width:40px; height:40px;
          background:rgba(10,27,32,.90); cursor:pointer; box-shadow:0 7px 18px rgba(0,0,0,.30);
          color:#F4F7F1; font-size:17px; }
        #volume-toggle:hover { transform:scale(1.08); }
        </style>
        <div id="wellness-ambience">
          <button id="volume-toggle" aria-label="Mute or unmute ambient music">🔊</button>
        </div>
        <audio id="ambient-audio" loop preload="none">
          <!-- Free-to-stream instrumental source; playback starts after a user gesture when required. -->
          <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3" type="audio/mpeg">
        </audio>
        <script>
        const volume = document.getElementById("volume-toggle");
        const audio = document.getElementById("ambient-audio");
        let muted = false, started = false;
        audio.volume = .08;
        volume.onclick = () => {
          if (!started) { audio.play().catch(() => {}); started = true; }
          muted = !muted; audio.muted = muted; volume.textContent = muted ? "🔇" : "🔊";
        };
        audio.play().then(() => { started = true; }).catch(() => {});
        </script>""",
        height=48,
    )
