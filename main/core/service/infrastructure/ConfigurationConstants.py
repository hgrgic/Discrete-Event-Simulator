import os

MONGO_DB_HOST = os.environ.get('MONGO_HOST', None)
MONGO_DB_PORT = os.environ.get('MONGO_PORT', None)
MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', None)
MONGO_DB_USER = os.environ.get('MONGO_USER', None)
MONGO_DB_PASS = os.environ.get('MONGO_PASS', None)

REPORT_COLLECTION = 'reports'
REQUEST_AUTH=True