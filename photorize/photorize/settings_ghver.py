from configurations import Configuration, values
from urlparse import urljoin
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


class Base(Configuration):
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'SECRET'
    ALLOWED_HOSTS = ['localhost']

    # Application definition
    DEFAULT_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.sites',  # required for allauth
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    )

    THIRD_PARTY_APPS = (
        'bootstrap3',
        'sorl.thumbnail',
    )

    LOCAL_APPS = (
        'photorizer',
    )

    ALLAUTH_APPS = (
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        # include the providers you want to enable:
        # 'allauth.socialaccount.providers.amazon',
        # 'allauth.socialaccount.providers.angellist',
        # 'allauth.socialaccount.providers.bitbucket',
        # 'allauth.socialaccount.providers.bitly',
        # 'allauth.socialaccount.providers.coinbase',
        'allauth.socialaccount.providers.dropbox',
        # 'allauth.socialaccount.providers.facebook',
        # 'allauth.socialaccount.providers.flickr',
        # 'allauth.socialaccount.providers.feedly',
        # 'allauth.socialaccount.providers.github',
        'allauth.socialaccount.providers.google',
        # 'allauth.socialaccount.providers.hubic',
        # 'allauth.socialaccount.providers.instagram',
        # 'allauth.socialaccount.providers.linkedin',
        # 'allauth.socialaccount.providers.linkedin_oauth2',
        # 'allauth.socialaccount.providers.openid',
        # 'allauth.socialaccount.providers.persona',
        # 'allauth.socialaccount.providers.soundcloud',
        # 'allauth.socialaccount.providers.stackexchange',
        # 'allauth.socialaccount.providers.tumblr',
        # 'allauth.socialaccount.providers.twitch',
        # 'allauth.socialaccount.providers.twitter',
        # 'allauth.socialaccount.providers.vimeo',
        # 'allauth.socialaccount.providers.vk',
        # 'allauth.socialaccount.providers.weibo',
        # 'allauth.socialaccount.providers.xing',
        )

    INSTALLED_APPS = DEFAULT_APPS + THIRD_PARTY_APPS + LOCAL_APPS + ALLAUTH_APPS

    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_USE_TLS = True
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_HOST_USER = 'xxxx'
    EMAIL_HOST_PASSWORD = 'xxxx'
    DEFAULT_FROM_EMAIL = 'Photorizer Staff <staff@photorizer.net>'
    EMAIL_PORT = 587

    # Allauth config settings
    ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
    ACCOUNT_EMAIL_REQUIRED = True
    SOCIALACCOUNT_EMAIL_VERIFICATION = 'optional'
    SOCIALACCOUNT_EMAIL_REQUIRED = False
    SOCIALACCOUNT_PROVIDERS = {
        'google':
            {'SCOPE': ['profile',],
             'AUTH_PARAMS': {'access_type': 'online'}}}

    TEMPLATE_DIRS = (
        'photorizer/templates/allauth',
        )

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

    DEBUG = False
    TEMPLATE_DEBUG = False
    THUMBNAIL_DEBUG = False

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

    CACHES = {
        # 'default': {
        #     'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        #     'LOCATION': '127.0.0.1:11211'
        # }
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.messages.context_processors.messages',
        'django.contrib.auth.context_processors.auth',
        # Required by allauth template tags
        'django.core.context_processors.request',
        # allauth specific context processors
        'allauth.account.context_processors.account',
        'allauth.socialaccount.context_processors.socialaccount',
        )

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regarless of 'allauth'
        'django.contrib.auth.backends.ModelBackend',
        # allauth-specific authentication methods, such as login by e-mail
        'allauth.account.auth_backends.AuthenticationBackend',
        )

    # Internationalization
    # https://docs.djangoproject.com/en/1.6/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    SITE_ID = 2  # site ID in django_sites db table

    LOGIN_URL = 'login'
    LOGOUT_URL = 'logout'
    LOGIN_REDIRECT_URL = '/main'

    # LOGGING = {}


