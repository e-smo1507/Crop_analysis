import streamlit as st

from common import REPO_URL

st.title("Privacy")
st.caption("Last updated 22 October 2026")
st.write("This is a student project. It does not ask you to sign up and does not ask for personal information.")

st.subheader("What the app handles")
st.write("The values you choose or type (state, district, crop, season, year, area, production) are sent "
         "to the server only to calculate the estimate. The app does not save them to a database or file.")

st.subheader("Cookies and analytics")
st.write("The app sets no cookies of its own and runs no advertising or analytics code. Usage statistics "
         "collection in Streamlit is switched off in the configuration.")

st.subheader("Hosting")
st.write("Whoever hosts the app, and the network in between, may keep standard technical logs such as IP "
         "address, time and requested page. Those logs are governed by the host's own policy, not by this app.")

st.subheader("Contact")
st.write(f"Questions or deletion requests can be raised as an issue at [{REPO_URL}]({REPO_URL}).")
