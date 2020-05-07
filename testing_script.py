from retrieval.sentence_index import search_index, make_clean_index
import requests
import json
import csv

n=10 #number of top results to record
score_funcs=['ok', 'bm25f', 'pln', 'tfidf', 'freq']
lens=[0,0,0,0,0]
with open(f"test_results_top_{n}.csv", "w", encoding="utf-8", newline='') as csv_out:
    writer=csv.writer(csv_out)
    i=0
    with open("nlp_abstracts_100.txt", encoding="utf-8") as query:
        for line in query.readlines():
            i+=1
            writer.writerow([f"Query {i}: {line}"])
            j=0
            for func in score_funcs:
                j+=1
                writer.writerow([f"Scoring Function {j}"])
                data={"query":line, "score_func":func}
                results=requests.post("http://127.0.0.1:5000/recommendations", data=data)
                for rec in json.loads(results.content)["recommendations"][:n]:
                    lens[j-1]+=len(rec.split(" "))
                    writer.writerow([rec])
            writer.writerow([])
        writer.writerow(lens)
