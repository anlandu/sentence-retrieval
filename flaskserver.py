#https://flask.palletsprojects.com/en/1.1.x/quickstart/#apis-with-json
from flask import Flask, request
from flask_cors import CORS
from retrieval.sentence_index import search_index, make_clean_index
import os
INDEX_DIR = 'retrieval/sentence_index'
DATA_DIR = 'data/scisummnet'

DOWNLOAD_INDEX = True
def initialize():
    if not os.path.exists(INDEX_DIR):
        if DOWNLOAD_INDEX:
            os.system('sh ./retrieval/download_index.sh')
        else:
            # Add code to manually build index
            pass
        
initialize()
app = Flask(__name__)
CORS(app)


def query_recommendations(q, n=10):
    #https://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python    
    print('QUERYING FOR {0} DOCUMENTS USING "{1}"'.format(n, q)) 
    return [h.highlights("content") for h in list(search_index(q, 'retrieval/sentence_index'))[:n]]

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
    query="default"
    if request.method == 'POST':
        query = request.form['query']
        #add a part for number of recommendations to ask for
        print(request.form)
    # the code below is executed if the request method
    return {
        "recommendations" : query_recommendations(query)
    }# was GET or the credentials were invalid
