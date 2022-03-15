import pandas as pd
import numpy as np
import requests
# from tqdm import tqdm


def rank_stats(rank_df):
    """
    For weekly queries
    In this function we return the high top rank, high bottom rank
    """

    # Construct empty dictionary to hold our rank stats
    rank_dict = dict({"high_ranks": {"high_rank_name": "",
                                     "high_rank_score": 0,
                                     "high_rank_five": pd.DataFrame()},
                      "low_ranks": {"low_rank_name": "",
                                    "low_rank_score": 0,
                                    "low_rank_five": pd.DataFrame()}
                      })

    #  Ranks
    # Get the count of how often each player achieves each available rank
    rank_no_gw = rank_df[rank_df.columns.difference(["gameweek"])]
    rank_counts = rank_no_gw.apply(pd.value_counts).fillna(0)

    #  Top ranker
    # sort by highest count for toprank #15
    top_count = rank_counts.loc[1].sort_values(ascending=False)
    # what is the max count
    top_max_value = top_count.values.max()
    # Isolate which players have this high count
    top_count_name = top_count[top_count == top_max_value]

    # Create a dataframe to hold how many times each manager has achieved a top weekly points score
    df_top = pd.DataFrame(top_count).reset_index().rename(columns={"index": "Manager", 1: "Top Count"})
    rank = df_top["Top Count"].rank(method="min", ascending=False).astype(int)
    df_top.insert(0, "rank", rank)
    df_top["Top Count"] = df_top["Top Count"].astype(int)
    df_top.set_index("rank", inplace=True)

    # If there are multiple low achievers we need to print them all out
    list_of_top_names = []
    for i in range(0, top_count_name.shape[0]):
        joint_top = top_count_name.index[i]
        list_of_top_names.append(joint_top.title())

    # Bottom ranker
    # sort by highest count for bottom rank #15
    bottom_count = rank_counts.iloc[-1].sort_values(ascending=False)
    # what is the max count
    bottom_max_value = bottom_count.values.max()
    # Isolate which players have this high count
    bottom_count_name = bottom_count[bottom_count == bottom_max_value]

    df_bott = pd.DataFrame(bottom_count).reset_index()
    df_bott.columns = ["Manager", "Bottom Count"]

    rank = df_bott["Bottom Count"].rank(method="min", ascending=False).astype(int)
    df_bott.insert(0, "rank", rank)
    df_bott["Bottom Count"] = df_bott["Bottom Count"].astype(int)
    df_bott.set_index("rank", inplace=True)

    # If there are multiple low achievers we need to print them all out
    list_of_bottom_names = []
    for i in range(0, bottom_count_name.shape[0]):
        joint_bottom = bottom_count_name.index[i]
        list_of_bottom_names.append(joint_bottom.title())

    # Populate the dictionary with our date - top rankers
    rank_dict["high_ranks"]["high_rank_name"] = list_of_top_names
    rank_dict["high_ranks"]["high_rank_score"] = top_max_value
    rank_dict["high_ranks"]["high_rank_five"] = df_top

    # Bottom rankers
    rank_dict["low_ranks"]["low_rank_name"] = list_of_bottom_names
    rank_dict["low_ranks"]["low_rank_score"] = bottom_max_value
    rank_dict["low_ranks"]["low_rank_five"] = df_bott

    return rank_dict


