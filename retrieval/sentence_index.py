import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh.qparser import OrGroup
import xml.etree.ElementTree as ET
from os import listdir

ROOT_PATH = 'data/scisummnet/top1000_complete/'


def get_doc_ids():
    ids = listdir(ROOT_PATH)
    return ids


def make_clean_index(dirname):
    # Always create the index from scratch
    ix = index.create_in(dirname, schema=get_schema())
    writer = ix.writer()

    # Assume we have a function that gathers the filenames of the
    # documents to be indexed
    for path in get_doc_ids():
        add_doc(writer, path)

    writer.commit()


def get_schema():
    return Schema(id=ID(unique=True, stored=True), content=TEXT(stored=True))


def add_doc(writer, id):
    path = ROOT_PATH + id
    doc_tree = ET.parse(path + '/Documents_xml/' + id + '.xml')
    doc_root = doc_tree.getroot()

    i = 0
    for section in doc_root:
        # print(section.tag, section.attrib)
        for sent in section:
            writer.add_document(id=str(id)+str(i), content=sent.text)
            i += 1
    #summary_tree = ET.parse(path + '/summary/' + id + '.gold.txt')
    #summary_root = summary_tree.getroot()


def search_index(query, dirname):
    ix = index.open_dir(dirname, schema=get_schema())
    og = OrGroup.factory(0.9)
    qp = QueryParser("content", schema=get_schema(), group=og)
    qp.add_plugin(FuzzyTermPlugin())
    q = qp.parse(query)
    searcher = ix.searcher()
    results = searcher.search(q, limit=None)
    results.fragmenter.surround = 100
    return results


def main():
    ix_dir = 'sentence_index'
    # make_clean_index(ix_dir)
    r = search_index(
        "Comparisons against related algorithms are also conducted.", ix_dir)
    print(len(r))
    for result in r[:10]:
        print(result.highlights("content"))

if __name__ == '__main__':
    main()
