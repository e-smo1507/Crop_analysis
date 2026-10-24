import json
from pathlib import Path

import joblib
import streamlit as st

ROOT = Path(__file__).parent
MODELS = ROOT / "models"
REPO_URL = "https://github.com/essthar10/crop-yield-prediction"
FEATURES = {
    "full": ["State", "District", "Crop", "Year", "Season", "Area", "Production"],
    "forecast": ["State", "District", "Crop", "Year", "Season", "Area"],
}
NEEDED = ["model_full.pkl", "model_forecast.pkl", "le_state.pkl", "le_district.pkl",
          "le_crop.pkl", "le_season.pkl", "catalog.json", "metrics.json"]

CSS = """
<style>
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], [data-testid="stAppDeployButton"] { display: none !important; }
.block-container { padding-top: 3rem; max-width: 760px; }
h1 { font-weight: 700; letter-spacing: -0.01em; }
.stButton > button, .stDownloadButton > button {
    border-radius: 4px; font-weight: 600; padding: 0.55rem 1.4rem;
}
[data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"] { border-radius: 4px; }
[data-testid="stMetric"] { background: #E6ECE5; border-left: 4px solid #1F5A3B; padding: 1rem 1.2rem; border-radius: 4px; }
.site-footer { border-top: 1px solid #C9D1C8; margin-top: 3rem; padding-top: 1rem; font-size: 0.9rem; }
@media (prefers-reduced-motion: reduce) { * { animation: none !important; transition: none !important; } }
</style>
"""


@st.cache_resource
def load_assets():
    missing = [n for n in NEEDED if not (MODELS / n).exists()]
    if missing:
        return None
    return {
        "full": joblib.load(MODELS / "model_full.pkl"),
        "forecast": joblib.load(MODELS / "model_forecast.pkl"),
        "enc": {c: joblib.load(MODELS / f"le_{c}.pkl") for c in ("state", "district", "crop", "season")},
        "catalog": json.loads((MODELS / "catalog.json").read_text()),
        "metrics": json.loads((MODELS / "metrics.json").read_text()),
    }
