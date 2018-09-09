import os


API_ID = os.environ.get('API_ID')
API_HASH = os.environ.get('API_HASH')

PROXY_HOST = os.environ.get('PROXY_HOST')
PROXY_PORT = int(os.environ.get('PROXY_PORT', 1080))
PROXY_USERNAME = os.environ.get('PROXY_USERNAME')
PROXY_PASSWORD = os.environ.get('PROXY_PASSWORD')

LIMIT_MESSAGES_FOR_ANALYZE = os.environ.get('LIMIT_MESSAGES_FOR_ANALYZE', 5000)

TELEGRAM_ADMIN_NAME = os.environ.get('TELEGRAM_ADMIN_NAME')
