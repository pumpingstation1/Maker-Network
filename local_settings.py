import os

DEBUG = True

ADMINS = (
	('Eric Stein', 'toba@des.truct.org'),
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '3kdsjfoiewajfoiewajfOESRghjwowejgoewhFH383'

MEDIA_SERVE = False
MEDIA_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'media'))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME' : 'site.db'
    }
}

#EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = 'smtp.truct.org'
#EMAIL_PORT = 465
#EMAIL_HOST_USER = ''
#EMAIL_HOST_PASSWORD = ''
#EMAIL_USE_TLS = True
