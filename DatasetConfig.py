import xml.etree.cElementTree as ET
import re


def generateDatasetFromXML():
    tree = ET.ElementTree(file='SemEval2016-Task3-CQA-QL-train-part1-with-multiline.xml')
    root = tree.getroot()
    OrgQSubject = []  # Subjek Pertanyaan Original
    OrgQBody = []  # Pertanyaan Original
    RelQBody = []  # Pertanyaan Related yang = perfect match
    RELQ_RELEVANCE2ORGQ = []  # Hubungan pertanyaan Related dengan Pertanyaan Original
    RelCText = []  # Teks Jawaban yang = both of Good
    RELC_RELEVANCE2ORGQ = []  # Hubungan jawaban dengan pertanyaan Original
    RELC_RELEVANCE2RELQ = []  # Hubungan jawaban dengan pertanyaan Related
    RELQ_ID = []
    RELQ_Quest = []
    RELQ_Relevance = []

    for OrgQuestionList in root:
        for threadQuest in OrgQuestionList[3].iterfind('RelQuestion[@RELQ_RELEVANCE2ORGQ="PerfectMatch"]'):
            RELQ_ID.append(threadQuest.get('RELQ_ID'))
            RELQ_Relevance.append(threadQuest.get('RELQ_RELEVANCE2ORGQ'))
            RELQ_Quest.append(threadQuest[2].text)

        for thread in OrgQuestionList[3].iterfind(
                'RelComment[@RELC_RELEVANCE2ORGQ="Good"][@RELC_RELEVANCE2ORGQ="Good"]'):
            strID = re.search('(.+?)_C', thread.get('RELC_ID')).group(1)
            if strID in RELQ_ID:
                OrgQSubject.append(OrgQuestionList[0].text)
                OrgQBody.append(OrgQuestionList[2].text)
                RelQBody.append(re.sub(r'.*// (.*)', r'\1', RELQ_Quest[RELQ_ID.index(strID)]))
                # RelQBody.append(RELQ_Quest[RELQ_ID.index(strID)])
                RELQ_RELEVANCE2ORGQ.append(RELQ_Relevance[RELQ_ID.index(strID)])
                RelCText.append(thread[1].text)
                RELC_RELEVANCE2ORGQ.append(thread.get('RELC_RELEVANCE2ORGQ'))
                RELC_RELEVANCE2RELQ.append(thread.get('RELC_RELEVANCE2RELQ'))
            break

    result = [(OrgQSubject[i], OrgQBody[i], RelQBody[i], RELQ_RELEVANCE2ORGQ[i], RelCText[i], RELC_RELEVANCE2ORGQ[i],
               RELC_RELEVANCE2RELQ[i]) for i in range(len(OrgQSubject))]

    return RelQBody, RelCText


generateDatasetFromXML()
