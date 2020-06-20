import os

MYSQL_SERVER = os.environ.get('MYSQL_SERVER', "leader-of-digital-mysql")
MYSQL_USER = os.environ.get('MYSQL_USER', "root")
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', "12121212")
MYSQL_DB = os.environ.get('MYSQL_DB', "leaderofdigital")
MYSQL_PORT = os.environ.get('MYSQL_PORT', "3306")
SECRET_KEY = os.environ.get('SECRET_KEY', b"leader-of-digital-jwt-secret")

VK_APP_ID = '7516806'
VK_APP_SECRET = os.environ.get('VK_APP_SECRET', '')

SQLALCHEMY_DATABASE_URI = (
	f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_SERVER}:{MYSQL_PORT}/{MYSQL_DB}"
)

PROJECT_NAME = "LeadersOfDigitalBackend"

BACKEND_CORS_ORIGINS = "http://localhost:*, http://0.0.0.0:*"

API_V1_STR = "/api/v1"