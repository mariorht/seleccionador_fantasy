import unittest
import pandas as pd
import os

from data_extraction.SofascoreDataExtractor import SofascoreDataExtractor
from data_extraction.CsvDataExtractor import CsvDataExtractor
import shutil


class TestDataExtractors(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Crear instancia de SofascoreDataExtractor
        cls.api_extractor = SofascoreDataExtractor()

        # Crear la carpeta 'test/data' si no existe
        if not os.path.exists('tests/data'):
            os.makedirs('tests/data')

        # Guardar la clasificación total en un CSV
        cls.league_standings_total = cls.api_extractor.get_league_standings("total")
        cls.league_standings_total.to_csv('tests/data/league_standings_total.csv', index=False)

        # Guardar la clasificación como local en un CSV
        cls.league_standings_home = cls.api_extractor.get_league_standings("home")
        cls.league_standings_home.to_csv('tests/data/league_standings_home.csv', index=False)

        # Guardar la clasificación como visitante en un CSV
        cls.league_standings_away = cls.api_extractor.get_league_standings("away")
        cls.league_standings_away.to_csv('tests/data/league_standings_away.csv', index=False)

        # Guardar las estadísticas de todos los equipos en un CSV
        cls.team_statistics = cls.api_extractor.get_all_teams_statistics()
        cls.team_statistics.to_csv('tests/data/team_statistics.csv', index=False)

        # Guardar las estadísticas de todos los jugadores en un CSV
        cls.all_player_statistics = cls.api_extractor.get_all_player_statistics()
        cls.all_player_statistics.to_csv('tests/data/all_players_statistics.csv', index=False)

        # Crear instancia de CsvDataExtractor
        cls.csv_extractor = CsvDataExtractor(base_dir='tests/data')

    def test_league_standings_total(self):
        csv_data = self.csv_extractor.get_league_standings("total")
        pd.testing.assert_frame_equal(self.league_standings_total.fillna('N/A'), csv_data.fillna('N/A'))

    def test_league_standings_home(self):
        csv_data = self.csv_extractor.get_league_standings("home")
        pd.testing.assert_frame_equal(self.league_standings_home.fillna('N/A'), csv_data.fillna('N/A'))

    def test_league_standings_away(self):
        csv_data = self.csv_extractor.get_league_standings("away")
    
        pd.testing.assert_frame_equal(self.league_standings_away.fillna('N/A'), csv_data.fillna('N/A'))

    def test_team_statistics(self):
        csv_data = self.csv_extractor.get_all_teams_statistics()
        pd.testing.assert_frame_equal(self.team_statistics.fillna('N/A'), csv_data.fillna('N/A'))

    def test_all_player_statistics(self):
        csv_data = self.csv_extractor.get_all_player_statistics()
        pd.testing.assert_frame_equal(self.all_player_statistics.fillna('N/A'), csv_data.fillna('N/A'))
        
    @classmethod
    def tearDownClass(cls):
        # Eliminar la carpeta 'test/data' al finalizar las pruebas
        shutil.rmtree('tests/data')

if __name__ == '__main__':
    unittest.main()
