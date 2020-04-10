#https://flask.palletsprojects.com/en/1.1.x/quickstart/#apis-with-json
from flask import Flask, request
from flask_cors import CORS
from retrieval.sentence_index import search_index, make_clean_index
import os
INDEX_DIR = 'retrieval/sentence_index'
DATA_DIR = 'data/scisummnet'

def initialize():
    if not os.path.exists(DATA_DIR):
        #https://stackoverflow.com/questions/3777301/how-to-call-a-shell-script-from-python-code/3777308
        print('DOWNLOADING SCISUMMNET')
        os.system('sh ./data/download_data.sh')
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        print('BUILDING INDEX AT "{0}"'.format(INDEX_DIR))
        make_clean_index(INDEX_DIR)

initialize()
app = Flask(__name__)
CORS(app)


def query_recommendations(q, n=10):
    #https://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python    
    print('QUERYING FOR {0} DOCUMENTS USING "{1}"'.format(n, q)) 
    return [h['content'] for h in list(search_index(q, 'retrieval/sentence_index'))[:n]]

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
