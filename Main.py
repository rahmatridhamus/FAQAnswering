from math import pow, sqrt

import Preprocessing as pre
import WordnetSimilarity as wn
import numpy as np
import TFIDF as tfidf
import time


def bipartite(Q1, Q2):
    temp = []
    for item in Q1:
        temp.append(max(item))
    word1 = sum(temp) / len(Q1)

    temp = []
    for item in Q2:
        temp.append(max(item))
    word2 = sum(temp) / len(Q2)

    return 0.5 * (word1 + word2)


def cosineSimilarity(idf1, idf2):
    a = np.dot(idf1, idf2)
    b = np.linalg.norm(idf1) * np.linalg.norm(idf2)
    if (a == 0):
        return 0
    else:
        return a / b


def chiSquareStat(tfVector1, tfVector2):
    result = 0
    sumX = getSum(tfVector1)
    sumY = getSum(tfVector2)
    h = sumX + sumY

    locResX = 0
    locResY = 0
    for i in range(len(tfVector1)):
        sqrtX = pow(tfVector1[i], 2)
        sqrtY = pow(tfVector2[i], 2)

        locResX += sqrtX/(sumX * (tfVector1[i] + tfVector2[i]))
        locResY += sqrtY / (sumY * (tfVector1[i] + tfVector2[i]))

    result = (h*(locResX+locResY))-h
    return sqrt(result)


def getSum(tfVector):
    sumVal = 0
    for i in range(len(tfVector)):
        sumVal += tfVector[i]
    return sumVal


def chi2Cosine(idf1, idf2):
    cosVal = cosineSimilarity(idf1, idf2)
    chiVal = chiSquareStat(idf1, idf2)
    a = 0.5
    return (a * cosVal) + (1 - a) * chiVal


def process(data):
    # start time count
    start_time = time.time()

    a = 0.7  # konstanta proporsional polarisasi
    iteri = 0  # iterasi

    # current question processing
    questFromUser = data
    preQuestFromUser = pre.preprocs(questFromUser)

    print('------- Input -------')
    print(questFromUser, ' : ', preQuestFromUser)

    # dataset question processing
    questDataset, answerDataset = pre.openFile("Dataset Gabung.xlsx")
    # questDataset, answerDataset = pre.openFile("Dataset NLP2.xlsx")
    prequestDataset, preAnswerDataset = [], []

    # Generating TFIDF to CSV
    # tfidf.generateTFIDF()

    # Start Checking
    bestChi = 0
    tempChi = ""
    for i in range(len(answerDataset)):
        # a = pre.preprocs(answerDataset[i])
        q = pre.preprocs(questDataset[i])
        prequestDataset.append(q)
        # preAnswerDataset.append(a)

    print('Data set loaded', len(prequestDataset))

    similiarity = []
    # similiarityCosine = []
    # similiarityBipartite = []
    for item in prequestDataset:
        iteri += 1
        print(iteri, "yang diteliti: ", item)

        # semantic similarity processing, wordnet similarity antar kata -->  bipartite mapping
        Q1 = wn.similarityBetweenWord(preQuestFromUser, item)
        Q2 = wn.similarityBetweenWord(item, preQuestFromUser)
        scoreBipartite = bipartite(Q1, Q2)

        # statistic similarity processing, TF-IDF antar kata --> cosine similarity
        tfidf1, tfidf2 = tfidf.getTfVector(preQuestFromUser, item, questDataset)

        # scoreCosine = cosineSimilarity(tfidf1, tfidf2)
        scoreCosine = chi2Cosine(tfidf1, tfidf2)

        overall = a * scoreBipartite + (1 - a) * scoreCosine
        overallCosine = scoreCosine
        overallBipartite = scoreBipartite

        similiarity.append(overall)
        if(bestChi<overallCosine):
            bestChi = overallCosine
            tempChi = ""+str(overallCosine)+", from "+str(item)
        # print("Cosine: ", overallCosine)
        print("Chisquare: ", overallCosine)
        print("Bipartite: ", overallBipartite)
        print("Overall: ", overall)
        print()


    print("best Chi, ",tempChi)
    answer = answerDataset[similiarity.index(max(similiarity))]
    print('------------ Question ------------')
    print(data)
    print('------------ Answer ------------')
    print(answer, ". with similarity value: ", max(similiarity))
    print("--- %s seconds ---" % (time.time() - start_time))
    return answer


# masukkan pertanyaan
process("who are you?")
