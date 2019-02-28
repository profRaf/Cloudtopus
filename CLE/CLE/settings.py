import os
import sys
import getpass
import ipgetter
from celery.schedules import crontab


# Get public ip of server
PUBLIC_IP = ipgetter.myip()
PUBLIC_IP_GOOGLE = PUBLIC_IP + ".xip.io"
PRODUCTION_DOMAIN = ['www.cloudtopus.com','cloudtopus.com']
LOCALHOST_DOMAIN = ['localhost','127.0.0.1']


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR,"templates")
STATIC_DIR = os.path.join(BASE_DIR,"static")


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '--2$vfi4$(vsdvf_@_(6x%$9^(-ea3h0gkr6p*8j)zf7!_y&je'
AES_SECRET_KEY = 'A$4Hj8dhf3c@aj87'
EVENT_SECRET_KEY = '4c81cc820321d84eb2963b3c5c85a11e77d3b9510790b326f42a66c35ee61b7b'


# SECURITY WARNING: don't run with debug turned on in production!
#DEBUG = True #Testing for local
DEBUG= False #for deployment

#ALLOWED_HOSTS= ['*']
ALLOWED_HOSTS = [PUBLIC_IP,PUBLIC_IP_GOOGLE,'www.cloudtopus.com'] + PRODUCTION_DOMAIN + LOCALHOST_DOMAIN
PRODUCTION_SERVER_HOSTS = PRODUCTION_DOMAIN + LOCALHOST_DOMAIN


ADMIN_LOGIN = 'admin3'
ADMIN_PASSWORD = 'admin1+2'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Module_TeamManagement',
    'Module_Account',
    'Module_DeploymentMonitoring',
    'Module_CommunicationManagement',
    'Module_EventConfig',
    'django.contrib.sites', # new
    'allauth', # new
    'allauth.account', # new
    'allauth.socialaccount', # new
    'allauth.socialaccount.providers.google', # new
    'django_celery_beat', # new
    'formtools',
    'widget_tweaks',
    'background_task',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CLE.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR],
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

WSGI_APPLICATION = 'CLE.wsgi.application'


# Database Initiation
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# Database configuration
password = ''
host = 'localhost'
default_DB = 'App_Data'
cle_DB = 'CLE_Data'

# Checks if it's production linux server
if 'posix' in os.name and 'ec2-user' in getpass.getuser():
    password = 'cle12345'

# Checks if it's local developement or production
# if PUBLIC_IP in PRODUCTION_SERVER_HOSTS:
#     host = '52.76.221.221'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': default_DB,
        'USER': 'root',
        'PASSWORD': password,
        'HOST': host,
        'PORT': '3306',
    },
    'CLE_Data': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': cle_DB,
        'USER': 'root',
        'PASSWORD': password,
        'HOST': host,
        'PORT': '3306',
    }
}

DATABASE_ROUTERS = ['CLE.router.TMRouter']


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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


# Social Authentications

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

SOCIALACCOUNT_ADAPTER = 'Module_Account.adapters.SocialAccountWhitelist'


SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'hd': 'smu.edu.sg'
        }
    }
}

SITE_ID = 2 # Check your Database to see site id


LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_LOGOUT_ON_GET = True

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/
STATIC_ROOT = STATIC_DIR
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    STATIC_DIR,
    #'/Thunderhead Monkeys/CLE/static',
]


FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)


# Celery Configuration
# Celery application definition
# http://docs.celeryproject.org/en/v4.0.2/userguide/configuration.html

CELERY_BROKER_URL  = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Makassar'
CELERY_BEAT_SCHEDULE = {
    'task-number-one': { #name of scheduler
    'task': 'trailheadscrapper', #name of task
    'schedule':  crontab(hour=0, minute=45) #period of running in seconds (Roughly one day)
    #'arg's :  #if have args
    #},
    #'task-number-two': { #name of scheduler
    #'task': 'tableaurefresh', #name of task
    #'schedule':  100.0 #period of running in seconds
    #'arg's :  #if have args
    },

}


# Django-Backgroun-Tasks configuration

MAX_ATTEMPTS = 3
BACKGROUND_TASK_RUN_ASYNC = True
