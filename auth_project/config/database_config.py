import os

_POSTGRES_USER = os.environ.get("_POSTGRES_USER", "postgres")
_POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "postgrespassword")
_POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "postgres")
_POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
_POSTGRES_DATABASE = os.environ.get("POSTGRES_DATABASE", "postgres")

POSTGRES_DATABASE_CONFIG = {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': _POSTGRES_DATABASE,
    'USER': _POSTGRES_USER,
    'PASSWORD': _POSTGRES_PASSWORD,
    'HOST': _POSTGRES_HOST,
    'PORT': _POSTGRES_PORT,
}
