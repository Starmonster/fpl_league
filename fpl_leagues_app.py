import streamlit as st
import pandas as pd
import numpy as np

from plot_functions import *
from stat_functions import *



#Create dictionary's for our user input
points_type = {"weekly":"points", "overall":"total_points"}
tidy_search = {"No": "no", "Yes": "yes"}

def main():

    """
    A web app to display FPL player stats and performance
    """
    # Create a sidebar with links to main sections
    st.sidebar.header("Sections")
    st.sidebar.markdown("[Intro](#intro)")
    st.sidebar.markdown("[Charts](#plot)")
    st.sidebar.markdown("[Statistics](#stat_header)")
    st.sidebar.markdown("[More](#more)")

    # Header section
    st.markdown("<p style='text-align: left; color: white;'>&#11088;&#x1F47EStarmonster Labs&#x1F479;&#x1F52C </p>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; color: white;'>FPL LEAGUE ANALYSIS</h1>", unsafe_allow_html=True)

    intro_head = "<h2 style='text-align: center; color: white;'>Introduction<h2/>"
    st.header(f"{intro_head}", anchor="intro")

    st.markdown("<p style='text-align: center;'> Enter your FPL league id to generate manager performance plots and statistics!</p>", unsafe_allow_html=True)



    league_id = st.number_input("Enter your league id", step=1, value=671315)
    search_type = st.selectbox("Review weekly or overall stats?", tuple(points_type.keys()))

    if search_type == "weekly":
        search_type = "points"
    else:
        search_type = "total_points"



    # Call in the current league data from get_league function (see plot_functions.py)
    # To solve updating league periods - consider adding try/except block here to manage this issue
    try:
        standings, league_name = get_league(league_id)
    except:
        st.write("The League is updating, please hang on!!")


    # Call in the league points data
    points_df, gw_number = get_points(search_type, standings)

    # Call in the ranking data
    rank_df = get_rank(points_df)

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

    # Let's ensure we keep the real worl rankings (not rankings among the focussed names only)
    rank_cols = points_df.columns
    rank_df = rank_df[rank_cols.tolist()]

    # Add the gameweek number to our plotting dataframes
    points_df["gameweek"] = list(range(1, points_df.shape[0] + 1))
    rank_df["gameweek"] = list(range(1, rank_df.shape[0] + 1))

    chart_head = "<h2 style='text-align: center; color: white;'><h2/>"
    st.header(f"{chart_head}", anchor="plot")

    plot_generator = st.button("Generate Plots")

    if plot_generator:
        # Call in the plots from our plotting function
        with st.spinner("Loading Charts.... "):
            fig, fig1 = get_plotly(points_df, rank_df, league_name, search_type)

        st.plotly_chart(fig)
        st.plotly_chart(fig1)

    # st.write(points_df.iloc[0])
    # st.write(points_df.columns.tolist())
    st.markdown(f"<div id='linkto_title>Jump to Here<div/>", unsafe_allow_html=True)

    # STATS SECTION
    if search_type=="points":
        stat_header = f"""<h2 style='text-align: center; color: white;'>Gameweek League Stats<h2/>"""
    else:
        stat_header = f"""<h2 style='text-align: center; color: white;'>Season League Stats<h2/>"""

    st.header(f"{stat_header}", anchor="stat_header")

    if search_type == "points":
        rank_dict, pts_dict = stats_handler(rank_df, points_df)

        st.text("See League Top Scores:")
        with st.expander("See Arcade Style Top Scores"):
            st.dataframe(pts_dict["high_points"]["high_scores"])

        st.text(f"{rank_dict['high_ranks']['high_rank_name'][0]} has the most high scores with {rank_dict['high_ranks']['high_rank_score']} high scores")
        with st.expander("See top 5 ranked managers"):
            st.dataframe(rank_dict['high_ranks']['high_rank_five'])

        st.text(f"{rank_dict['low_ranks']['low_rank_name'][0]} has the most low scores with {rank_dict['low_ranks']['low_rank_score']} low scores")
        with st.expander("See bottom 5 ranked managers"):
            st.dataframe(rank_dict['low_ranks']['low_rank_five'])

        # st.text(f"{pts_dict['high_points']['high_points_name'][0]} has the single highest score with {pts_dict['high_points']['high_points_score']} in gw??")
        st.text(pts_dict["high_points"]["high_str_output"])
        with st.expander("See top 5 mangers by highest score"):
            st.dataframe(pts_dict['high_points']['high_points_five'])


        # st.text(f"{pts_dict['low_points']['low_points_name'][0]} has the single lowest score with {pts_dict['low_points']['low_points_score']} in gw??")
        st.text(pts_dict["low_points"]["low_str_output"])
        with st.expander("See top 5 managers by lowest score"):
            st.dataframe(pts_dict['low_points']['low_points_five'])

    else:
        st.text("Season stats go here!! Work in Progress!!")
        st.warning("User Warning: Load time up to 1 minute to generate season stats!!")
        season_generator = st.button("Generate Season Stats")

        if season_generator:
            with st.spinner("Loading Stats.... "):
                bonus, captain = season_stats(league_id)

            st.text("BONUS POINTS RANKINGS:")
            with st.expander("See ranks by bonus points scored:"):
                st.dataframe(bonus)

            st.text("CAPTAIN PICK POINTS RANKINGS:")
            with st.expander("See ranks by captain pick points scored:"):
                st.dataframe(captain)



    st.markdown("Code:<link> https://github.com/Starmonster/fpl_league</link>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()