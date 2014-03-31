"""
Django settings for photorize project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
from configurations import Configuration, values
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'wpfj_uj^j&gyc@97ua(fk&+=da0(^0j_*m&e6i6xzx-6hog4&+'

    TEMPLATE_DEBUG = True

    ALLOWED_HOSTS = ['localhost']


    # Application definition
    DEFAULT_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        # 'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'south',
        'bootstrap3',
        'sorl.thumbnail',
        'registration',
    )

    LOCAL_APPS = (
        'photorizer',
    )

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS

    ACCOUNT_ACTIVATION_DAYS = 3

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'user@gmail.com'
    EMAIL_HOST_PASSWORD = 'secret'
    DEFAULT_FROM_EMAIL = 'user@gmail.com'
    # EMAIL_PORT = 465
    EMAIL_PORT = 587

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    )

    ROOT_URLCONF = 'photorize.urls'

    WSGI_APPLICATION = 'photorize.wsgi.application'


    # Database
    # https://docs.djangoproject.com/en/1.6/ref/settings/#databases

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'photorizedb',
            'USER': 'photorizer',
            'PASSWORD': 'photorize',
            'HOST': 'localhost',
            # 'ENGINE': 'django.db.backends.sqlite3',
            # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/var/www/photorizer/media/'

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.6/howto/static-files/
    STATIC_URL = '/static/'
    STATIC_ROOT = '/var/www/photorizer/static/'

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.messages.context_processors.messages',
        'django.contrib.auth.context_processors.auth')

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # SITE_ID = 'photorizer.com'

    LOGIN_URL = 'login'
    LOGOUT_URL = 'logout'
    LOGIN_REDIRECT_URL = '/main'

    # LOGGING = {}

class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    DEFAULT_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        # 'django.contrib.sites',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'south',
        'bootstrap3',
        'sorl.thumbnail',
        'registration',
    )

    LOCAL_APPS = (
        'photorizer',
    )

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS + ('debug_toolbar',)

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Prod(Base):
    DEBUG = False
    AWS_STORAGE_BUCKET_NAME = 'photorize'
    STATICFILES_STORAGE = 'storages.backends.s3boto.S3BotoStorage'
    S3_URL = 'http://%s.s3.amazonaws.com/' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = S3_URL
