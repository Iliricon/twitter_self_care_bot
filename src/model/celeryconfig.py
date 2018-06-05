BROKER_TRANSPORT = "sqlakombu.transport.Transport"
BROKER_HOST = "sqlite:///celerydb.sqlite"
CELERY_RESULT_BACKEND = "database"
CELERY_RESULT_DBURI = "sqlite:///celerydb.sqlite"
CELERY_RESULT_ENGINE_OPTIONS = {"echo": True}
