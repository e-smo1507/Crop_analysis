import streamlit as st

from common import REPO_URL

st.title("Terms of use")
st.caption("Last updated 22 October 2026")

st.subheader("Purpose")
st.write("This app is an educational project that estimates crop yield from historical Indian crop "
         "production records. Using it means you accept these terms.")

st.subheader("Estimates, not advice")
st.write("Results are statistical estimates. They are not guarantees, and they are not agronomic, "
         "financial, insurance or legal advice. Do not rely on them alone for decisions about "
         "planting, selling, lending or crop insurance. Check against local field data and expert advice.")

st.subheader("Data limits")
st.write("The model learns from records for 1997 to 2019 and uses no weather or soil data. Some "
         "state, district and crop combinations have few records and give weaker estimates. "
         "See the Method and accuracy page for the measured error.")

st.subheader("No warranty and liability")
st.write("The app is provided as is, without warranty of any kind, and may be unavailable or changed "
         "at any time. To the extent the law allows, the author is not liable for losses that result "
         "from using it.")

st.subheader("Acceptable use")
st.write("Do not attempt to disrupt the service or overload it with automated requests.")

st.subheader("Source code and contact")
st.write(f"The code is at [{REPO_URL}]({REPO_URL}). Raise questions about these terms as an issue there.")
