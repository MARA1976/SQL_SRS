import streamlit as st
import duckdb as db
import pandas as pd


st.write("""
#SQL SRS Spaced repetition  System SQL practice
""")

st.write("Hello world!")
with st.sidebar:
    theme = st.selectbox(
        "what would you like to review?",
        ("cross_Joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme..."
    )
    st.write("You selected:", theme)