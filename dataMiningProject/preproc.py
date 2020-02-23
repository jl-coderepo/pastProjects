import os
from itertools import chain
from itertools import combinations
import math
import random


def formDB(pr):
    startdir = os.getcwd()
    os.chdir('reuters21578')

    db = []  # DB Schema: (id, topics, places, people, orgs, exchanges, companies, author, title, body, date)

    tset = set()
    plset = set()
    peset = set()
    oset = set()
    eset = set()
    cset = set()

    for f in os.listdir('.'):
        if os.path.splitext(f)[1] == '.sgm':
            record = open(f, 'r')
            line = record.readline()

            while line != '':

                if line[:8] == '<REUTERS':
                    id = line[line.find('NEWID') + 7:-3]

                    while line != "</REUTERS>\n":

                        line = record.readline()
                        if line[:6] == '<DATE>':
                            date = line[6:line.find('</DATE>')]

                        elif line[:8] == '<TOPICS>':
                            tline = line[11:line.find('</TOPICS>') - 4]
                            topics = tline.split('</D><D>')
                            if len(topics) == 1 and topics[0] == '':
                                topics = []
                            tset |= set(topics)

                        elif line[:8] == '<PLACES>':
                            plline = line[11:line.find('</PLACES>') - 4]
                            places = plline.split('</D><D>')
                            if len(places) == 1 and places[0] == '':
                                places = []
                            plset |= set(places)

                        elif line[:8] == '<PEOPLE>':
                            peline = line[11:line.find('</PEOPLE>') - 4]
                            people = peline.split('</D><D>')
                            if len(people) == 1 and people[0] == '':
                                people = []
                            peset |= set(people)

                        elif line[:6] == '<ORGS>':
                            oline = line[9:line.find('</ORGS>') - 4]
                            orgs = oline.split('</D><D>')
                            if len(orgs) == 1 and orgs[0] == '':
                                orgs = []
                            oset |= set(orgs)

                        elif line[:11] == '<EXCHANGES>':
                            eline = line[14:line.find('</EXCHANGES>') - 4]
                            exchanges = eline.split('</D><D>')
                            if len(exchanges) == 1 and exchanges[0] == '':
                                exchanges = []
                            eset |= set(exchanges)

                        elif line[:11] == '<COMPANIES>':
                            cline = line[9:line.find('</COMPANIES>') - 4]
                            companies = cline.split('</D><D>')
                            if len(companies) == 1 and companies[0] == '':
                                companies = []
                            cset |= set(companies)

                    db.append((id, topics, places, people, orgs, exchanges, companies))

                line = record.readline()
            record.close()

    if pr:
        print('(ID, TOPICS, PLACES, PEOPLE, ORGS, EXCHANGES, COMPANIES)')
        for entry in db:
            print(entry)
        print('')
        print('Category Sets:')
        print('Topics: ' + ', '.join(tset))
        print('Places: ' + ', '.join(plset))
        print('People: ' + ', '.join(peset))
        print('Orgs: ' + ', '.join(oset))
        print('Exchanges: ' + ', '.join(eset))
        print('Companies: ' + ', '.join(cset))

        print('')
        print('Label Counts')
        prStr = ''
        prDict = {}
        for i in tset:
            count = 0
            for entry in db:
                if i in entry[1]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('Topics: ' + prStr)

        prStr = ''
        prDict = {}
        for i in plset:
            count = 0
            for entry in db:
                if i in entry[2]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('Places: ' + prStr)

        prStr = ''
        prDict = {}
        for i in peset:
            count = 0
            for entry in db:
                if i in entry[3]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('People: ' + prStr)

        prStr = ''
        prDict = {}
        for i in oset:
            count = 0
            for entry in db:
                if i in entry[4]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('Orgs: ' + prStr)

        prStr = ''
        prDict = {}
        for i in eset:
            count = 0
            for entry in db:
                if i in entry[5]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('Exchanges: ' + prStr)

        prStr = ''
        prDict = {}
        for i in cset:
            count = 0
            for entry in db:
                if i in entry[6]:
                    count += 1
            # prStr += i + ':' + str(count) + ', '
            prDict[i] = count
        dk = sorted(prDict, key=prDict.get)
        dk.reverse()
        for i in dk:
            prStr += i + ':' + str(prDict[i]) + ', '
        print('Companies: ' + prStr)

    retlist = []
    for tup in db:
        retlist.append((tup[0], tup[1]))
    os.chdir(startdir)
    return retlist


