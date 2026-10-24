import pandas as pd
import streamlit as st

from common import REPO_URL, load_assets

st.title("Method and accuracy")
st.write("This app was built during a Data Science internship at DLK Software Solutions, Chennai, "
         "as part of a B.Tech Information Technology course at Anna University, Tiruchirappalli. "
         f"The code is public: [{REPO_URL}]({REPO_URL}).")

st.subheader("Data")
st.write("The Kaggle dataset India Agriculture Crop Production, with records by state, district, crop, "
         "season and year. Yield is production divided by area.")

assets = load_assets()
if assets is None:
    st.info("Train the model to see the measured accuracy and cleaning log here.")
    st.stop()
m = assets["metrics"]

st.subheader("Cleaning")
st.table(pd.DataFrame(m["cleaning"], columns=["Step", "Records"]).set_index("Step"))

st.subheader("Accuracy on held-out data")
st.write(f"{m['train_rows']:,} records for training and {m['test_rows']:,} for testing, split at random "
         f"(80:20). Trained on {m['trained_on']} with scikit-learn {m['sklearn']}.")
names = {"full": "Area and production", "forecast": "Area only"}
rows = []
for key, label in names.items():
    for algo, algo_label in (("decision_tree", "Decision Tree"), ("random_forest", "Random Forest")):
        r = m["models"][key][algo]
        rows.append({"Inputs": label, "Model": algo_label, "R2": round(r["r2"], 4),
                     "RMSE": round(r["rmse"], 3), "MAE": round(r["mae"], 3)})
st.dataframe(pd.DataFrame(rows), hide_index=True, width="stretch")

st.subheader("What the numbers mean")
st.write("Yield is calculated as production divided by area. When production and area are both given "
         "as inputs, the model is partly recovering a number it was handed, so the high score in that "
         "row says little about forecasting. The Area only rows are the fairer measure of an estimate "
         "made before harvest.")
st.write("The split is random, so records from the same district and year can appear in both training "
         "and test sets. Accuracy on a later year or an unseen district would likely be lower. "
         "The model does not use rainfall, temperature or soil data.")

st.subheader("Feature importance (Random Forest)")
pick = st.radio("Inputs", list(names.values()), horizontal=True)
key = [k for k, v in names.items() if v == pick][0]
st.bar_chart(pd.Series(m["importance"][key]).sort_values(ascending=False))
