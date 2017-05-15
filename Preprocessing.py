import xlrd
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.stem.wordnet import WordNetLemmatizer

quiz=[]
answer =[]

ps=PorterStemmer()
stop_words = set(stopwords.words('english'))
lmtzr = WordNetLemmatizer()

def openFile(namaFile) :
    workbook = xlrd.open_workbook(namaFile)
    sheet = workbook.sheet_by_index(0)
    for x in range(sheet.nrows):
        for y in range(sheet.ncols):
            if y==0 :
                quiz.append(sheet.cell(x,y).value)
            else :
                answer.append(sheet.cell(x,y).value)
    return quiz,answer

def turnTaggingToWordNet(tagging) :
        if tagging.startswith('J'):
            return wordnet.ADJ
        elif tagging.startswith('V'):
            return wordnet.VERB
        elif tagging.startswith('N'):
            return wordnet.NOUN
        elif tagging.startswith('R'):
            return wordnet.ADV
        else:
            return ''

def preprocs(sent):
    words = word_tokenize(sent) #Tokenization
    words = [word.lower() for word in words if word.isalpha()] #Punctuation Removal
    # words = [word for word in words if not word in stop_words] #Stopword Removal
    # words = [ps.stem(word) for word in words] #Stemming
    words = [lmtzr.lemmatize(word) for word in words]
    st = pos_tag(words)#POS Tagging
    stWordnet = [(st[i][0],turnTaggingToWordNet(st[i][1])) for i in range(len(st))]
    return stWordnet