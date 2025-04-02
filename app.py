# pylint: disable=missing-module-docstring
import duckdb
import streamlit as st

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
answer = """
SELECT * FROM beverages
CROSS JOIN food_items
"""
#solution = duckdb.sql(answer).df()

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
# if query:
#     result = duckdb.sql(query).df()
#     st.dataframe(result)
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
#             f"result has a {n_lines_difference} lines difference with the solution"
#         )
# tab2, tab3 = st.tabs(["tables", "solution"])
#
# with tab2:
#     st.write("table: beverages")
#     st.dataframe(beverages)
#     st.write("table: food_items")
#     st.dataframe(food_items)
#     st.write("expected:")
#     st.dataframe(solution)
#
# with tab3:
#     st.text(answer)
