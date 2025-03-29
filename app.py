import streamlit as st
import duckdb as db

st.write("Hello world!")
with st.sidebar:
    theme = st.selectbox(
        "what would you like to review?",
        ("cross_Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme..."
    )
    st.write("You selected:", theme)