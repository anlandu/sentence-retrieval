#https://flask.palletsprojects.com/en/1.1.x/quickstart/#apis-with-json
from flask import Flask, request



app = Flask(__name__)

def query_recommendations(q):
    return [''.join(reversed(q))]

@app.route('/recommendations', methods=['POST', 'GET'])
def recommendations():
    if request.method == 'POST':
        query = request.form['query']
        #add a party for number of recommendations to ask for
        print(request.form)
    # the code below is executed if the request method
    return {
        "recommendations" : query_recommendations(query)
    }# was GET or the credentials were invalid