def points_stats(pts_frame):
    """
    For weekly queries
    return best / worst points hauls
    """
    # Construct empty dictionary to hold our points stats
    pts_dict = dict({"high_points": {"high_points_name": "",
                                     "high_points_score": 0,
                                     "high_points_five": pd.DataFrame(),},
                     "low_points": {"low_points_name": "",
                                    "low_points_score": 0,
                                    "low_points_five": pd.DataFrame()}
                     })

    # Single highest and lowest scores - first isolate only player features
    pts_no_gw = pts_frame[pts_frame.columns.difference(["gameweek"])]

    # Get the top scores for each player
    sorted_max_points = pts_no_gw.max().sort_values(ascending=False)
    # Get the top score
    max_score = sorted_max_points[0]
    # Get all the managers who achieved the top score (typically only 1 manager)
    top_scorers = sorted_max_points[sorted_max_points == max_score]

    # Create a dataframe of each player's top score
    df_top = pd.DataFrame(sorted_max_points).reset_index().rename(columns={"index": "Manager", 0: "Top Scores"})
    rank = df_top["Top Scores"].rank(method="min", ascending=False).astype(int)
    df_top.insert(0, "rank", rank)
    df_top["Top Scores"] = df_top["Top Scores"].astype(int)
    df_top.set_index("rank", inplace=True)

    # Get the list of names who have achieved the top points score
    list_of_top_names = []
    for i in range(0, top_scorers.shape[0]):
        joint_scorer = top_scorers.index[i]
        list_of_top_names.append(joint_scorer.title())
    print(f"{' & '.join(list_of_top_names)} have the same top score of {max_score} in the league")

    # Get the low scores for eachplayer
    sorted_min_points = pts_no_gw.min().sort_values()
    # remove zero values where a player may have missed the gameweek / late to the game
    sorted_min_points = sorted_min_points[sorted_min_points != 0]  # manual hack to eliminate plyrs who missed gw1
    min_score = sorted_min_points[0]
    low_scorers = sorted_min_points[sorted_min_points == min_score]

    # Create a dataframe of each players' bottom score
    df_bott = pd.DataFrame(sorted_min_points).reset_index().rename(columns={"index": "Manager", 0: "Bottom Scores"})
    rank = df_bott["Bottom Scores"].rank(method="min", ascending=True).astype(int)
    df_bott.insert(0, "rank", rank)
    df_bott["Bottom Scores"] = df_bott["Bottom Scores"].astype(int)
    df_bott.set_index("rank", inplace=True)

    # Get the list of names who have achieved the top points score
    list_of_bottom_names = []
    for i in range(0, low_scorers.shape[0]):
        joint_scorer = low_scorers.index[i]
        list_of_bottom_names.append(joint_scorer.title())
    print(f"{' & '.join(list_of_bottom_names)} have the same low score of {min_score} in the league")

    # Populate the dictionary with our data - top points scorers
    pts_dict["high_points"]["high_points_name"] = list_of_top_names
    pts_dict["high_points"]["high_points_score"] = max_score
    pts_dict["high_points"]["high_points_five"] = df_top

    # Bottom points scorers
    pts_dict["low_points"]["low_points_name"] = list_of_bottom_names
    pts_dict["low_points"]["low_points_score"] = min_score
    pts_dict["low_points"]["low_points_five"] = df_bott

    return pts_dict


