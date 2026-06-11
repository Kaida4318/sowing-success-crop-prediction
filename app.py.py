import streamlit as st
import pandas as pd
import joblib

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sowing Success · Crop AI",
    page_icon="🌾",
    layout="centered",
)

# ── Google Fonts + Custom CSS ─────────────────────────────────────────────────
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">

<style>
/* ─── Root palette ─────────────────────────────────── */
:root {
    --forest:   #1A3C2A;
    --forest-m: #234D37;
    --sage:     #7A9E7E;
    --amber:    #D4A017;
    --amber-lt: #F0C84A;
    --parch:    #F5EDDA;
    --parch-d:  #EDE0C4;
    --white:    #FFFFFF;
    --ink:      #1C1C1C;
    --muted:    #6B7B6E;
    --card-bg:  rgba(255,255,255,0.06);
    --card-bd:  rgba(255,255,255,0.12);
    --radius:   16px;
}

/* ─── App shell ────────────────────────────────────── */
.stApp {
    background: linear-gradient(160deg, #0F2318 0%, #1A3C2A 45%, #1F4730 100%);
    min-height: 100vh;
    font-family: 'Inter', sans-serif;
}

/* remove default streamlit padding */
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 4rem !important;
    max-width: 720px !important;
}

/* ─── Hero header ──────────────────────────────────── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero-icon {
    font-size: 3.2rem;
    display: block;
    margin-bottom: 0.6rem;
    filter: drop-shadow(0 4px 12px rgba(212,160,23,0.5));
    animation: float 4s ease-in-out infinite;
}
@keyframes float {
    0%, 100% { transform: translateY(0); }
    50%       { transform: translateY(-6px); }
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3rem;
    font-weight: 700;
    color: var(--parch);
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin: 0 0 0.4rem;
}
.hero-title span {
    color: var(--amber);
}
.hero-sub {
    font-size: 1rem;
    font-weight: 300;
    color: var(--sage);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.hero-desc {
    font-size: 0.95rem;
    color: var(--parch);
    opacity: 0.7;
    max-width: 440px;
    margin: 0 auto;
    line-height: 1.6;
}

/* ─── Form card ────────────────────────────────────── */
.form-card {
    background: var(--card-bg);
    border: 1px solid var(--card-bd);
    border-radius: var(--radius);
    padding: 2rem 2.2rem 2.2rem;
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
    box-shadow: 0 8px 40px rgba(0,0,0,0.25);
}
.form-card-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.15rem;
    color: var(--amber);
    margin-bottom: 1.4rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.form-card-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--card-bd);
    margin-left: 0.5rem;
}

/* ─── Streamlit input overrides ────────────────────── */
div[data-testid="stNumberInput"] label,
div[data-testid="stTextInput"]  label {
    color: var(--parch) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    margin-bottom: 4px !important;
}
div[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.07) !important;
    border: 1px solid rgba(255,255,255,0.18) !important;
    border-radius: 10px !important;
    color: var(--parch) !important;
    font-size: 1rem !important;
    padding: 0.6rem 0.9rem !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--amber) !important;
    box-shadow: 0 0 0 3px rgba(212,160,23,0.18) !important;
    outline: none !important;
}

/* helper text below inputs */
.input-hint {
    font-size: 0.75rem;
    color: var(--sage);
    margin-top: -0.3rem;
    margin-bottom: 0.8rem;
    opacity: 0.85;
}

/* ─── Predict button ───────────────────────────────── */
div[data-testid="stButton"] > button {
    width: 100% !important;
    background: linear-gradient(135deg, var(--amber) 0%, #B8880E 100%) !important;
    color: #1A1A1A !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.04em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 1.5rem !important;
    margin-top: 1rem !important;
    cursor: pointer !important;
    box-shadow: 0 4px 18px rgba(212,160,23,0.35) !important;
    transition: transform 0.15s, box-shadow 0.15s !important;
}
div[data-testid="stButton"] > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(212,160,23,0.5) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0) !important;
}

