import os

# Elasticsearch index
ES_INDEX = os.environ.get('ES_INDEX', 'openlobby')

# default analyzer for text fields
ES_TEXT_ANALYZER = os.environ.get('ES_TEXT_ANALYZER', 'czech')

# secret key for signing tokens
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    raise RuntimeError('Missing SECRET_KEY environment variable.')

# signature algorithm JSON Web Tokens
JWT_ALGORITHM = 'HS512'

# expiration time (seconds) of login attempt
LOGIN_ATTEMPT_EXPIRATION = 300

# expiration time (seconds) of session
SESSION_EXPIRATION = 60 * 60 * 24 * 14

# name of the site used in OpenID authentication
SITE_NAME = os.environ.get('SITE_NAME', 'Open Lobby')
