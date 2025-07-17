# config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY        = os.environ.get('SECRET_KEY', 'clave_por_defecto')
    DB_USER           = os.environ.get('DB_USER', 'root')
    DB_PASSWORD       = os.environ.get('DB_PASSWORD', '')
    DB_HOST           = os.environ.get('DB_HOST', '127.0.0.1')
    DB_PORT           = os.environ.get('DB_PORT', '3307')   # <-- default a tu puerto Laragon
    DB_NAME           = os.environ.get('DB_NAME', 'graphroute')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
