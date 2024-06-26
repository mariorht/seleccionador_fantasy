import requests
import pandas as pd
from .DataExtractor import DataExtractor
from bs4 import BeautifulSoup
import os
import pandas as pd
from fuzzywuzzy import process, fuzz

SEASON = 52376
TOURNAMENT = 8
BASE_URL = "http://www.sofascore.com/api/v1"

class SofascoreDataExtractor(DataExtractor):

    def __init__(self):
        self.teams = {
            2817: "Barcelona",
            2829: "Real Madrid",
            2885: "Deportivo Alavés",
            6577: "Las Palmas",
            33779: "Granada",
            24264: "Girona FC",
            2836: "Atlético Madrid",
            2825: "Athletic Club",
            2824: "Real Sociedad",
            2816: "Real Betis",
            2819: "Villarreal",
            2828: "Valencia",
            2859: "Getafe",
            2833: "Sevilla",
            2820: "Osasuna",
            2826: "Mallorca",
            2821: "Celta Vigo",
            2818: "Rayo Vallecano",
            4488: "Cádiz",
            2858: "Almería"
        }

    def get_league_standings(self, standings_type: str = "total") -> pd.DataFrame:
        """
        Obtiene la clasificación de la liga según el tipo especificado: 'total', 'home' o 'away'.
        """
        if standings_type not in ["total", "home", "away"]:
            raise ValueError("standings_type debe ser 'total', 'home' o 'away'")
        
        url = f"{BASE_URL}/unique-tournament/{TOURNAMENT}/season/{SEASON}/standings/{standings_type}"
        response = requests.get(url)
        data = response.json()

        teams_data = data['standings'][0]['rows']  # Asumiendo que 'standings' contiene la clasificación deseada

        teams_list = []
        for team in teams_data:
            team_info = {
                'Position': team['position'],
                'Team': team['team']['name'],
                'Matches': team['matches'],
                'Wins': team['wins'],
                'Draws': team['draws'],
                'Losses': team['losses'],
                'Goals For': team['scoresFor'],
                'Goals Against': team['scoresAgainst'],
                'Points': team['points'],
                'Promotion/Relegation': team.get('promotion', {}).get('text', 'N/A')
            }
            teams_list.append(team_info)

        return pd.DataFrame(teams_list)

    def get_team_statistics(self, team_id: int) -> pd.DataFrame:
        url = f"{BASE_URL}/team/{team_id}/unique-tournament/{TOURNAMENT}/season/{SEASON}/statistics/overall"
        response = requests.get(url)
        data = response.json()

        if 'statistics' in data:
            stats = data['statistics']
            team_stats = {
                'Team': self.teams[team_id],
                'Goals Scored': stats.get('goalsScored', 0),
                'Goals Conceded': stats.get('goalsConceded', 0),
                'Assists': stats.get('assists', 0),
                'Shots': stats.get('shots', 0),
                'Penalty Goals': stats.get('penaltyGoals', 0),
                'Penalties Taken': stats.get('penaltiesTaken', 0),
                'Free Kick Goals': stats.get('freeKickGoals', 0),
                'Goals From Inside The Box': stats.get('goalsFromInsideTheBox', 0),
                'Goals From Outside The Box': stats.get('goalsFromOutsideTheBox', 0),
                'Yellow Cards': stats.get('yellowCards', 0),
                'Red Cards': stats.get('redCards', 0),

            }
            return pd.DataFrame([team_stats])
        else:
            return pd.DataFrame()


    def get_all_teams_statistics(self) -> pd.DataFrame:
        all_teams_stats = pd.DataFrame()

        for team_id, team_name in self.teams.items():
            team_stats = self.get_team_statistics(team_id)
            if not team_stats.empty:
                all_teams_stats = pd.concat([all_teams_stats, team_stats], ignore_index=True)

        return all_teams_stats

    def get_player_statistics(self, player_id: int, player_name: str, team_name: str) -> pd.DataFrame:
        url = f"{BASE_URL}/player/{player_id}/unique-tournament/{TOURNAMENT}/season/{SEASON}/statistics/overall"
        response = requests.get(url)
        data = response.json()
        if 'statistics' in data:
            stats = data['statistics']
            player_stats = {
                'Player Name': player_name,
                'Team': team_name,
                'Rating': stats.get('rating', None),
                'Total Rating': stats.get('totalRating', None),
                'Goals': stats.get('goals', None),
                'Assists': stats.get('assists', None),
                'Expected Goals': stats.get('expectedGoals', None),
                'Expected Assists': stats.get('expectedAssists', None),
                'Accurate Passes': stats.get('accuratePasses', None),
                'Inaccurate Passes': stats.get('inaccuratePasses', None),
                'Total Passes': stats.get('totalPasses', None),
                'Successful Dribbles': stats.get('successfulDribbles', None),
                'Yellow Cards': stats.get('yellowCards', None),
                'Red Cards': stats.get('redCards', None),
                'Shots On Target': stats.get('shotsOnTarget', None),
                'Total Shots': stats.get('totalShots', None),
                'Minutes Played': stats.get('minutesPlayed', None),
                'Appearances': stats.get('appearances', None),
                'ID': player_id

            }
            return pd.DataFrame([player_stats])
        else:
            return pd.DataFrame()

            
            
    def fetch_players(self, url, team_name):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        players = []
        player_ids = set()  # Conjunto para almacenar los identificadores de los jugadores

        for link in soup.find_all('a', href=True):
            href = link['href']
            if '/es/jugador/' in href:
                parts = href.split('/')
                player_name = parts[-2]
                player_id = parts[-1]
                if player_id not in player_ids:  # Verificar si el jugador ya fue agregado
                    players.append({'Team': team_name, 'Player Name': player_name, 'ID': player_id})
                    player_ids.add(player_id)  # Agregar el identificador del jugador al conjunto

        return pd.DataFrame(players)

    def get_all_player_statistics(self) -> pd.DataFrame:
        teams = [
            ("http://www.sofascore.com/es/equipo/futbol/barcelona/2817#tab:squad", "Barcelona"),
            ("http://www.sofascore.com/es/equipo/futbol/real-madrid/2829#tab:squad", "Real Madrid"),
            ("http://www.sofascore.com/es/equipo/futbol/atletico-madrid/2836#tab:squad", "Atlético Madrid"),
            ("http://www.sofascore.com/es/equipo/futbol/sevilla/2833#tab:squad", "Sevilla FC"),
            ("http://www.sofascore.com/es/equipo/futbol/real-betis/2816#tab:squad", "Real Betis"),
            ("http://www.sofascore.com/es/equipo/futbol/villarreal/2819#tab:squad", "Villarreal CF"),
            ("http://www.sofascore.com/es/equipo/futbol/real-sociedad/2824#tab:squad", "Real Sociedad"),
            ("http://www.sofascore.com/es/equipo/futbol/athletic-club/2825#tab:squad", "Athletic Club"),
            ("http://www.sofascore.com/es/equipo/futbol/valencia/2828#tab:squad", "Valencia CF"),
            ("http://www.sofascore.com/es/equipo/futbol/celta-vigo/2821#tab:squad", "Celta de Vigo"),
            ("http://www.sofascore.com/es/equipo/futbol/getafe/2859#tab:squad", "Getafe CF"),
            ("http://www.sofascore.com/es/equipo/futbol/girona/24264#tab:squad", "Girona"),
            ("http://www.sofascore.com/es/equipo/futbol/osasuna/2820#tab:squad", "CA Osasuna"),
            ("http://www.sofascore.com/es/equipo/futbol/alaves/2885#tab:squad", "Deportivo Alavés"),
            ("http://www.sofascore.com/es/equipo/futbol/granada/33779#tab:squad", "Granada CF"),
            ("http://www.sofascore.com/es/equipo/futbol/las-palmas/6577#tab:squad", "Las Palmas"),
            ("http://www.sofascore.com/es/equipo/futbol/cadiz/4488#tab:squad", "Cádiz CF"),
            ("http://www.sofascore.com/es/equipo/futbol/mallorca/2826#tab:squad", "RCD Mallorca"),
            ("http://www.sofascore.com/es/equipo/futbol/rayo-vallecano/2818#tab:squad", "Rayo Vallecano"),
            ("http://www.sofascore.com/es/equipo/futbol/almeria/2858#tab:squad", "Almería")
        ]

        results_df = pd.DataFrame()  # DataFrame vacío para almacenar todos los resultados

        for url, team_name in teams:
            team_df = self.fetch_players(url, team_name)
            results_df = pd.concat([results_df, team_df], ignore_index=True)

        all_players_stats = pd.DataFrame()
        for index, row in results_df.iterrows():
            player_id = row['ID']
            player_name = row['Player Name']
            team_name = row['Team']
            df = self.get_player_statistics(player_id, player_name, team_name)
            if not df.empty:
                all_players_stats = pd.concat([all_players_stats, df], ignore_index=True)

        return all_players_stats
        

    def download_player_images(self, output_dir='player_images'):
        teams = [
            ("http://www.sofascore.com/es/equipo/futbol/barcelona/2817#tab:squad", "Barcelona"),
            ("http://www.sofascore.com/es/equipo/futbol/real-madrid/2829#tab:squad", "Real Madrid"),
            ("http://www.sofascore.com/es/equipo/futbol/atletico-madrid/2836#tab:squad", "Atlético Madrid"),
            ("http://www.sofascore.com/es/equipo/futbol/sevilla/2833#tab:squad", "Sevilla FC"),
            ("http://www.sofascore.com/es/equipo/futbol/real-betis/2816#tab:squad", "Real Betis"),
            ("http://www.sofascore.com/es/equipo/futbol/villarreal/2819#tab:squad", "Villarreal CF"),
            ("http://www.sofascore.com/es/equipo/futbol/real-sociedad/2824#tab:squad", "Real Sociedad"),
            ("http://www.sofascore.com/es/equipo/futbol/athletic-club/2825#tab:squad", "Athletic Club"),
            ("http://www.sofascore.com/es/equipo/futbol/valencia/2828#tab:squad", "Valencia CF"),
            ("http://www.sofascore.com/es/equipo/futbol/celta-vigo/2821#tab:squad", "Celta de Vigo"),
            ("http://www.sofascore.com/es/equipo/futbol/getafe/2859#tab:squad", "Getafe CF"),
            ("http://www.sofascore.com/es/equipo/futbol/girona/24264#tab:squad", "Girona"),
            ("http://www.sofascore.com/es/equipo/futbol/osasuna/2820#tab:squad", "CA Osasuna"),
            ("http://www.sofascore.com/es/equipo/futbol/alaves/2885#tab:squad", "Deportivo Alavés"),
            ("http://www.sofascore.com/es/equipo/futbol/granada/33779#tab:squad", "Granada CF"),
            ("http://www.sofascore.com/es/equipo/futbol/las-palmas/6577#tab:squad", "Las Palmas"),
            ("http://www.sofascore.com/es/equipo/futbol/cadiz/4488#tab:squad", "Cádiz CF"),
            ("http://www.sofascore.com/es/equipo/futbol/mallorca/2826#tab:squad", "RCD Mallorca"),
            ("http://www.sofascore.com/es/equipo/futbol/rayo-vallecano/2818#tab:squad", "Rayo Vallecano"),
            ("http://www.sofascore.com/es/equipo/futbol/almeria/2858#tab:squad", "Almería")
        ]

        # Crear la carpeta de salida si no existe
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        player_ids = set()

        for url, team_name in teams:
            team_df = self.fetch_players(url, team_name)
            for index, row in team_df.iterrows():
                player_id = row['ID']
                if player_id not in player_ids:
                    player_ids.add(player_id)
                    image_url = f"http://api.sofascore.app/api/v1/player/{player_id}/image"
                    response = requests.get(image_url, stream=True)
                    if response.status_code == 200:
                        file_path = os.path.join(output_dir, f"{player_id}.jpg")
                        with open(file_path, 'wb') as out_file:
                            out_file.write(response.content)



    def generate_players_prize_csv(self, output_dir="../data", base_dir="../assets"):
        print(f"Generando el archivo 'players_prize.csv'...")

        # Cargar los archivos CSV necesarios
        df_statistics = pd.read_csv(os.path.join(output_dir, 'all_players_statistics.csv'))
        df_biwenger = pd.read_csv(os.path.join(base_dir, 'datos_jugadores_biwenger.csv'), delimiter=';')

        # Función para encontrar el nombre más similar
        def find_best_match(name, choices, scorer, threshold=80):
            best_match, score = process.extractOne(name, choices, scorer=scorer)
            return best_match if score >= threshold else None

        # Crear un diccionario para almacenar las coincidencias
        matches = {}

        # Lista de nombres en el archivo de estadísticas
        statistics_names = df_statistics['Player Name'].tolist()

        # Encontrar las mejores coincidencias para cada nombre en el archivo de biwenger
        for player in df_biwenger['Jugador']:
            best_match = find_best_match(player, statistics_names, fuzz.token_set_ratio)
            matches[player] = best_match

        # Crear una nueva columna en el dataframe de biwenger con los nombres coincidentes
        df_biwenger['Player Name'] = df_biwenger['Jugador'].map(matches)

        # Filtrar filas donde no se encontró una coincidencia adecuada
        df_biwenger = df_biwenger.dropna(subset=['Player Name'])
        
        # Unir ambos dataframes utilizando la columna 'Player Name'
        merged_df = pd.merge(df_biwenger, df_statistics, on='Player Name')

        # Eliminar duplicados basados en una columna clave, por ejemplo, 'Player Name'
        merged_df = merged_df.drop_duplicates(subset=['Player Name'])

        # Eliminar la columna 'Jugador'
        merged_df = merged_df.drop(columns=['Jugador'])
        
        # Eliminar la columna 'Team'
        merged_df = merged_df.drop(columns=['Team'])

        # Reordenar las columnas para que 'Player Name' sea la primera
        columns_order = ['Player Name'] + [col for col in merged_df.columns if col != 'Player Name']
        merged_df = merged_df[columns_order]

        # Guardar el dataframe combinado en un nuevo archivo CSV
        players_prize_file = os.path.join(output_dir, 'players_prize.csv')
        merged_df.to_csv(players_prize_file, index=False)
        print(f"Archivo 'players_prize.csv' generado y guardado en '{players_prize_file}'.")
        

    def check_and_create_data_files(self, base_dir='../data', image_dir='../data/images'):
        # Crear una instancia de la clase SofascoreDataExtractor
        api_extractor = SofascoreDataExtractor()

        # Lista de archivos esperados
        files = [
            'league_standings_total.csv',
            'league_standings_home.csv',
            'league_standings_away.csv',
            'team_statistics.csv',
            'all_players_statistics.csv'
        ]

        # Crear la carpeta 'data' si no existe
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
            print(f"Directorio '{base_dir}' creado.")

        # Verificar y crear archivos si no existen
        for file in files:
            file_path = os.path.join(base_dir, file)
            if os.path.exists(file_path):
                print(f"El archivo '{file}' ya existe.")
            else:
                print(f"El archivo '{file}' no existe. Generando...")
                if file == 'league_standings_total.csv':
                    data = api_extractor.get_league_standings("total")
                elif file == 'league_standings_home.csv':
                    data = api_extractor.get_league_standings("home")
                elif file == 'league_standings_away.csv':
                    data = api_extractor.get_league_standings("away")
                elif file == 'team_statistics.csv':
                    data = api_extractor.get_all_teams_statistics()
                elif file == 'all_players_statistics.csv':
                    data = api_extractor.get_all_player_statistics()
                data.to_csv(file_path, index=False)
                print(f"Archivo '{file}' generado y guardado en '{file_path}'.")

        # Verificar la cantidad de imágenes en la carpeta
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
            print(f"Directorio '{image_dir}' creado.")

        num_images = len([name for name in os.listdir(image_dir) if os.path.isfile(os.path.join(image_dir, name))])
        if num_images >= 200:
            print(f"El directorio '{image_dir}' ya contiene {num_images} imágenes.")
        else:
            print(f"El directorio '{image_dir}' contiene solo {num_images} imágenes. Descargando imágenes de jugadores...")
            api_extractor.download_player_images(output_dir=image_dir)
            
            
                
        # Verificar y crear el archivo players_prize.csv si no existe
        players_prize_file = os.path.join(base_dir, 'players_prize.csv')
        print(players_prize_file)
        if os.path.exists(players_prize_file):
            print(f"El archivo 'players_prize.csv' ya existe.")
        else:
            self.generate_players_prize_csv(output_dir=base_dir, base_dir= os.path.join(base_dir, "../assets"))
            print(f"Archivo 'players_prize.csv' generado y guardado en {players_prize_file}.")


        print(f"Proceso completado. Datos guardados en la carpeta '{base_dir}' y imágenes en '{image_dir}'.")

