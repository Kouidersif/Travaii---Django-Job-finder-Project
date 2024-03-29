

from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('NOT_SECRET')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = [ "*" ]

if DEBUG == False:
    ALLOWED_HOSTS = ['https//travaii.com', 'https//travaii.com', '192.169.177.207', 'http://192.169.177.207', 'travaii.com', 'www.travaii.com', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS = ['https://*.travaii.com', 'https://*.127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'company',
    'applicants',
    'fontawesomefree',
    'django_filters',
    'bootstrapform',
    'ckeditor',
    'mathfilters',
    'blog',
    'django_recaptcha',
    'django_celery_results',
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

ROOT_URLCONF = 'JobPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'JobPortal.wsgi.application'


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



# Celery Configuration Options
CELERY_TIMEZONE = 'UTC'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


#test
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'JobPortal/static')
]

#static root 
STATIC_ROOT =  os.path.join(BASE_DIR, 'static/')

MEDIA_URL= '/images/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'images/')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL= 'main.User'


#APPEND_SLASH=False

# STRIPE_PUBLISHABLE_KEY = 'pk_test_51Lz03SKORmC2RvgXRhtthq6yKQVLC1xLCCSq7PWqJ8HqFClSjSOtvQBDN7ImsLdRilbvCTbe1XBQE7ppeKP3D5tL007zG2iI6B'
# STRIPE_PUBLISHABLE_KEY = 'pk_live_51Lz03SKORmC2RvgXf0IAm5tseSPsDozduvh8jFgRwCdn4fxeMKZAAPL6JC7btx654sLBbJBhvvhKo6o7Xc0NYWHB00Xm3uEJE0'
# STRIPE_SECRET_KEY = config('STPCEY')
# STRIPE_SECRET_KEY = 'sk_test_51Lz03SKORmC2RvgXBDXoH9ulCpO8Bg4S8PniDbXU5PleTK4bRXyuBGVWXKaQ8ICYCT9XEIWSLi80lwIo8mQ5tut600SicR7GGr'
# STRIPE_ENDPOINT_SECRET = config('wbhk')
# STRIPE_ENDPOINT_SECRET = "whsec_23636b68c54e8c74bce145860e8196efc1ec047b5714a3d665180809b9f9ae53"



CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    'awesome_ckeditor': {
        'skin': 'moono',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        "removePlugins": "stylesheetparser",
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-','Preview','-']},
            {'name': 'clipboard', 'items': ['Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Checkbox', 'Radio']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            #{'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            #{'name': 'insert',
             #'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}


## EMAIL CONFIG


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
if DEBUG == False:
    #EMAIL_HOST = 'server163.web-hosting.com'
    EMAIL_HOST = 'mail.privateemail.com'
    # EMAIL_HOST_PASSWORD =config('EMLPDW')
    EMAIL_HOST_USER = 'support@travaii.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    DEFAULT_FROM_EMAIL = 'support@travaii.com'
PASSWORD_RESET_TIMEOUT= 14400


# Add to your settings file
CONTENT_TYPES = ['image', 'video', 'file']
# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
MAX_UPLOAD_SIZE = 2621440


LOGIN_REDIRECT_URL = 'home' 

LOGIN_URL = 'log_in'


RECAPTCHA_PUBLIC_KEY = os.getenv("CAPATCHA_PUBLIC")
RECAPTCHA_PRIVATE_KEY = os.getenv("CAPATCHA_PRIVATE")



CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'django-cache'

# celery setting.
CELERY_CACHE_BACKEND = 'default'

# django setting.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# Redis as message broker
CELERY_BROKER_URL = 'redis://localhost:6379/0'

# Redis as backend
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'