/* ─── Result card ──────────────────────────────────── */
.result-card {
    background: linear-gradient(135deg, rgba(212,160,23,0.15) 0%, rgba(122,158,126,0.10) 100%);
    border: 1px solid rgba(212,160,23,0.4);
    border-radius: var(--radius);
    padding: 1.6rem 2rem;
    text-align: center;
    margin-top: 0.5rem;
    animation: bloom 0.45s cubic-bezier(.22,.97,.46,1.1) both;
}
@keyframes bloom {
    0%   { opacity: 0; transform: scale(0.92) translateY(10px); }
    100% { opacity: 1; transform: scale(1)    translateY(0); }
}
.result-label {
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--sage);
    margin-bottom: 0.4rem;
}
.result-crop {
    font-family: 'Playfair Display', serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: var(--amber-lt);
    margin-bottom: 0.3rem;
    text-shadow: 0 2px 12px rgba(212,160,23,0.3);
}
.result-conf {
    font-size: 0.9rem;
    color: var(--parch);
    opacity: 0.75;
    margin-top: 0.4rem;
}
.conf-bar-wrap {
    background: rgba(255,255,255,0.1);
    border-radius: 99px;
    height: 6px;
    margin: 0.6rem auto 0;
    max-width: 260px;
    overflow: hidden;
}
.conf-bar-fill {
    height: 6px;
    border-radius: 99px;
    background: linear-gradient(90deg, var(--sage), var(--amber));
    transition: width 0.8s ease;
}

/* ─── Model stats strip ────────────────────────────── */
.stats-strip {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 0.8rem;
    margin: 2rem 0 1rem;
}
.stat-box {
    background: var(--card-bg);
    border: 1px solid var(--card-bd);
    border-radius: 12px;
    padding: 1rem 0.5rem;
    text-align: center;
    backdrop-filter: blur(8px);
}
.stat-val {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--amber);
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-key {
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--sage);
}

/* ─── About section ────────────────────────────────── */
.about-card {
    background: var(--card-bg);
    border: 1px solid var(--card-bd);
    border-radius: var(--radius);
    padding: 1.8rem 2.2rem;
    backdrop-filter: blur(10px);
    margin-top: 0.5rem;
}
.about-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    color: var(--parch);
    margin-bottom: 1rem;
}
.insight-box {
    background: rgba(212,160,23,0.1);
    border-left: 3px solid var(--amber);
    border-radius: 0 8px 8px 0;
    padding: 0.9rem 1.1rem;
    margin-top: 1.2rem;
}
.insight-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 0.3rem;
}
.insight-text {
    font-size: 0.9rem;
    color: var(--parch);
    opacity: 0.85;
    line-height: 1.55;
}
.about-list {
    list-style: none;
    padding: 0;
    margin: 0;
}
.about-list li {
    font-size: 0.875rem;
    color: var(--parch);
    opacity: 0.8;
    padding: 0.3rem 0;
    display: flex;
    align-items: baseline;
    gap: 0.6rem;
    line-height: 1.5;
}
.about-list li::before {
    content: '·';
    color: var(--amber);
    font-size: 1.3rem;
    flex-shrink: 0;
}

/* ─── Footer ───────────────────────────────────────── */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-size: 0.78rem;
    color: var(--muted);
    letter-spacing: 0.04em;
}

