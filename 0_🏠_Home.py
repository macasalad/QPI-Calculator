import streamlit as st

st.set_page_config(
    page_title = "Home",
    page_icon = "🏠"
)

st.title("Welcome to [App Title]! ✨")

st.link_button("CompSAt QPI Calculator", "https://qpi.compsat.org/")
st.sidebar.success("Select a feature above.")