import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-tu-clave-secreta-aqui'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'jazzmin',  # <--- JAZZMIN DEBE IR PRIMERO
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gestion',
    'django.contrib.humanize', # Para formatear números con puntos
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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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

# --- CONFIGURACIÓN REGIONAL (ESPAÑOL PARAGUAY) ---
LANGUAGE_CODE = 'es-py'
TIME_ZONE = 'America/Asuncion'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Formato de números (Miles con punto)
USE_THOUSAND_SEPARATOR = True
THOUSAND_SEPARATOR = '.'
DECIMAL_SEPARATOR = ','
NUMBER_GROUPING = 3

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --- CONFIGURACIÓN VISUAL (JAZZMIN) ---
JAZZMIN_SETTINGS = {
    # Títulos y Logos
    "site_title": "Gestor de Cobranzas",
    "site_header": "Gestión",
    "site_brand": "💼 Mi Negocio",
    "welcome_sign": "Bienvenido al Sistema",
    "copyright": "MiGestor",
    
    # Buscador general
    "search_model": "gestion.Cliente",

    # Botón para volver al Dashboard principal
    "topmenu_links": [
        {"name": "🏠 VOLVER AL DASHBOARD", "url": "dashboard", "permissions": ["auth.view_user"]},
    ],

    # Menú lateral
    "show_sidebar": True,
    "navigation_expanded": True,
    
    # Iconos
    "icons": {
        "gestion.Cliente": "fas fa-users",
        "gestion.Venta": "fas fa-shopping-cart",
        "gestion.Pago": "fas fa-hand-holding-usd",
        "auth.User": "fas fa-user-shield",
    },
    
    "order_with_respect_to": ["gestion.Cliente", "gestion.Venta", "gestion.Pago"],

    # --- MODO DIOS (UI BUILDER) ---
    # Esto habilita el botón flotante para probar temas oscuros/claros en vivo
    "show_ui_builder": True, 
}

# --- TEMA VISUAL Y PARCHES ---
JAZZMIN_UI_TWEAKS = {
    "theme": "spacelab", # Tema claro suave por defecto
    #"dark_mode_theme": "darkly", # Descomenta para probar tema oscuro
}

# CONEXIÓN DE TUS ARCHIVOS PERSONALIZADOS
# Aquí cargamos el CSS que arregla el contraste y el JS que automatiza ventas
JAZZMIN_SETTINGS["custom_css"] = "gestion/css/admin_fixes.css"
JAZZMIN_SETTINGS["custom_js"] = "gestion/js/admin_ventas.js"