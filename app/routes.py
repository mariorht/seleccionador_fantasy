from flask import current_app as app, render_template, send_from_directory
import os
import pandas as pd
from data_extraction.CsvDataExtractor import CsvDataExtractor

# Crear una instancia de CsvDataExtractor para leer los datos desde los CSV
csv_extractor = CsvDataExtractor(base_dir=os.path.join(app.root_path, '../data'))

@app.route('/')
def home():
    # Obtener las estadísticas de todos los jugadores
    player_stats = csv_extractor.get_all_player_statistics_prize()
    
    # Transformar el nombre del jugador
    player_stats['Player Name'] = player_stats['Player Name'].apply(lambda x: ' '.join(word.capitalize() for word in x.replace('-', ' ').split()))
    
    # Redondear los números decimales a dos decimales
    player_stats = player_stats.round(2)

    return render_template('index.html', players=player_stats, columns=player_stats.columns)

@app.route('/images/<filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, '../data/images'), filename + ".jpg")

@app.route('/about')
def about():
    return "This is the about page."

@app.route('/scatter')
def scatter():
    # Obtener las estadísticas de todos los jugadores
    player_stats = csv_extractor.get_all_player_statistics_prize()
    
    # Transformar el nombre del jugador
    player_stats['Player Name'] = player_stats['Player Name'].apply(lambda x: ' '.join(word.capitalize() for word in x.replace('-', ' ').split()))
    
    # Redondear los números decimales a dos decimales
    player_stats = player_stats.round(2)
    
    # Identificar columnas numéricas
    numeric_columns = player_stats.select_dtypes(include='number').columns.tolist()
    
    return render_template('scatter.html', columns=numeric_columns, players=player_stats)
