import argparse
from data.main import load_data
from data.main import preprocessing
from model.main import build_model
from model.main import test_model
from server import runserver

def gather_data(*data_file):
    pass

def preprocessing(data_file):
    pass

def build_model():
    pass

def test_model():
    pass

def runserver():
    pass

parser = argparse.ArgumentParser(description='Runs the application')

parser.add_argument("--gatherdata", help="commands the application to gather data from twitter", action="store_true")
args = parser.parse_args()

if args.gatherdata:
    load_data('data/dataset/depression_tagged/60Users_annotations.csv', 'data/dataset/full_tweets_depression.pickle')



