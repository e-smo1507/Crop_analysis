# Crop Yield Estimator

Streamlit app that estimates crop yield (tonnes per hectare) for Indian state, district, crop and season
combinations. Built from the summer internship project at DLK Software Solutions, Chennai.

Pages: Estimate, Method and accuracy, Privacy, Terms.

## 1. Get the data
Download "India Agriculture Crop Production" from Kaggle and save it as `data/crop_production.csv`.
Expected columns: State, District, Crop, Year, Season, Area, Production, Production Units.
(The data is not included in this repository.)

## 2. Train
    pip install -r requirements.txt
    python train_model.py --csv data/crop_production.csv

This cleans the data, trains a Decision Tree and a Random Forest for two input sets (with and without
Production), and writes models, encoders, a catalog of valid combinations and measured metrics to `models/`.
The Method page shows the real numbers from that run. Commit `models/` so the host can load it.

## 3. Run locally
    streamlit run app.py
    python -m pytest -q tests

## 4. Deploy
Use the same Python (3.11) and package versions as `requirements.txt`, because pickled scikit-learn models
break across versions.

* Streamlit Community Cloud: connect the GitHub repo, set Python 3.11 under advanced settings. It gives a
  `*.streamlit.app` address and shows its own "Hosted with Streamlit" badge outside the app, which the app
  cannot remove. To my knowledge it does not support custom domains.
* Custom domain and no host badge: deploy the included `Dockerfile` on Render, Fly.io, Railway or a VPS,
  then add a CNAME record at your domain registrar pointing to the host's address, and enable HTTPS in the
  host dashboard.

## Branding
The favicon is `assets/favicon.png`. Streamlit's menu, footer and deploy button are hidden in `common.py`.
