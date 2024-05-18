from abc import ABC, abstractmethod
import pandas as pd

class DataExtractor(ABC):

    @abstractmethod
    def get_league_standings(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_team_statistics(self, team_id: int) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_player_statistics(self, player_id: int, player_name: str, team_name: str) -> pd.DataFrame:
        pass
    
    @abstractmethod
    def get_all_teams_statistics(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_all_player_statistics(self) -> pd.DataFrame:
        pass