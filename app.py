# pylint: disable=missing-module-docstring

import os
import logging
import duckdb
import numpy as np
import streamlit as st
import pandas as pd
from datetime import date, timedelta

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")
if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read()) # pylint: disable=missing-module-docstring

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

def check_user_solution(user_query: str) -> None:
    result = con.execute(user_query).df()
    st.dataframe(result)
    try:
        result = result[solution_df.columns]
        st.dataframe( result.compare( solution_df ) )
        if result.compare(solution_df).shape == (0, 0):
            st.write("correct!")
            st.balloons()

    except KeyError as a:
        st.write( "Some columns are missing" )
    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution"
        )

with st.sidebar:
    available_themes_df = con.execute(f"SELECT DISTINCT theme FROM memory_state").df()
    theme = st.selectbox(
        "what would you like to review?",
        available_themes_df ["theme"].unique(),
        index=None,
        placeholder="Select a theme...",
    )
    if theme:
        st.write( f"You selected {theme}" )
        exercise = (
            con.execute( f"SELECT * FROM memory_state WHERE theme = '{theme}'" )
            .df()
            .sort_values( "last_reviewed" )
            .reset_index( drop=True )
        )
    else:
        exercise = (
            con.execute( f"SELECT * FROM memory_state" )
            .df()
            .sort_values( "last_reviewed" )
            .reset_index( drop=True )
        )

    st.write(exercise)

    exercise_name = exercise.loc[0, "exercise_name"]
    with open( f"answers/{exercise_name}.sql", "r" ) as f:
        answer = f.read()

    solution_df = con.execute(answer).df()


st.header("enter your code:")
query = st.text_area(label="votre code sql ici", key="user_input")


if query:
    check_user_solution(query)

for n_days in [2, 7, 21]:
    if st.button(f'revoir dans {n_days} jours'):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name '{exercise_name}'")
        st.rerurn()

if st.button('Reset'):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")


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

        st.text(answer)
