import os
from dotenv import load_dotenv

load_dotenv(override=True)

timeout = 10

class Config:
    SECRET_KEY          = os.getenv('SECRET_KEY', 'ams-dev-secret-key-2026')
    DB_CHARSET          = os.getenv('DB_CHARSET', 'utf8mb4')
    DB_NAME             = os.getenv('DB_NAME', 'AMS_DB')
    DB_HOST             = os.getenv('DB_HOST', '127.0.0.1')
    DB_PASSWORD         = os.getenv('DB_PASSWORD', 'password123')
    DB_PORT             = int(os.getenv('DB_PORT', 3306))
    DB_USER             = os.getenv('DB_USER', 'ams_user')
    DB_CONNECT_TIMEOUT  = timeout
    DB_READ_TIMEOUT     = timeout
    DB_WRITE_TIMEOUT    = timeout
    BRAND_NAME          = "π-AMS"
