from flask import current_app as app, render_template
import pandas as pd
from data_extraction.CsvDataExtractor import CsvDataExtractor

# Crear una instancia de CsvDataExtractor para leer los datos desde los CSV
csv_extractor = CsvDataExtractor(base_dir='data')

@app.route('/')
def home():
    # Obtener las estadísticas de todos los jugadores
    player_stats = csv_extractor.get_all_player_statistics()
    
    # Transformar el nombre del jugador
    player_stats['Player Name'] = player_stats['Player Name'].apply(lambda x: ' '.join(word.capitalize() for word in x.replace('-', ' ').split()))
    
    # Redondear los números decimales a dos decimales
    player_stats = player_stats.round(2)

    # Seleccionar las estadísticas de los primeros 10 jugadores para mostrarlas en la tabla
    top_players = player_stats.head(20)

    return render_template('index.html', players=top_players, columns=top_players.columns)

@app.route('/about')
def about():
    return "This is the about page."