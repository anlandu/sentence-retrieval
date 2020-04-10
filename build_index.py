import os
from retrieval.sentence_index import make_clean_index
DATA_DIR='data/scisummnet'
INDEX_DIR='retrieval/sentence_index'
def initialize():
    if not os.path.exists(DATA_DIR):
        #https://stackoverflow.com/questions/3777301/how-to-call-a-shell-script-from-python-code/3777308
        print('DOWNLOADING SCISUMMNET')
        os.system('sh ./data/download_data.sh')
    if not os.path.exists(INDEX_DIR):
        os.mkdir(INDEX_DIR)
        print('BUILDING INDEX AT "{0}"'.format(INDEX_DIR))
        make_clean_index(INDEX_DIR)
    print("build index complete")

initialize()