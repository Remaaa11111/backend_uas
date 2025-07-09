from datetime import timedelta
import os
from dotenv import load_dotenv

load_dotenv()  # Load file .env

class Config:
    # Konfigurasi Aplikasi
    SECRET_KEY = os.getenv('SECRET_KEY', 'supersecretkey')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'superjwtsecretkey')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.getenv('JWT_ACCESS_TOKEN_EXPIRES', 3600)))

    # Konfigurasi Database Manual (jika kamu tidak pakai SQLAlchemy)
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'db_perpus')
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_POOLNAME = os.getenv('DB_POOLNAME', 'db_perpus_pool')
    POOL_SIZE = int(os.getenv('POOL_SIZE', 10))
