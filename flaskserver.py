#https://flask.palletsprojects.com/en/1.1.x/quickstart/#apis-with-json
from flask import Flask, request
from retrieval.sentence_index import search_index


app = Flask(__name__)

def query_recommendations(q, n=10):
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
