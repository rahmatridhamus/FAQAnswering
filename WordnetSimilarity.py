from nltk.corpus import wordnet
from itertools import product

def findMaxScore(synset1, synset2):
    maxscore = 0
    for i, j in list(product(*[synset1, synset2])):
        score = i.path_similarity(j)  # Wu-Palmer Similarity
        if score != None:
            maxscore = (score if maxscore < score else maxscore)
    return maxscore

def similarityBetweenWord(quest1, quest2):
    hasil = []
    temp = []
    for word1 in quest1:
        for word2 in quest2:
            synset1 = wordnet.synsets(word1[0])
            synset2 = wordnet.synsets(word2[0])
            score = findMaxScore(synset1, synset2)
            temp.append(score)
        hasil.append(temp)
        temp = []
    return hasil