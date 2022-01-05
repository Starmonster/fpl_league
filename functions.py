# In this script we'll build all the functions required to run the back end

import plotly.express as px
import pandas as pd
import json
import requests


# Build the main plotting function
# Let's use plotly to display the visualisations
def get_plotly(points_df, rank_df, league_name):
    """
    Here we'll code for plotly displays which will be more interactive and suited to web deployment
    """

    # Plot the players points
    fig = px.line(points_df, x=points_df.gameweek, y=points_df.columns,
                  title=f"{league_name} - Player Points"
                  )
    fig.update_traces(line=dict(width=5))
    fig.update_layout(
        xaxis_title="GW",
        yaxis_title="Player Points",
        legend_title="Player",
        width=1000,
        height=650
    )
    #fig.show()

    # Plot the players ranks
    fig1 = px.line(rank_df, x=rank_df.gameweek, y=rank_df.columns,
                   title=f"{league_name} - Player Rank"

                   )  # pts_frame.iloc[::-1].index
    fig1.update_yaxes(autorange="reversed")
    fig1.update_traces(line=dict(width=5))
    fig1.update_layout(
        xaxis_title="GW",
        yaxis_title="Player Rank",
        legend_title="Player",
        width=1000,
        height=650,
    )
    #fig1.show()

    # layout(xaxis = list(autorange = "reversed").

    return fig, fig1

### Call in league and player data

def get_league(league_id):
    """
    Returns the league data / current standings and user info
    """

    # Get and store league url
    league_url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings"
    # Request league data and store in a dictionary
    request_league = requests.get(league_url)
    league = request_league.json()

    # Isolate the current player standings (which includes id and entry details we can use to access mgr details)
    standings = league["standings"]["results"]
    league_name = league["league"]["name"]

    return standings, league_name


def get_points(points_type, standings):
    """
    This function returns all the weekly / or total points data
    """

    df = pd.DataFrame()
    for i, j in enumerate(standings):
        # print(i)

        # Get the entry number each manager
        entry_number = j["entry"]
        # Pass the entry number to a url
        manager = f"https://fantasy.premierleague.com/api/entry/{entry_number}/history/"

        # Call in and store the manager's data
        m = requests.get(manager)
        m_json = m.json()

        # Assign the player name for use as a column header
        name = j["player_name"]

        # Get the user's season data including pts
        user_season = m_json["current"]
        gw_number = user_season[-1]["event"]

        pts_list = []
        for x, j in enumerate(user_season):
            pts = user_season[x][points_type]  # We take the argument given by the user to create dataframe
            pts_list.append(pts)

        # Now we need to handle late entrants as their data is offset from the rest of the league.
        for i in list(range(gw_number)):
            if len(pts_list) == gw_number:  # If we have the correct amount of points - do nothing
                break
            else:
                pts_list.insert(0, 0)  # Else add a 0 (the points scored before the user entered) to start of list
                # Note Jurica is an example of this in Chumpions League

        df[name] = pd.Series(pts_list)

    # Make all the column headers lowercase to reduce later search errors!
    df.rename(columns=str.lower, inplace=True)

    return df, gw_number


def get_rank(df):
    """
    Returns weekly or overall rank

    We have passed in the user points_df
    """

    all_ranks = []
    for row in df.iterrows():
        week = row[1].values.tolist()

        sort_pts = week.copy()
        sort_pts.sort()
        sort_pts.reverse()

        ranks = []
        for i, (j, k) in enumerate(zip(week, sort_pts)):
            # find the index at which each players total_points is in the ordered list of total_points
            # Essentially find the rank of the player in that gameweek
            rank = sort_pts.index(j) + 1
            ranks.append(rank)

        all_ranks.append(ranks)

    rank_frame = pd.DataFrame(all_ranks, columns=df.columns)

    return rank_frame


def focussed(pts_frame, player_select):
    # 1. Transpose, 2. Get last column

    latest = pts_frame.T.iloc[:, -1].to_frame()

    # Reset the index so we can use to slice the df into chunks
    latest = latest.reset_index().rename(columns={"index": "name"})

    # Ask a user for their name
    username = player_select

    # Get the users row
    user_row = latest[latest.name == username.lower()]

    # Get the index of the users row
    index_of_user = user_row.index[0]

    #  Get the users three above and two below (Maybe people want to look up slightly more than down!)
    rivals = latest.iloc[index_of_user - 2: index_of_user + 3]  # Rememeber when slicing we need to end one index higher

    # Then get the complete plotset for these "rivals"
    names = rivals.name.tolist()
    pts_frame = pts_frame[names]

    return pts_frame


