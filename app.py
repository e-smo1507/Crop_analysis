import streamlit as st

from common import CSS, REPO_URL, ROOT

st.set_page_config(page_title="Crop Yield Estimator", page_icon=str(ROOT / "assets" / "favicon.png"),
                   layout="centered")
st.markdown(CSS, unsafe_allow_html=True)

pages = [
    st.Page("views/predict.py", title="Estimate", url_path="estimate", default=True),
    st.Page("views/about.py", title="Method and accuracy", url_path="method"),
    st.Page("views/privacy.py", title="Privacy", url_path="privacy"),
    st.Page("views/terms.py", title="Terms", url_path="terms"),
]
st.navigation(pages, position="top").run()

st.markdown('<div class="site-footer">', unsafe_allow_html=True)
cols = st.columns(4)
cols[0].page_link(pages[2], label="Privacy")
cols[1].page_link(pages[3], label="Terms")
cols[2].link_button("Source code", REPO_URL, type="tertiary")
st.markdown("</div>", unsafe_allow_html=True)
