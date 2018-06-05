from .celery import app
from .word2vecReader import Word2Vec

model = None

@app.task
def load_model():
    model_path = "model/word2vec_twitter_model.bin"
    print("Loading the model, this can take some time...")
    model = Word2Vec.load_word2vec_format(model_path, binary=True)
    print("The vocabulary size is: "+str(len(model.vocab)))


@app.task
def query(string):
    if model is None:
        return None
    else:
        return model[string]

