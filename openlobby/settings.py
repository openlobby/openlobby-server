import os
import dsnparse

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = 'DEBUG' in os.environ

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if DEBUG:
        SECRET_KEY = 'not-secret-at-all'
    else:
        raise RuntimeError('Missing SECRET_KEY environment variable.')

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',
    'django_extensions',
    'graphene_django',
    'django_elasticsearch_dsl',
    'openlobby.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'openlobby.core.middleware.TokenAuthMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'openlobby.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'openlobby.wsgi.application'

AUTH_USER_MODEL = 'core.User'

DATABASE_DSN = os.environ.get('DATABASE_DSN', 'postgresql://db:db@localhost:5432/openlobby')
db = dsnparse.parse(DATABASE_DSN)
assert db.scheme == 'postgresql'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': db.paths[0],
        'USER': db.username,
        'PASSWORD': db.password,
        'HOST': db.host,
        'PORT': db.port,
    }
}

ELASTICSEARCH_DSL = {
    'default': {
        'hosts': os.environ.get('ELASTICSEARCH_DSN', 'http://localhost:9200'),
    },
}

ELASTICSEARCH_DSL_INDEX_SETTINGS = {
    'number_of_shards': 1,
    'number_of_replicas': 0,
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# Internationalization

LANGUAGE_CODE = 'cs'

TIME_ZONE = 'Europe/Prague'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO' if DEBUG else 'WARNING',
        },
    },
}


GRAPHENE = {
    'SCHEMA': 'openlobby.schema.schema'
}

###############################################################################
# Custom settings

# Elasticsearch index with reports
ES_INDEX = os.environ.get('ES_INDEX', 'openlobby')

# default analyzer for text fields
ES_TEXT_ANALYZER = os.environ.get('ES_TEXT_ANALYZER', 'czech')

# signature algorithm JSON Web Tokens
JWT_ALGORITHM = 'HS512'

# expiration time (seconds) of login attempt
LOGIN_ATTEMPT_EXPIRATION = 300

# expiration time (seconds) of session
SESSION_EXPIRATION = 60 * 60 * 24 * 14

# name of the site used in OpenID authentication
SITE_NAME = os.environ.get('SITE_NAME', 'Open Lobby')

# redirect URI used in OpenID authentication
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:8010/login-redirect')
