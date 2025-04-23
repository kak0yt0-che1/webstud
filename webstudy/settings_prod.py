from .settings import *
import dj_database_url

DEBUG = False

ALLOWED_HOSTS = ['your-domain.com', 'webstud.onrender.com']

DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}
