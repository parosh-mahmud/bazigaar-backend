
from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'tlh41ft#rz3_f4v)2d17v@$+!%f$t*k*f=%98xlfb_ywix0)34'
DEBUG = True
ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CORS_ALLOW_CREDENTIALS = True
INSTALLED_APPS = [
    'django.contrib.sites',
    # 'rest_framework_swagger',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'knox',

    # Third party app
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'dj_rest_auth',
    'drf_yasg',

    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',

    # farhan
    'Lottery',

    # admin
    'SuperAdminPanel',
    'AdminPanel',
    'AgentPanel',

    # base is a app where own build code and packages is written
    "base",

    # my_app
    'user_app',
    'follow',
    'chat_with_friend',
    'chat_in_group',
    'livestream',
    'notifications',
    'reseller_app',
    'reseller_payment_method',
    'level_and_achievement',
    'leaderboard',
    'wallet_app',

    'HostApp',
    'SliderApp',
    'spinning_game',

    # 'calling_app',
    'calling_app2',
    'group_call',

    # ticket
    'ticket_draw_app',
    'contact_us',


    # live event
    'server_sent_event',
    'website',


]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.UserAchivementMiddleware',
]

ROOT_URLCONF = 'configurations.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'configurations.wsgi.application'
ASGI_APPLICATION = 'configurations.asgi.application'

DATABASES = {

    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': 'bazigaar',
    #     'USER': 'bazigaar',
    #     'PASSWORD': 'Arif@125',
    #     'HOST': 'db',
    #     'PORT': '5432',
    # }

    'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': BASE_DIR / 'db.sqlite3',
    }
}

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
# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ORIGIN_ALLOW_ALL = True


# CORS_ALLOWED_ORIGINS = [
#   'http://18.136.192.25:3000','http://localhost:3000',
# ]
CSRF_TRUSTED_ORIGINS = ['https://api.bazigaar.com']
# CORS_ALLOW_HEADERS = [
# 'accept',
# 'accept-encoding',
# 'authorization',
# 'content-type',
# 'dnt',
# 'origin',
# 'user-agent',
# 'x-csrftoken',
# 'x-requested-with',
# ]

AUTH_USER_MODEL = "user_app.User"
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'hog3rider474@gmail.com'
EMAIL_HOST_PASSWORD = 'nxgffwnayctrlcsy'
# EMAIL_HOST = 'smtp.office365.com'
# EMAIL_HOST_USER = 'support@bazigaar.com'
# EMAIL_HOST_PASSWORD = 'Toby7799$'



STATIC_URL = '/static/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATIC_ROOT = os.path.join(BASE_DIR, '/static/upload')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


REST_FRAMEWORK = {
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 20,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    # 'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication',),

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'user_app.custom_auth.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'knox.auth.TokenAuthentication',

        # 'rest_framework.authentication.TokenAuthentication',

    ],
    'DEFAULT_PAGINATION_CLASS': 'base.paginations.CustomPagination',
}

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': '312607528448-kb5er91g84l06ri2bcad8nt5t2n8cquc.apps.googleusercontent.com',
            'secret': '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',
            'key': 'AIzaSyAjPS4aox4iLY2QmRt7BiAU-b-mkh0PKLU'
        },
        "SCOPE": [
            "profile",
            "email"
            # "https://www.googleapis.com/auth/userinfo.email"
        ],
        "AUTH_PARAMS": {
            "access_type": "online",
        }
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",
)

REST_KNOX = {
    'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
    'AUTH_TOKEN_CHARACTER_LENGTH': 64,
    'TOKEN_TTL': timedelta(days=6),
    'USER_SERIALIZER': 'AdminPanel.serializers.AdminUserSerializer',
    #   'USER_Data': '',
    'TOKEN_LIMIT_PER_USER': None,
    'AUTO_REFRESH': False,
    'EXPIRY_DATETIME_FORMAT': None,
}

REST_AUTH_SERIALIZERS = {
    "LOGIN_SERIALIZER": "user_app.login_serializers.NewLoginSerializer"
}

REST_AUTH_REGISTER_SERIALIZERS = {
    "REGISTER_SERIALIZER": "user_app.register_serializer.NewRegisterSerializer"
}

ACCOUNT_ADAPTER = 'user_app.email.ModifiedAccountAdapter'
ADAPTER = "user_app.email.ModifiedAccountAdapter"
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
# ACCOUNT_USER_MODEL_USERNAME_FIELD = 'email'
USERNAME_REQUIRED = False
ACCOUNT_EMAIL_VERIFICATION = "mandatory"  # None
ACCOUNT_CONFIRM_EMAIL_ON_GET = False
# ACCOUNT_USER_MODEL_USERNAME_FIELD=None
DATA_UPLOAD_MAX_NUMBER_FIELDS = 2000
