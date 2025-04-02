# pylint: disable=missing-module-docstring
import duckdb
import pandas as pd
import streamlit as st
import numpy as np

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
# solution = duckdb.sql(answer).df()

with st.sidebar:
    theme = st.selectbox(
        "what would you like to review?",
        ("cross_joins", "GroupBy", "Windows Functions"),
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    exercise = con.execute(f"SELECT * FROM memory_state WHERE theme = '{theme}'").df()
    st.write(exercise)

st.header("enter your code:")
query = st.text_area(label="votre code sql ici", key="user_input")

if query:
    result = con.execute(query).df()
    st.dataframe(result)
#
#     if len(result.columns) != len(solution.columns):
#         st.write("some columns are missing")
#     try:
#         result = result[solution.columns]
#         st.dataframe(result.compare(solution))
#     except KeyError as a:
#         st.write("Some columns are missing")
#
#     n_lines_difference = result.shape[0] - solution.shape[0]
#     if n_lines_difference != 0:
#         st.write(
#          f"result has a {n_lines_difference} lines difference with the solution"
#       )
tab2, tab3 = st.tabs(["tables", "solution"])

with tab2:
    exercise_tables = exercise.loc[0, "tables"]
    exercise["tables"] = exercise["tables"].apply(
        lambda x: x.tolist() if isinstance( x, np.ndarray ) else x
    )
    for table in exercise_tables:
        st.write(f"table : {table}")
        df_table = con.execute(f"SELECT * FROM {table}")
        st.dataframe(df_table)

with tab3:
    exercise_name = exercise.loc[0, "exercise_name"]
    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()
        st.text(answer)
