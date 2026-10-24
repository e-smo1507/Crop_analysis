"""Clean the Kaggle India Agriculture Crop Production dataset, train the
Decision Tree and Random Forest regressors, and write everything the app needs
into models/.

Usage:  python train_model.py --csv data/crop_production.csv
"""
import argparse
import datetime
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeRegressor

OUT = Path(__file__).parent / "models"
CATS = ["State", "District", "Crop", "Season"]
FEATURES = {
    "full": ["State", "District", "Crop", "Year", "Season", "Area", "Production"],
    "forecast": ["State", "District", "Crop", "Year", "Season", "Area"],
}


def clean(path):
    df = pd.read_csv(path)
    df.columns = [c.strip() for c in df.columns]
    df = df.rename(columns={"State_Name": "State", "District_Name": "District", "Crop_Year": "Year"})
    log = [("Raw records", len(df))]

    df = df.dropna(subset=["Crop", "Season", "Area", "Production"])
    log.append(("After removing rows with missing values", len(df)))

    if "Production Units" in df.columns:
        df = df[df["Production Units"].astype(str).str.strip().str.lower() == "tonnes"]
    log.append(("After keeping records measured in tonnes", len(df)))

    for c in CATS:
        df[c] = df[c].astype(str).str.strip()
    df["Year"] = df["Year"].astype(str).str[:4].astype(int)
    df["Area"] = pd.to_numeric(df["Area"], errors="coerce")
    df["Production"] = pd.to_numeric(df["Production"], errors="coerce")
    df = df.dropna(subset=["Area", "Production"]).drop_duplicates()
    log.append(("After removing duplicates", len(df)))

    df = df[(df["Area"] > 0) & (df["Production"] > 0)].copy()
    df["Yield"] = df["Production"] / df["Area"]
    log.append(("After removing zero area or zero production", len(df)))

    df = df[df["Yield"] <= df["Yield"].quantile(0.99)]
    log.append(("After removing yield above the 99th percentile", len(df)))

    per_year = df.groupby("Year").size()
    thin = per_year[per_year < 0.05 * per_year.median()].index
    df = df[~df["Year"].isin(thin)]
    log.append((f"After removing incomplete years {list(map(int, thin)) or 'none'}", len(df)))
    return df.reset_index(drop=True), log


def build_catalog(df):
    tree = {}
    for (s, d, c), g in df.groupby(["State", "District", "Crop"]):
        tree.setdefault(s, {}).setdefault(d, {})[c] = sorted(g["Season"].unique())
    q = df.groupby("Crop")["Yield"].quantile([0.25, 0.5, 0.75]).unstack()
    crop_stats = {c: {"p25": r[0.25], "median": r[0.5], "p75": r[0.75]} for c, r in q.iterrows()}
    return {"tree": tree, "crop_stats": crop_stats,
            "years": [int(df["Year"].min()), int(df["Year"].max())]}


def evaluate(model, X, y):
    p = model.predict(X)
    return {"r2": float(r2_score(y, p)),
            "rmse": float(np.sqrt(mean_squared_error(y, p))),
            "mae": float(mean_absolute_error(y, p))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    args = ap.parse_args()
    OUT.mkdir(exist_ok=True)

    df, log = clean(args.csv)
    catalog = build_catalog(df)
    for c in CATS:
        enc = LabelEncoder().fit(df[c])
        df[c] = enc.transform(df[c])
        joblib.dump(enc, OUT / f"le_{c.lower()}.pkl")

    metrics = {"cleaning": log, "rows": len(df), "sklearn": sklearn.__version__,
               "trained_on": datetime.date.today().isoformat(), "models": {}, "importance": {}}
    for name, cols in FEATURES.items():
        X_tr, X_te, y_tr, y_te = train_test_split(df[cols], df["Yield"], test_size=0.2, random_state=42)
        metrics["train_rows"], metrics["test_rows"] = len(X_tr), len(X_te)
        dt = DecisionTreeRegressor(random_state=42).fit(X_tr, y_tr)
        rf = RandomForestRegressor(n_estimators=50, max_depth=12, min_samples_leaf=5,
                                   random_state=42, n_jobs=-1).fit(X_tr, y_tr)
        metrics["models"][name] = {"decision_tree": evaluate(dt, X_te, y_te),
                                   "random_forest": evaluate(rf, X_te, y_te)}
        metrics["importance"][name] = dict(zip(cols, map(float, rf.feature_importances_)))
        joblib.dump(rf, OUT / f"model_{name}.pkl", compress=3)
        size = (OUT / f"model_{name}.pkl").stat().st_size / 1e6
        print(f"{name}: {metrics['models'][name]}  file {size:.1f} MB")

    (OUT / "catalog.json").write_text(json.dumps(catalog))
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print("Saved to", OUT)


if __name__ == "__main__":
    main()
