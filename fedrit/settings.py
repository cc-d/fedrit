"""
Django settings for fedrit project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import logging
import string
from pathlib import Path

##### Custom Vars #####
class HOST:
    name = 'fedrit',
    domain = 'fedrit.com'


##### LOGGING #####
LOGLEVEL = logging.DEBUG
LOGFLEVEL = logging.DEBUG
logging.basicConfig(level=LOGLEVEL)

LOGFORMAT = '%(asctime)s %(levelname)s %(filename)s.%(funcName)s:%(lineno)d | %(message)s'
LFORMAT = '%(asctime)s %(levelname)s %(message)s'

lformat1 = logging.Formatter(LOGFORMAT)
shandler1 = logging.StreamHandler()

lformat2 = logging.Formatter(LFORMAT)
shandler2 = logging.StreamHandler()

shandler1.setFormatter(lformat1)
shandler2.setFormatter(lformat2)

# Create logger configurations
logger_configs = {
    __name__: {
        'level': LOGLEVEL,
        'handlers': [shandler1]
    },
    'logf': {
        'level': LOGLEVEL,
        'handlers': [shandler2]
    }
}

logger = logging.getLogger(__name__)
logger.addHandler(shandler1)

lflogger = logging.getLogger('logf')
lflogger.addHandler(shandler2)

logging.basicConfig(level=LOGLEVEL, format=LOGFORMAT)

for name, config in logger_configs.items():
    logger = logging.getLogger(name)
    logger.setLevel(config['level'])
    logger.handlers = config['handlers']


##### END LOGGING #####

VALID_CHARS = string.ascii_letters + string.digits + '_' + '-'
VALID_NAME_LEN_MAX = 30
VALID_NAME_CHARS = string.ascii_letters + string.digits + '_' + '-'

CORS_ORIGIN_ALLOW_ALL = True
##### End Custom Vars #####


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-jf)h25x^^=51tjq=*_90qhqj8knk_h@)bz0%sx2z$!+oa=ae-l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework.authtoken',
    'api',
    'corsheaders',
    'django_extensions'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware'
]

ROOT_URLCONF = 'fedrit.urls'

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

WSGI_APPLICATION = 'fedrit.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


