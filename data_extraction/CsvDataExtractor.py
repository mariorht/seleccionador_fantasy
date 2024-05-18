from .DataExtractor import DataExtractor
import pandas as pd

class CsvDataExtractor(DataExtractor):

    def __init__(self, base_dir='data'):
        self.base_dir = base_dir

    def get_league_standings(self, standings_type: str) -> pd.DataFrame:
        file_map = {
            "total": "league_standings_total.csv",
            "home": "league_standings_home.csv",
            "away": "league_standings_away.csv"
        }
        file_path = f"{self.base_dir}/{file_map.get(standings_type, 'league_standings_total.csv')}"
        return pd.read_csv(file_path)

    def get_team_statistics(self, team_id: int) -> pd.DataFrame:
        team_stats = pd.read_csv(f"{self.base_dir}/team_statistics.csv")
        return team_stats[team_stats['Team ID'] == team_id]

    def get_player_statistics(self, player_id: int, player_name: str, team_name: str) -> pd.DataFrame:
        player_stats = pd.read_csv(f"{self.base_dir}/all_players_statistics.csv")
        return player_stats[(player_stats['Player Name'] == player_name) & (player_stats['Team'] == team_name)]

    def get_all_teams_statistics(self) -> pd.DataFrame:
        return pd.read_csv(f"{self.base_dir}/team_statistics.csv")

    def get_all_player_statistics(self) -> pd.DataFrame:
        return pd.read_csv(f"{self.base_dir}/all_players_statistics.csv")
