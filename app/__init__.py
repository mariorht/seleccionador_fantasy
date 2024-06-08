from flask import Flask
from data_extraction.SofascoreDataExtractor import SofascoreDataExtractor
import os

def create_app():
    app = Flask(__name__)

    with app.app_context():
        # Importar las rutas
        from . import routes

        # Verificar y crear archivos de datos si no existen
        extractor = SofascoreDataExtractor()
        extractor.check_and_create_data_files(base_dir=os.path.join(app.root_path, '../data'), image_dir=os.path.join(app.root_path, '../data/images'))

    return app