/* ─── Hide default streamlit chrome ────────────────── */
#MainMenu, footer, header { visibility: hidden; }
div[data-testid="stDecoration"] { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Load model & scaler ───────────────────────────────────────────────────────
@st.cache_resource
def load_artifacts():
    model  = joblib.load("crop_svm_model.pkl")
    scaler = joblib.load("crop_scaler.pkl")
    return model, scaler

model, scaler = load_artifacts()


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <span class="hero-icon">🌾</span>
  <p class="hero-sub">AI-Powered Agriculture</p>
  <h1 class="hero-title">Sowing <span>Success</span></h1>
  <p class="hero-desc">
    Enter your soil's nutrient profile and receive an instant, 
    AI-driven crop recommendation.
  </p>
</div>
""", unsafe_allow_html=True)


# ── Input form ────────────────────────────────────────────────────────────────
st.markdown('<div class="form-card"><div class="form-card-title">🧪 Soil Analysis Inputs</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    N = st.number_input("Nitrogen (N)", min_value=0.0, max_value=500.0, value=50.0, step=1.0)
    st.markdown('<p class="input-hint">Typical range: 0 – 140 kg/ha</p>', unsafe_allow_html=True)
    K = st.number_input("Potassium (K)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    st.markdown('<p class="input-hint">Strongest predictor of crop type</p>', unsafe_allow_html=True)
with col2:
    P = st.number_input("Phosphorus (P)", min_value=0.0, max_value=500.0, value=30.0, step=1.0)
    st.markdown('<p class="input-hint">Typical range: 5 – 145 kg/ha</p>', unsafe_allow_html=True)
    ph = st.number_input("pH Level", min_value=0.0, max_value=14.0, value=6.5, step=0.1)
    st.markdown('<p class="input-hint">Optimal range: 5.5 – 7.5</p>', unsafe_allow_html=True)

predict_clicked = st.button("🌱 Analyse Soil & Recommend Crop")
st.markdown('</div>', unsafe_allow_html=True)


# ── Prediction output ─────────────────────────────────────────────────────────
if predict_clicked:
    input_df     = pd.DataFrame([[N, P, K, ph]], columns=["N", "P", "K", "ph"])
    scaled_input = scaler.transform(input_df)
    prediction   = model.predict(scaled_input)[0]

    conf_html = ""
    if hasattr(model, "predict_proba"):
        confidence = model.predict_proba(scaled_input).max() * 100
        conf_html = f"""
        <p class="result-conf">Confidence: <strong>{confidence:.1f}%</strong></p>
        <div class="conf-bar-wrap">
          <div class="conf-bar-fill" style="width:{confidence:.1f}%"></div>
        </div>
        """
    else:
        conf_html = '<p class="result-conf">SVM model · RBF Kernel</p>'

    st.markdown(f"""
    <div class="result-card">
      <p class="result-label">Recommended Crop</p>
      <p class="result-crop">{prediction.title()}</p>
      {conf_html}
    </div>
    """, unsafe_allow_html=True)


# ── Model stats strip ─────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-strip">
  <div class="stat-box"><div class="stat-val">SVM</div><div class="stat-key">Algorithm</div></div>
  <div class="stat-box"><div class="stat-val">2.2k</div><div class="stat-key">Soil Samples</div></div>
  <div class="stat-box"><div class="stat-val">22</div><div class="stat-key">Crop Classes</div></div>
  <div class="stat-box"><div class="stat-val">73%</div><div class="stat-key">Accuracy</div></div>
</div>
""", unsafe_allow_html=True)


# ── About section ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="about-card">
  <p class="about-title">About the Model</p>
  <ul class="about-list">
    <li>Support Vector Machine with RBF kernel, trained on labelled soil records</li>
    <li>Four input features: Nitrogen, Phosphorus, Potassium, and pH</li>
    <li>Classifies soil profiles into one of 22 distinct crop types</li>
    <li>Trained on 2,200 samples from diverse agricultural conditions</li>
  </ul>
  <div class="insight-box">
    <p class="insight-label">✦ Key Insight</p>
    <p class="insight-text">
      Potassium (K) was identified as the strongest individual predictor of crop type — 
      fields with high K levels reliably cluster into distinct crop categories, giving 
      the model a decisive separating feature.
    </p>
  </div>
</div>
""", unsafe_allow_html=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Sowing Success &nbsp;·&nbsp; AI Crop Recommendation &nbsp;·&nbsp; Powered by SVM
</div>
""", unsafe_allow_html=True)