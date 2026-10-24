import pandas as pd
import streamlit as st

from common import FEATURES, load_assets

st.title("Estimate crop yield")
st.write("Pick a state, district, crop and season from the Indian crop production records "
         "(1997 to 2019), enter the cultivated area, and get an estimated yield in tonnes per hectare.")

assets = load_assets()
if assets is None:
    st.error("Model files are missing. Run `python train_model.py --csv data/crop_production.csv` "
             "and restart the app. See the README for the dataset download.")
    st.stop()

tree = assets["catalog"]["tree"]
y_min, y_max = assets["catalog"]["years"]

mode = st.radio(
    "What do you know?",
    ["Area only (estimate before harvest)", "Area and production (as in the project report)"],
)
use_production = mode.startswith("Area and")

left, right = st.columns(2)
state = left.selectbox("State", sorted(tree))
district = left.selectbox("District", sorted(tree[state]))
crop = left.selectbox("Crop", sorted(tree[state][district]))
season = left.selectbox("Season", tree[state][district][crop])
year = right.number_input("Year", min_value=1990, max_value=2100, value=y_max, step=1)
area = right.number_input("Area (hectares)", min_value=0.0, value=100.0, step=10.0)
production = None
if use_production:
    production = right.number_input("Production (tonnes)", min_value=0.0, value=100.0, step=10.0)

if year > y_max:
    st.warning(f"The records end in {y_max}. The model treats {int(year)} like {y_max}, "
               "so it cannot reflect newer trends.")

if st.button("Estimate yield", type="primary"):
    if area <= 0:
        st.error("Enter an area greater than 0 hectares.")
        st.stop()
    if use_production and production <= 0:
        st.error("Enter a production greater than 0 tonnes, or switch to Area only.")
        st.stop()

    enc = assets["enc"]
    values = {
        "State": enc["state"].transform([state])[0],
        "District": enc["district"].transform([district])[0],
        "Crop": enc["crop"].transform([crop])[0],
        "Year": year, "Season": enc["season"].transform([season])[0],
        "Area": area, "Production": production,
    }
    key = "full" if use_production else "forecast"
    X = pd.DataFrame([[values[c] for c in FEATURES[key]]], columns=FEATURES[key])
    estimate = float(assets[key].predict(X)[0])

    st.metric("Estimated yield", f"{estimate:.2f} tonnes per hectare")
    if use_production:
        st.caption(f"For comparison, {production:,.1f} t over {area:,.1f} ha is "
                   f"{production / area:.2f} t/ha. In this mode the model sees both numbers.")
    else:
        st.write(f"Expected total production on {area:,.1f} ha: about **{estimate * area:,.1f} tonnes**.")
    r = assets["catalog"]["crop_stats"].get(crop)
    if r:
        st.caption(f"Typical yield for {crop} in the records: {r['p25']:.2f} to {r['p75']:.2f} t/ha "
                   f"(median {r['median']:.2f}).")
