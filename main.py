import numpy as np
import time
import Document
import porter
import TextRepresenter
import Parser
import ParserCACM
from index import *
from weighter import *
from modeles import *
from evaluation import *
from QueryParser import *

t = time.time()
index = Index("test",index_link="index/test_index", stems_link="index/test_inverted_index",index_doc = "index/test_doc",stems_doc="index/test_inverted_doc")

print("Index Start")
#index.indextion(souprint("TESTTEST")rce = 'cacm/cacm.txt')
print("Index End, time :",time.time() - t)
t = time.time()
print("Index_Inverse Start")
#index.indextion_inverse(source = 'cacm/cacm.txt')
print("Index_Inverse End, time :",time.time() - t)
t = time.time()

print(type(index.getTsForStem('inform')))
print(type(index.getTfdForDoct('10')))

porter = TextRepresenter.PorterStemmer()
query="What difficulties are involved in automatically retrieving articles from approximate titles?"

#query="What is love"

query = porter.getTextRepresentation(query)
#print(query.keys())


#print("\n DOC ",weighter.getDocWeightsForDoc('1'))
#print("\n Stem ",weighter.getDocWeightsForStem('engin'))
#print("\n Query ",weighter.getWeightsForQuery(query))
#print(score.items())
print("START EVA")

query_parser = QueryParser(TextRepresenter.PorterStemmer())
query_parser.initQry('cacm/cacm.qry')
query_parser.initRel('cacm/cacm.rel')

#print(query_parser.nextDocument().text)

weighter = Weighter_03(index)
vect = Vectoriel(index, weighter, normalized = False)
query = query_parser.nextQuery()
docs = vect.getRanking(query.get_query())
irlist = IRList(query, docs)
print(EvalMeasure.eval_ap(irlist))

print("ENDEND")
