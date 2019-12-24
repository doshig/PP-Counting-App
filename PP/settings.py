"""
Django settings for SFA project.

Generated by 'django-admin startproject' using Django 2.0.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '39c&10x(cm5z*-5n-^5%*6i!4vjrwjt_f-o8m(wod1z$@kbx6a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    # 'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jquery',
    'django_python3_ldap', #Active Directory authentication
    'rest_framework',
    'import_export',
    'django.contrib.humanize',
    'Homepage',
    'CountingLog',
    'DepartmentLog',
    'Reportview',
    'LABLog',
    'django.contrib.admin', ##This must be after 'TrainingLog' so logout process TrainingLog logged_out.html, and not Django Admin logout

]

IMPORT_EXPORT_USE_TRANSACTIONS = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PP.urls'

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

WSGI_APPLICATION = 'PP.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

AUTHENTICATION_BACKENDS = [
        
        "django_python3_ldap.auth.LDAPBackend", ###If you want Active Directory users to be able to log in
    "django.contrib.auth.backends.ModelBackend", ###If you want Django users to be able to log in 
        ]

LDAP_AUTH_FORMAT_USERNAME = "django_python3_ldap.utils.format_username_active_directory"
LDAP_AUTH_ACTIVE_DIRECTORY_DOMAIN = "MSAEROSPACE" ##Works needed for msaerospace\username login scheme


##Can be foudn in DC2 - > Active Directory Users and Computers -> Users -> pick a user -> Attribut Editor
LDAP_AUTH_USER_FIELDS = {
    "username": "sAMAccountName", #correct
    "first_name": "givenName", #correct
    "last_name": "sn", #correct
    "email": "mail", #correct
}

LDAP_AUTH_OBJECT_CLASS = "users"
LDAP_AUTH_USER_LOOKUP_FIELDS = ('username',)



#LDAP_AUTH_URL = 'ldap://DC2.msaerospace.local:389' ## SEEMS TO BE WORKING; 
#LDAP_AUTH_URL = 'ldap://DC2:389' ## SEEMS TO BE WORKING; do not use port 389 that sends PW in the clear
LDAP_AUTH_URL = 'ldap://10.1.1.28:389' ## SEEMS TO BE WORKING; do not use port 389 that sends PW in the clear
#LDAP_AUTH_URL = 'ldap://10.1.1.29:636' ## NOT WORKING; do not use port 389 that sends PW in the clear
##From DC2 - > CMD - > dsquery user -name administrator, drop CN=administrator
#LDAP_AUTH_SEARCH_BASE = "CN=Users, DC=msaerospace,DC=local" ##This no longer works as of 05/28/19 as some users are now separated into departments
'''This will search top level active directory, parsing through all sub folders. This is the most broad search'''
LDAP_AUTH_SEARCH_BASE = "DC=msaerospace,DC=local"
#this is from 10.1.1.24 Active Directory - > Domain Controllers -> Attribute Editor
#this is from 10.1.1.24 Active Directory - > msaerospace.local side bar -> properties -> attribute editor

#LDAP_AUTH_USE_TLS=True
LDAP_AUTH_CONNECTION_USERNAME = None
LDAP_AUTH_CONNECTION_PASSWORD = None



## DC2 - > Active Director Users and Computers -> Pick a User -> Attribut Editor -> objectClass
LDAP_AUTH_OBJECT_CLASS = "organizationalPerson"


REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'US/Pacific'


USE_I18N = True

USE_L10N = True

USE_THOUSAND_SEPARATOR = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = r'C:\Users\tastetf\Desktop\DjangoPP\PP\static'