def points_stats_gws(pts_frame):
    # GET HIGH SCORES
    # Remove the gameweek column so this does not affect our scoring calculations
    pts_no_gw = pts_frame[pts_frame.columns.difference(["gameweek"])]

    # Construct empty dictionary to hold our points stats
    pts_dict = dict({"high_points": {"high_str_output": "",
                                     "high_points_five": pd.DataFrame(),
                                     "high_scores": pd.DataFrame()},
                     "low_points": {"low_str_output": "",
                                    "low_points_five": pd.DataFrame()}
                     })

    max_pts_ply = pts_no_gw.max().to_frame().reset_index().rename(columns={0: "high_score", "index": "manager"})
    max_pts_gw = pd.DataFrame(pts_no_gw.idxmax().values + 1, columns=["gw"])  # , columns=["points", "gw"])
    max_pts_df = max_pts_ply.join(max_pts_gw)

    sorted_max = max_pts_df.sort_values(by="high_score", ascending=False).reset_index(drop=True)

    #  Build the new stats package
    max_score = sorted_max["high_score"].iloc[0]
    # Get the top scorers
    top_scorers = sorted_max[sorted_max["high_score"] == max_score]["manager"]
    # Get the gameweeks at which the top scores were made
    gw_list = [sorted_max.iloc[i].gw for i in range(0, len(top_scorers))]
    # Create a list of strings stating the player and the gameweek top score achieved
    stat_string = [f"{top_scorers[i].title()} in gw {gw_list[i]}" for i in range(0, len(top_scorers))]
    format_num = len(top_scorers)
    # Make some string manipluation to allow the function to display the correct number of top scorers
    # Create 1 paretheses for string format
    parenth = "{}, "
    # Build the correct number of parentheses
    str_par = parenth * (format_num - 1) + "{}"

    if len(top_scorers) > 1:
        high_out = (f"{len(top_scorers)} players have the top score of {max_score}: " f"{str_par}".format(*stat_string))

    else:
        high_out = (
            f"{top_scorers[0].title()} has the single highest score with {max_score} in gameweek {gw_list[0]}!")

    #  GET LOW SCORES

    # Get minimum points excluding 0 scores  - our app will only accept non zero scores.
    # Zero scores assumed to be missed Gameweeks!!!
    non_zeros = pts_no_gw[pts_no_gw > int(0)]
    min_pts_ply = pts_no_gw[pts_no_gw > int(0)].min().to_frame().reset_index().rename(
        columns={0: "low_score", "index": "manager"})
    min_pts_ply["low_score"] = min_pts_ply["low_score"].astype(int)
    min_pts_gw = pd.DataFrame(non_zeros.idxmin().values + 1, columns=["gw"])  # , columns=["points", "gw"])
    min_pts_df = min_pts_ply.join(min_pts_gw)

    sorted_min = min_pts_df.sort_values(by="low_score", ascending=True).reset_index(drop=True)

    #  Build the new stats package
    min_score = sorted_min["low_score"].iloc[0]
    # Get the low scorers
    low_scorers = sorted_min[sorted_min["low_score"] == min_score]["manager"]
    # Get the gameweeks at which the top scores were made
    gw_list = [sorted_min.iloc[i].gw for i in range(0, len(low_scorers))]
    # Create a list of strings stating the player and the gameweek top score achieved
    stat_string = [f"{low_scorers[i].title()} in gw {gw_list[i]}" for i in range(0, len(low_scorers))]
    format_num = len(low_scorers)
    # Make some string manipluation to allow the function to display the correct number of top scorers
    # Create 1 paretheses for string format
    parenth = "{}, "
    # Build the correct number of parentheses
    str_par = parenth * (format_num - 1) + "{}"
    # print(f"{len(top_scorers)} players have the top score of {max_score}: " "{}, {}".format(*stat_string))
    if len(low_scorers) > 1:
        low_out = (f"{len(low_scorers)} players have the low score of {min_score}: " f"{str_par}".format(*stat_string))
    else:
        low_out = (f"{low_scorers[0].title()} has the single lowest score with {min_score} in gameweek {gw_list[0]}!")

    # Add ranking features to the datasets
    max_rank = sorted_max["high_score"].rank(method="min", ascending=False).astype(int)
    sorted_max.insert(0, "rank", max_rank)
    sorted_max.set_index("rank", inplace=True)

    min_rank = sorted_min["low_score"].rank(method="min", ascending=True).astype(int)
    sorted_min.insert(0, "rank", min_rank)
    sorted_min.set_index("rank", inplace=True)


    ####GET ARCADE LEAGUE HIGH SCORES
    # Stack each full gameweek one on top of the other then sort by points scored
    stacked_scores = pts_no_gw.stack().reset_index()
    stacked_scores["gameweek"] = stacked_scores["level_0"] + 1
    stacked_scores.drop("level_0", axis=1, inplace=True)
    stacked_scores.rename(columns={0: "points", "level_1": "manager"}, inplace=True)
    # Sort by high scores
    sorted_scores = stacked_scores.sort_values(by="points", ascending=False)
    sorted_scores.reset_index(drop=True, inplace=True)
    max_rank = sorted_scores["points"].rank(method="min", ascending=False).astype(int)
    sorted_scores.insert(0, "rank", max_rank)
    sorted_scores.set_index("rank", inplace=True)

    # Enter the data into our data dict
    pts_dict["high_points"]["high_str_output"] = high_out
    pts_dict["high_points"]["high_points_five"] = sorted_max
    pts_dict["high_points"]["high_scores"] = sorted_scores
    pts_dict["low_points"]["low_str_output"] = low_out
    pts_dict["low_points"]["low_points_five"] = sorted_min

    return pts_dict


# Build season stats
def bonus_points(df_data, id_list):
    bonus_df = pd.DataFrame(columns=["manager", "bonus"])
    for manager in id_list:
        manager_season = df_data[df_data.manager == manager[1]]

        team = manager_season[(manager_season.position > 0) & (manager_season.position < 12)]
        season_bonus = team.bonus.sum()
        temp = pd.DataFrame([[manager[1], season_bonus]], columns=bonus_df.columns)
        #     bonus_df = bonus_df.append({'manager': manager[1], 'bonus': season_bonus}, ignore_index=True)
        bonus_df = bonus_df.append(temp)

    bonus_df.sort_values(by="bonus", ascending=False, inplace=True)
    bonus_df.reset_index(inplace=True, drop=True)
    max_rank = bonus_df["bonus"].rank(method="min", ascending=False).astype(int)

    bonus_df.insert(0, "rank", max_rank)
    bonus_df.set_index("rank", inplace=True)

    return bonus_df


