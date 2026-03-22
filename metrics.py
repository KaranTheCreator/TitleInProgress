from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
from nba_api.stats.static import players
from nba_api.stats.static import teams

def get_player_stats(player_name):
    # Return player name and selected career stats.
    player = players.find_players_by_full_name(player_name)
    if not player:
        return None, None

    player_id = player[0]["id"]

    # Get display name
    info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    name = info.get_data_frames()[0]["DISPLAY_FIRST_LAST"][0]

    # Get career stats
    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    df = career.get_data_frames()[0]

    
    team_lookup = {team["id"]: team["abbreviation"] for team in teams.get_teams()}
    df["TEAM"] = df["TEAM_ID"].map(team_lookup)


    #turns totals into pre-made averages for easier calculations
    df["PPG"] = df["PTS"] / df["GP"]
    df["APG"] = df["AST"] / df["GP"]
    df["RPG"] = df["REB"] / df["GP"]
    df["BPG"] = df["BLK"] / df["GP"]
    df["SPG"] = df["STL"] / df["GP"]

    # Pick columns
    stats = df[["SEASON_ID", "TEAM", "GP", "PPG", "RPG", "APG", "BPG", "SPG", "TOV", "FGA", "FGM", "FG_PCT"]].to_dict(orient="records")

    return name, stats
