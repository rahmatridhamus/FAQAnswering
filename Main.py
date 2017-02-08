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


def process(data):
    # start time count
    start_time = time.time()

    a = 0.5
    iteri = 0
    # current question processing
    questFromUser = data
    preQuestFromUser = pre.preprocs(questFromUser)

    print('------- Input -------')
    print(questFromUser, ' : ', preQuestFromUser)

    # dataset question processing
    questDataset, answerDataset = pre.openFile("Dataset Gabung.xlsx")
    prequestDataset, preAnswerDataset = [], []

    # Generating TFIDF to CSV
    # tfidf.generateTFIDF()

    # Start Checking
    for i in range(len(answerDataset)):
        # a = pre.preprocs(answerDataset[i])
        q = pre.preprocs(questDataset[i])
        prequestDataset.append(q)
        # preAnswerDataset.append(a)

    print('Data set loaded',len(prequestDataset))

    similiarity = []
    # similiarityCosine = []
    # similiarityBipartite = []
    for item in prequestDataset:
        iteri += 1
        print(iteri,"yang diteliti: ",item)

        # semantic similarity processing, wordnet similarity antar kata -->  bipartite mapping
        Q1 = wn.similarityBetweenWord(preQuestFromUser, item)
        Q2 = wn.similarityBetweenWord(item, preQuestFromUser)
        scoreBipartite = bipartite(Q1, Q2)

        # statistic similarity processing, TF-IDF antar kata --> cosine similarity
        tfidf1, tfidf2 = tfidf.getTfidfQuestion(preQuestFromUser, item,iteri)

        scoreCosine = cosineSimilarity(tfidf1, tfidf2)

        overall = a*scoreBipartite+(1-a)*scoreCosine
        overallCosine = scoreCosine
        overallBipartite = scoreBipartite

        similiarity.append(overall)
        print("Cosine: ",overallCosine)
        print("Bipartite: ",overallBipartite)
        print("Overall: ",overall)
        print()

    answer = answerDataset[similiarity.index(max(similiarity))]
    print('------------ Question ------------')
    print(data)
    print('------------ Answer ------------')
    print(answer,". with similarity value: ",max(similiarity))
    print("--- %s seconds ---" % (time.time() - start_time))
    return answer

process("who are you dude?")
