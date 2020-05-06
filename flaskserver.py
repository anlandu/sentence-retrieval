#https://flask.palletsprojects.com/en/1.1.x/quickstart/#apis-with-json
from flask import Flask, request, send_from_directory
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


def query_recommendations(q, score_func, n=10):
    #https://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python    
    print('QUERYING "{1}" FOR {0} DOCUMENTS USING {2}'.format(n, q, score_func)) 
    results = [h.highlights("content") for h in list(search_index(q, score_func, 'retrieval/sentence_index'))[:n]]
    return [i for i in results if len(i) > 0]

@app.route('/<path:path>')
def send_js(path):
    return send_from_directory('frontend/dist', path)

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
    query="default"
    if request.method == 'POST':
        query = request.form['query']
        score_func = request.form['score_func']
    return {
        "recommendations" : query_recommendations(query, score_func)
    }# was GET or the credentials were invalid
