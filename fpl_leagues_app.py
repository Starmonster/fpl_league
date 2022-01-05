import streamlit as st
import pandas as pd
import numpy as np

from functions import *



#Create dictionary's for our user input
points_type = {"points":"points", "total_points":"total_points"}
tidy_search = {"Yes": "yes", "No": "no"}

def main():

    """
    A web app to display FPL player stats and performance
    """

    st.title("FPL TEAM ANALYSIS")
    st.subheader("Shows user performance per week and across full season")
    st.markdown("<h1 style='text-align: center; color: red;'>Centred Text</h1>", unsafe_allow_html=True)

    league_id = st.number_input("What is your league id?", step=1)
    search_type = st.selectbox("Review weekly or overall stats?", tuple(points_type.keys()))

    # Call in the current league data from get_league function (see functions.py)
    standings, league_name = get_league(league_id)

    # Call in the league points data
    points_df, gw_number = get_points(search_type, standings)

    # For large leagues we may want to reduce the quantity of data returned (to keep plots easy to read)
    reduce = st.selectbox("Compare closest rivals only?", options=tuple(tidy_search.keys()))

    # If else statement to handle reduced plots to go below...
    if reduce.lower() == "yes":
        all_players = points_df.columns.tolist()
        player_select = st.selectbox("What's your name?", all_players)

        points_df = focussed(points_df, player_select)

        #### ASK THE USER THEIR NAME THROUGH STREAMLIT INTERFACE - THEN PASS NAME TO FOCUSSED FCT
    else:
        points_df = points_df
    # Call in the ranking data
    rank_df = get_rank(points_df)

    # Add the gameweek number to our plotting dataframes
    points_df["gameweek"] = list(range(1, points_df.shape[0] + 1))
    rank_df["gameweek"] = list(range(1, rank_df.shape[0] + 1))

    # Call in the plots from our plotting function
    fig, fig1 = get_plotly(points_df, rank_df, league_name)

    st.plotly_chart(fig)
    st.plotly_chart(fig1)

    # st.write(points_df.iloc[0])
    # st.write(points_df.columns.tolist())



if __name__ == "__main__":
    main()