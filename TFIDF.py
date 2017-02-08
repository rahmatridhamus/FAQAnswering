import math

import Preprocessing as pre
import nltk
import string
import numpy
import csv
from itertools import chain


def getCorpus(questDataset):
    prequestDataset = []
    # questDataset, answerDataset = pre.openFile("Dataset Gabung.xlsx")
    for i in range(len(questDataset)):
        q = pre.preprocs(questDataset[i])
        term, tag = zip(*q)
        prequestDataset.append(term)
        wordDict = []
        wordDict = list(chain(*prequestDataset))

    return wordDict


def getUniqueWords(allWords):
    uniqueWords = []
    for i in allWords:
        if not i in uniqueWords:
            uniqueWords.append(i)
    return uniqueWords


def column(matrix, i):
    return [row[i] for row in matrix]


def generateTFIDF():
    questDataset, answerDataset = pre.openFile("Dataset Gabung.xlsx")
    terms = []
    questCorpus = []
    stringKata = ""
    prequestDataset = []
    tfidfVal = []
    for i in range(len(questDataset)):
        q = pre.preprocs(questDataset[i])
        term, tag = zip(*q)
        prequestDataset.append(term)
        terms = list(chain(*prequestDataset))
        stringKata = nltk.re.sub('[%s]' % nltk.re.escape(string.punctuation), '', questDataset[i])
        questCorpus.append(stringKata.lower())

    for i in range(len(questCorpus)):
        for j in range(len(terms)):
            tfidfVal.append(tf_idf(terms[j], questCorpus[i], questCorpus))

    tfidfVal = numpy.array(tfidfVal)
    result = numpy.reshape(tfidfVal, (len(questCorpus), len(terms)))

    result = result.tolist()
    for i, x in enumerate(questCorpus):
        result[i].insert(0, x)

    terms = getUniqueWords(terms)
    terms.insert(0, '')
    result.insert(0, terms)
    with open('tfidfres.csv', 'w', newline='') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(result)


def freq(word, doc):
    return doc.count(word)


def word_count(doc):
    return len(doc)


def tf(word, doc):
    return (freq(word, doc) / float(word_count(doc)))


def num_docs_containing(word, list_of_docs):
    count = 0
    for document in list_of_docs:
        if freq(word, document) > 0:
            count += 1
    return 1 + count


def idf(word, list_of_docs):
    return math.log(len(list_of_docs) /
                    float(num_docs_containing(word, list_of_docs)))


def tf_idf(word, doc, list_of_docs):
    return (tf(word, doc) * idf(word, list_of_docs))


def getTfidfQuestion(quest1, quest2, indexes):
    tfidfq1 = []
    tfidfq2 = []
    with open('tfidfres.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)

    terms = data[0]
    corpus = data[1::]
    questCorpus = [i[0] for i in data]

    words1 = [(i[0]) for i in quest1]
    words2 = [(i[0]) for i in quest2]

    allWords = getUniqueWords(words1 + words2)
    # print(terms)

    for i in range(len(allWords)):
        s = allWords[i]
        # print(terms.index(s))
        if (s in words1):
            if(s in terms):
                termIndex = terms.index(s)
                tfidfq1.append(float(corpus[indexes-1][termIndex]))
                # tfidfq1.append(int(1))
            else:
                tfidfq1.append(float (0))
        else:
            tfidfq1.append(float (0))

        if (s in words2):
            if (s in terms):
                termIndex = terms.index(s)
                tfidfq2.append(float(corpus[indexes-1][termIndex]))
                # tfidfq2.append(int(1))

            else:
                tfidfq2.append(float (0))
        else:
            tfidfq2.append(float (0))

    # print(questCorpus[indexes])
    print(allWords)
    print(tfidfq1)
    print(tfidfq2)
    return tfidfq1,tfidfq2
