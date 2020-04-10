import os.path
from whoosh import index
from whoosh.fields import Schema, ID, TEXT
from whoosh.qparser import QueryParser
from whoosh.qparser import FuzzyTermPlugin
from whoosh.qparser import OrGroup
import xml.etree.ElementTree as ET
from os import listdir

ROOT_PATH = '../data/scisummnet/top1000_complete/'

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
  
  content = ''
  for section in doc_root:
    # print(section.tag, section.attrib)
    for sent in section:
        content += sent.text + '\n'
    
  writer.add_document(id=id, content=content)
  #summary_tree = ET.parse(path + '/summary/' + id + '.gold.txt')
  #summary_root = summary_tree.getroot() 
  
def search_index(query, dirname):
  r_out=[]
  ix=index.open_dir(dirname, schema=get_schema())
  og = OrGroup.factory(0.9)
  qp = QueryParser("content", schema=get_schema(), group=og)
  qp.add_plugin(FuzzyTermPlugin())
  q = qp.parse(query)
  searcher=ix.searcher()
  results=searcher.search(q)
  return results



def main():
  ix_dir='sentence_index'
  make_clean_index(ix_dir) 

  r=search_index("Initially, only the keywords returned by the first ten heuristics are considered.", ix_dir)
  for result in r:
    print(result)

  #print(get_doc_ids())
  '''
  path = ROOT_PATH + 'N07-1011' 
  id = 'N07-1011'
  doc_tree = ET.parse(path + '/Documents_xml/' + id + '.xml')
  doc_root = doc_tree.getroot()
  
  for section in doc_root:
    print(section.tag, section.attrib)
    for sent in section:
        print(sent.text)
  
  for section in doc_root:
    print(section.tag, section.attrib)
    for sent in section:
        print(sent.text)
   '''
if __name__ == '__main__':
  main()
