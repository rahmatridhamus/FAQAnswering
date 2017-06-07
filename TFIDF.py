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


def generateTF(questDatasetParams):
    # print(len(questDataset))
    terms = []
    questCorpus = []
    stringKata = ""
    prequestDataset = []
    tfVal = []
    questDataset = []
    answerDataset = []

    questDataset = questDatasetParams
    for i in range(len(questDataset)):
        q = pre.preprocs(questDataset[i])
        term, tag = zip(*q)
        prequestDataset.append(term)
        terms = list(chain(*prequestDataset))
        stringKata = nltk.re.sub('[%s]' % nltk.re.escape(string.punctuation), '', questDataset[i])
        questCorpus.append(stringKata.lower())

    # print(questCorpus)
    # print()
    # print(terms)

    # for word in terms:
    #     tfVal.append(word,freq(word,terms))
    tfVal = [(word, freq(word, terms)) for word in getUniqueWords(terms)]
    return (tfVal)



def generateTFIDF():
    questDataset, answerDataset = pre.openFile("Dataset Gabung.xlsx")
    print("len dataset ",len(questDataset))
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
        for j in range(len(getUniqueWords(terms))):
            tfidfVal.append(tf_idf(terms[j], questCorpus[i], questCorpus))

    tfidfVal = numpy.array(tfidfVal)
    # print("len tfidfval ",len(tfidfVal))
    result = numpy.reshape(tfidfVal, (len(questCorpus), len(getUniqueWords(terms))))

    result = result.tolist()
    # print("len row result ",len(result))
    # print("len column result ",len(result[0]))

    terms = getUniqueWords(terms)
    # print("len long terms",len(terms))
    for i, x in enumerate(questCorpus):
        result[i].insert(0, x)

    terms.insert(0, '')
    result.insert(0, terms)
    # print()
    # print(len(result))
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


def getTfVector(quest1, quest2, questdatasetParams):
    tfq1 = []
    tfq2 = []

    terms,freqs = zip(*generateTF(questdatasetParams))

    words1 = [(i[0]) for i in quest1]
    words2 = [(i[0]) for i in quest2]

    allWords = getUniqueWords(words1 + words2)
    # print(terms)

    for i in range(len(allWords)):
        s = allWords[i];

        if(s in words1):
            if(s in terms):
                index = terms.index(s)
                tfq1.append(freqs[index])
            else: tfq1.append(int(0))
        else:tfq1.append(int(0))

        if (s in words2):
            if (s in terms):
                index = terms.index(s)
                tfq2.append(freqs[index])
            else: tfq2.append(int(0))
        else:tfq2.append(int(0))


    print(allWords)
    print(tfq1)
    print(tfq2)

    return tfq1, tfq2


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
            if (s in terms):
                termIndex = terms.index(s)
                tfidfq1.append(float(corpus[indexes - 1][termIndex]))
                # tfidfq1.append(int(1))
            else:
                tfidfq1.append(float(0))
        else:
            tfidfq1.append(float(0))

        if (s in words2):
            if (s in terms):
                termIndex = terms.index(s)
                tfidfq2.append(float(corpus[indexes - 1][termIndex]))
                # tfidfq2.append(int(1))

            else:
                tfidfq2.append(float(0))
        else:
            tfidfq2.append(float(0))

    # print(questCorpus[indexes])
    print(allWords)
    print(tfidfq1)
    print(tfidfq2)
    return tfidfq1, tfidfq2
