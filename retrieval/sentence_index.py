import xml.etree.ElementTree as ET
from os import listdir, mkdir
import shutil


from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh.qparser import OrGroup
from whoosh.scoring import BM25F, TF_IDF, Frequency
from whoosh.writing import AsyncWriter
from whoosh import analysis

from .scoring import OkBM25, PLN

ROOT_PATH = 'data/scisummnet/top1000_complete/'


def get_doc_ids():
    ids = listdir(ROOT_PATH)
    return ids


def make_clean_index(dirname):
    if index.exists_in(dirname):
        shutil.rmtree(dirname)
    mkdir(dirname)
    # Always create the index from scratch
    ix = index.create_in(dirname, schema=get_schema())
    writer = ix.writer()

    # Assume we have a function that gathers the filenames of the
    # documents to be indexed
    for path in get_doc_ids():
        add_doc(path, writer)
    writer.commit()


def get_schema():
    return Schema(id=ID(unique=True, stored=True),
                  content=TEXT(stored=True, analyzer=analysis.StemmingAnalyzer()))


def add_doc(id, writer):
    path = ROOT_PATH + id
    doc_tree = ET.parse(path + '/Documents_xml/' + id + '.xml')
    doc_root = doc_tree.getroot()

    i = 0
    for section in doc_root:
        # print(section.tag, section.attrib)
        for sent in section:
            if 30 < len(sent.text) < 120:
                writer.add_document(id=str(id)+str(i), content=sent.text)
                i += 1
    #summary_tree = ET.parse(path + '/summary/' + id + '.gold.txt')
    #summary_root = summary_tree.getroot()


def search_index(query, score_func_name, dirname):
    ix = index.open_dir(dirname, schema=get_schema())
    og = OrGroup.factory(0.9)
    qp = QueryParser("content", schema=get_schema(), group=og)
    # qp.add_plugin(FuzzyTermPlugin())
    # query = ' '.join([(x + '~' if len(x) > 5 else x) for x in query.split(' ')])
    q = qp.parse(query)
    score_func = OkBM25()
    if score_func_name == 'ok':
        score_func = OkBM25()
    elif score_func_name == 'bm25f':
        score_func = BM25F()
    elif score_func_name == 'pln':
        score_func = PLN()
    elif score_func_name == 'tfidf':
        score_func = TF_IDF()
    elif score_func_name == 'freq':
        score_func = Frequency()
    searcher = ix.searcher(weighting=score_func)
    results = searcher.search(q, limit=None)
    results.fragmenter.surround = 100
    return results


def main():
    ix_dir = 'retrieval/sentence_index'
    # make_clean_index(ix_dir)
    r = search_index(
        "Comparisons against related algorithms are also conducted.", 'ok', ix_dir)
    print(len(r))
    for result in r[:10]:
        print(result.highlights("content"))


if __name__ == '__main__':
    main()
