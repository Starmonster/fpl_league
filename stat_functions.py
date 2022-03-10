import pandas as pd


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
                                     "high_points_five": pd.DataFrame()},
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
    df_top = pd.DataFrame(sorted_max_points).reset_index().rename(columns={"index": "Manager", 0: "Top Count"})
    rank = df_top["Top Count"].rank(method="min", ascending=False).astype(int)
    df_top.insert(0, "rank", rank)
    df_top["Top Count"] = df_top["Top Count"].astype(int)
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
    df_bott = pd.DataFrame(sorted_min_points).reset_index().rename(columns={"index": "Manager", 0: "Bottom Count"})
    rank = df_bott["Bottom Count"].rank(method="min", ascending=True).astype(int)
    df_bott.insert(0, "rank", rank)
    df_bott["Bottom Count"] = df_bott["Bottom Count"].astype(int)
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


def stats_handler(rank_df, points_frame):
    """
    This function handles and returns the data from stat generator functions.
    """

    # Return the stats from rank_stat function....
    rank_dict = rank_stats(rank_df)

    # Return the stats from points_stat function...
    pts_dict = points_stats(points_frame)

    return rank_dict, pts_dict