def checkCounts(labels, data):
    for i in data:
        i[1][:] = [x for x in i[1] if x in labels]
    data[:] = [x for x in data if x[1]]

    print('Label Counts')
    o = chain.from_iterable(combinations(labels, r) for r in range(1, len(labels) + 1))
    for s in o:
        count = 0
        for entry in data:
            if set(entry[1]) == set(s):
                count += 1
        print(str(s) + ': ' + str(count))


def getArticles(labels, data):
    startdir = os.getcwd()
    os.chdir('reuters21578')

    results = {}

    idList = []
    for entry in data:
        idList.append(entry[0])

    for f in os.listdir('.'):
        if os.path.splitext(f)[1] == '.sgm':
            record = open(f, 'r')
            line = record.readline()

            while line != '':

                if line[:8] == '<REUTERS':
                    sId = line[line.find('NEWID') + 7:-3]

                    if sId in idList:
                        text = ''
                        topics = []
                        while line != '</REUTERS>\n':
                            if '<TOPICS>' in line:
                                for lab in labels:
                                    if lab in line:
                                        topics.append(lab)
                                topics = topics[:-1]
                            if '<BODY>' in line:
                                text += line[line.find('<BODY>') + len('<BODY>'):]
                                line = record.readline()
                                while '</BODY>' not in line:
                                    text += line
                                    line = record.readline()
                                results[sId] = (topics, text)
                            line = record.readline()
                line = record.readline()
            record.close()
    os.chdir(startdir)
    return results

'''
We dom't need this
def runAlg(labels, data, option, numSeeds, posSeeds):
    return 0;
'''

'''
    divData:
    Parameters:
        articles: A list of tuples from getArticles
        outFile: whether or not to write an output file of the IDs
    Returns: a list of tuples
        results[0]: tuples of unilabeled articles
        results[1]: tuples of multilabeled articles
'''


def divData(articles, outFile):
    uniLabel = []
    multiLabel = []
    for a in articles:
        if a[1].count(',') == 0:
            uniLabel.append(a)
        else:
            multiLabel.append(a)

    if (outFile):
        oFile = open('uniLabels.txt', 'w')
        for a in uniLabel:
            oFile.write(str(a[0]) + '\n')
        oFile.close()

        oFile = open('multiLabels.txt', 'w')
        for a in multiLabel:
            oFile.write(str(a[0]) + '\n')
        oFile.close()

    return [uniLabel, multiLabel]


def getSeeds(dividedData, option, numSeeds):
    seeds = []
    if (option == 1):
        seeds = random.sample(dividedData[0], numSeeds)

    elif (option == 2):
        seeds = []

    elif (option == 3):
        seeds = []

    elif (option == 4):
        seeds = []

    return seeds


if __name__ == "__main__":
    db = formDB(False)
    labList = ['money-fx', 'interest', 'trade', 'dlr']

    checkCounts(labList, db)
    articles = getArticles(labList, db)
    # IDs = divData(articles, True)
    #tfidf = tf_idf(articles)

    # oFile = open('out.txt', 'w')
    # for b in IDs:
    #     for a in b:
    #         print('id = ' + str(a[0]))
            # oFile.write('id = ' + str(a[0]) + '\n')
            # print(a[1])
            # oFile.write(a[1] + '\n')
            # print(a[2])
            # oFile.write(a[2] + '\n')
            # print('')
            # oFile.write('\n')
