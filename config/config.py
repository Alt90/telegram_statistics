import os


API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

PROXY_HOST = os.environ.get('PROXY_HOST')
PROXY_PORT = int(os.environ.get('PROXY_PORT', 1080))
PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')

COUNT_DAYS_FOR_ANALYZE = os.environ.get('COUNT_DAYS_FOR_ANALYZE', 3)

TELEGRAM_ADMIN_NAME = os.environ.get('TELEGRAM_ADMIN_NAME')
LABL_NAME = os.environ.get('LABL_NAME')