class Dev(Base):
    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = True
    TEMPLATE_DEBUG = True
    THUMBNAIL_DEBUG = True

    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/var/www/photorizer/media/'
    STATIC_URL = '/static/'
    # STATIC_ROOT = '/var/www/photorizer/static/'

    STATICFILES_DIRS = (
        '/var/www/photorizer/static',
        )

    INSTALLED_APPS = Base.INSTALLED_APPS + ('debug_toolbar',)


    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    BOOTSTRAP3 = {
        'jquery_url': urljoin(STATIC_URL, 'jquery-1.11.1.min.js'),
        # 'jquery_url': '/var/www/photorizer/static/jquery.min.js',
        'base_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/'),
        # 'base_url': '/var/www/photorizer/static/bootstrap-3.2.0-dist/',
        # 'css_url': None,
        'theme_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/css/bootstrap.min.css'),
        # 'theme_url': '/var/www/photorizer/static/bootstrap-3.2.0-dist/css/bootstrap-theme.min.css',
        'css_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/css/custom.css'),
        'javascript_url': None,
        'javascript_in_head': False,
        'include_jquery': True,
        'horizontal_label_class': 'col-md-2',
        'horizontal_field_class': 'col-md-4',
        'set_required': True,
        'form_required_class': '',
        'form_error_class': '',
        'form_renderers': {
            'default': 'bootstrap3.renderers.FormRenderer',
            },
        'formset_renderers':{
            'default': 'bootstrap3.renderers.FormsetRenderer',
            },
        'field_renderers': {
            'default': 'bootstrap3.renderers.FieldRenderer',
            'inline': 'bootstrap3.renderers.InlineFieldRenderer',
            },
        }

class Test(Base):
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'test_media')
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'test_static')
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


class Prod(Base):
    ALLOWED_HOSTS = ['*']
    ADMINS = (
        ('xxxx', 'xxxx'),
    )
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': '127.0.0.1:11211'
        }
    }

    INSTALLED_APPS = Base.INSTALLED_APPS + ('s3_folder_storage',)

    DEFAULT_FILE_STORAGE = 's3_folder_storage.s3.DefaultStorage'
    DEFAULT_S3_PATH = "media"
    STATICFILES_STORAGE = 's3_folder_storage.s3.StaticStorage'
    STATIC_S3_PATH = "static"
    AWS_ACCESS_KEY_ID = 'xxxx'
    AWS_SECRET_ACCESS_KEY = 'xxxx'
    AWS_STORAGE_BUCKET_NAME = 'photorizer'

    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    # For use with http:
    # MEDIA_URL = '//s3.amazonaws.com/%s/media/' % AWS_STORAGE_BUCKET_NAME
    # For use with https:
    MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    # For use with http:
    # STATIC_URL = '//s3.amazonaws.com/%s/static/' % AWS_STORAGE_BUCKET_NAME
    # For use with https:
    STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
    ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

    BOOTSTRAP3 = {
        'jquery_url': urljoin(STATIC_URL, 'jquery-1.11.1.min.js'),
        # 'jquery_url': '/var/www/photorizer/static/jquery.min.js',
        'base_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/'),
        # 'base_url': '/var/www/photorizer/static/bootstrap-3.2.0-dist/',
        # 'css_url': None,
        'theme_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/css/bootstrap.min.css'),
        # 'theme_url': '/var/www/photorizer/static/bootstrap-3.2.0-dist/css/bootstrap-theme.min.css',
        'css_url': urljoin(STATIC_URL, 'bootstrap-3.2.0-dist/css/custom.css'),
        'javascript_url': None,
        'javascript_in_head': False,
        'include_jquery': True,
        'horizontal_label_class': 'col-md-2',
        'horizontal_field_class': 'col-md-4',
        'set_required': True,
        'form_required_class': '',
        'form_error_class': '',
        'form_renderers': {
            'default': 'bootstrap3.renderers.FormRenderer',
            },
        'formset_renderers':{
            'default': 'bootstrap3.renderers.FormsetRenderer',
            },
        'field_renderers': {
            'default': 'bootstrap3.renderers.FieldRenderer',
            'inline': 'bootstrap3.renderers.InlineFieldRenderer',
            },
        }