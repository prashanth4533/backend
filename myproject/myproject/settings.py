

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent



SECRET_KEY = 'django-insecure-y6(i=8aa2o3(@=cn!6^k4(w_jg%sjj+w84d8i=xfd#b^vkb9dg'

DEBUG = True

ALLOWED_HOSTS = []



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 'rest_framework',
    'accounts','rest_framework.authtoken','corsheaders',
]
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # Change to IsAuthenticated or IsAdminUser in production
    ],
}



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    
]

ROOT_URLCONF = 'myproject.urls'

CORS_ALLOW_HEADERS = [
    'content-type',
    'Authorization',
    'X-Requested-With',
    'Access-Control-Allow-Headers',
]

CORS_ALLOW_METHODS = [
    "GET",
    "POST",
    "PUT",
    "DELETE",
    "OPTIONS",
]
CORS_ALLOWED_ORIGINS = [
      "http://localhost:3000",  # Add the origin of your frontend
  ]
CORS_ALLOW_CREDENTIALS = True # Crucial: Allow credentials
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

WSGI_APPLICATION = 'myproject.wsgi.application'

# settings.py

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'  # SMTP server for Gmail
EMAIL_PORT = 587  # SMTP port for Gmail
EMAIL_USE_TLS = True  # Use TLS for secure connection
EMAIL_HOST_USER = 'your-email@gmail.com'  # Your Gmail address
EMAIL_HOST_PASSWORD = 'your-email-password'  # Your Gmail app password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Default sender email address
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'prashanththiyagu3@example.com'

# Password reset settings
PASSWORD_RESET_TIMEOUT = 14400
# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# settings.py
PAYPAL_CLIENT_ID = "ATqitXJDc5JNEb2DrEQY0Qa5KykfjEsjYT2eKLRzmEHNPO0tUS-ELHIOC6C4eboU-J7kGmSw4Fe7CZ4j"
PAYPAL_SECRET = "ATqitXJDc5JNEb2DrEQY0Qa5KykfjEsjYT2eKLRzmEHNPO0tUS-ELHIOC6C4eboU-J7kGmSw4Fe7CZ4j"
PAYPAL_API_URL = "https://sandbox.paypal.com/sdk/js?client-id=ATqitXJDc5JNEb2DrEQY0Qa5KykfjEsjYT2eKLRzmEHNPO0tUS-ELHIOC6C4eboU-J7kGmSw4Fe7CZ4j"  # Use live endpoint for production


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}