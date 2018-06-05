from celery import Celery

app = Celery('tweet2vec',
                include=['model.tweet2vec_tasks'])

app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

if __name__ == "__main__":
    app.start()
