import preproc as pp
import math
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse


def run_fkm():
    db = pp.formDB(False)
    labels = ['money-fx', 'interest', 'trade', 'dlr']

    a = pp.getArticles(labels, db)
    idList = list(a.keys())
    print(idList)

    # print('world')
    tfidf = sk_tf_idf(a, idList)
    center = computeCenter(tfidf, idList)
    print(center)
    # print('hi')


def computeCenter(tfidf_vec, ids):
    init = False
    init2 = False
    for i in ids:
        if not init2:
            if not init:
                a = i
                init = True
            else:
                m = sparse.vstack((tfidf_vec[a], tfidf_vec[i]))
                init2 = True
        else:
            m = sparse.vstack((m, tfidf_vec[i]))

    return sparse.csr_matrix(sparse.csr_matrix.mean(m, axis=0))

# out dictionary key:id value:dict()


# IN: articles returned from getArticles as input
# OUT: List of dictionary where Key = word, Value = normalized tf-idf value.
#     Each list entry (dictionary) belongs to one article


def sk_tf_idf(articles, idList):
    idDict = {}
    tfVec = TfidfVectorizer()
    aList = []
    for i in idList:
        aList.append(articles[i][1])

    mat = tfVec.fit_transform(aList)

    # print(mat.shape)

    for i in range(mat.shape[0]):
        idDict[idList[i]] = mat[i]

    return idDict


def tf_idf(articles):
    # dict of id -> tf-idf dicts to return
    idDict = {}

    # term frequency: key = word, value = times key appears
    tf = {}
    # article frequency: key = word, value = number of articles it is in
    af = {}
    # idf calculated for each word in tf as log(N/af[key])
    idf = {}
    # tfidf calculated as tf[key]*idf[key]
    tfidf = {}
    numBodies = len(articles)
    maxVal = 0
    minVal = 0

    ###perform TF
    # set up a loop to grab each article
    for keyA in articles:
        ##inside each article, we must parse it to find all the words

        # grab the body text and split it into individual words
        body = articles[keyA][1]
        for word in body.split():
            # see if the word exists in dictionary
            if word in tf:
                # if it is, increment the value by one
                tf[word] += 1
            else:
                # otherwise we add it into the dictionary
                tf[word] = 1
                # add the word to AF so we know to search articles for this word
                af[word] = 0

        ###find the article frequency for each word we found in current article
        for key in tf:
            # for each key, iterate through the list of articles and see if it is contained
            for keyB in articles:
                #grab the text body for the article
                textBody = articles[keyB][1]
                # if it is, increment idf value
                if key in textBody:
                    af[key] += 1

        ###calculate idf for each key
        for key in tf:
            numArt = af[key]
            idf[key] = math.log10(numBodies / numArt)

        ###calculate tfidf for each key
        for key in tf:
            tfidfVal = tf[key] * idf[key]
            # set the maxVal
            if maxVal < tfidfVal:
                maxVal = tfidfVal
            # set the minVal
            if minVal == 0 or minVal > tfidfVal:
                minVal = tfidfVal
            tfidf[key] = tfidfVal

        valRange = maxVal - minVal
        ###go through tfidf and normalize the values
        for key in tfidf:
            valToNorm = tfidf[key]
            norm = (valToNorm - minVal) / (valRange)
            tfidf[key] = norm

        #create the dictionary entry
        artId = keyA
        idDict[artId] = tfidf

        # clear storage to prep for next article
        maxVal = 0
        minVal = 0
        tf.clear()
        af.clear()
        idf.clear()
        tfidf.clear()

    return idDict


if __name__ == '__main__':
    run_fkm()