def captain_points(df_data, id_list):
    cap_df = pd.DataFrame(columns=["manager", "captain_pts"])
    for manager in id_list:
        manager_season = df_data[df_data.manager == manager[1]]

        team = manager_season[manager_season.is_captain == 1].sort_values(by="gw")
        captain_pts = team.total_points.sum()

        temp = pd.DataFrame([[manager[1], captain_pts]], columns=cap_df.columns)
        #     cap_df = cap_df.append({'manager': manager[1], 'cap': season_cap}, ignore_index=True)
        cap_df = cap_df.append(temp)

    cap_df.sort_values(by="captain_pts", ascending=False, inplace=True)
    cap_df.reset_index(inplace=True, drop=True)
    max_rank = cap_df["captain_pts"].rank(method="min", ascending=False).astype(int)

    cap_df.insert(0, "rank", max_rank)
    cap_df.set_index("rank", inplace=True)

    return cap_df

def season_stats(league_id):
    """
    In this function we'll call in season stats and display some of our preferred data
    """

    league_url = f"https://fantasy.premierleague.com/api/leagues-classic/{league_id}/standings"

    request_league = requests.get(league_url)
    league = request_league.json()

    # Isolate the current player standings (which includes id and entry details we can use to access mgr details)
    standings = league["standings"]["results"]
    # league_name = league["league"]["name"]
    id_list = []

    for i in range(0, len(standings)):
        id_list.append((standings[i]["entry"], standings[i]["player_name"]))

    # First we need to get the gameweek
    my_url = f"https://fantasy.premierleague.com/api/entry/{1400333}/"
    my_request = requests.get(my_url)
    my_json = my_request.json()

    gw = my_json["current_event"]

    df_squads = pd.DataFrame()

    # Check all gameweeks up to the latest gw and build the manager season squads dataframe

    for i in id_list:
        for j in range(1, gw + 1):

            try:
                my_url_picks = f"https://fantasy.premierleague.com/api/entry/{i[0]}/event/{j}/picks/"
                my_picks_req = requests.get(my_url_picks)
                my_picks_json = my_picks_req.json()

                gw_df = pd.DataFrame(my_picks_json["picks"])
                gw_df["gw"] = j
                gw_df["manager"] = i[1]
                df_squads = df_squads.append(gw_df)
            except:
                # Fill nans if a manager missed a gameweek (normally early gameweeks for late entries)
                gw_df = pd.DataFrame({'element': np.nan, 'position': np.nan, 'multiplier': np.nan,
                                      'is_captain': np.nan, 'is_vice_captain': np.nan, 'gw': j, 'manager': i[1]},
                                     index=[0])
                df_squads = df_squads.append(gw_df)

    #  Now get the players high level data from endpoint
    players = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    players = requests.get(players)
    players = players.json()
    elements_df = pd.DataFrame(players['elements'])

    # Now get detailed gw data for each player
    # Set an empty data set to store all the data
    data = pd.DataFrame()
    for i in range(1, elements_df.shape[0]):
        # Access the endpoint
        element = f"https://fantasy.premierleague.com/api/element-summary/{i}/"
        get_element = requests.get(element)
        element_json = get_element.json()
        #  Convert the player history in a dataframe
        element_hist = pd.DataFrame(element_json['history'])
        #  Add the player history to the master player history dataset
        data = data.append(element_hist)
    data = data.rename(columns={"round": "gw"})

    # specify the required columns from each dataset to be merged
    ele_cols = ['id', 'web_name', 'element_type']
    data_cols = ["element", "gw", "total_points", "goals_scored", "assists", "clean_sheets", "goals_conceded", "bonus"]
    # Merge the player weekly and general data
    data_merged = data[data_cols].merge(elements_df[ele_cols], left_on="element", right_on="id")

    # Now merge our weekly player data with our managers squads dataframe
    df_data = df_squads.fillna(0).reset_index(drop=True).merge(data_merged, on=["element", "gw"])

    # Call the bonus points
    bonus_ranks = bonus_points(df_data, id_list)
    captain_ranks = captain_points(df_data, id_list)

    return bonus_ranks, captain_ranks

def stats_handler(rank_df, points_frame):
    """
    This function handles and returns the data from stat generator functions.
    """

    # Return the stats from rank_stat function....
    rank_dict = rank_stats(rank_df)

    # Return the stats from points_stat function...
    # pts_dict = points_stats(points_frame)
    pts_dict = points_stats_gws(points_frame)


    return rank_dict, pts_dict