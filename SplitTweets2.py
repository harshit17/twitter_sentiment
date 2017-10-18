import csv, re

def good(st):
    badword = ['myself', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves',
        'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'its', 'itself', 'they', 'them',
        'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
        'those', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had', 'having',
        'does', 'did', 'doing', 'the', 'and', 'but', 'because', 'until', 'while', 'for',
        'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
        'after', 'above', 'below', 'from', 'down', 'out', 'off', 'over', 'under', 'again',
        'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any',
        'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'nor', 'not', 'only',
        'own', 'same', 'than', 'too', 'very', 'can', 'will', 'just', 'don', 'should', 'now']

    if (st.isdigit()):
        return False
    if (len(st) < 3):
        return False
    if st.startswith('@'):
        return False
    if st.startswith('http'):
        return False
    if st in badword:
        return False

    return True


def getTweet(tweet):

    listt = tweet.split(' ')
    listt2 = listt[:]

    for w in listt2:
        w2 = re.sub("[^A-Za-z]", "", w)
        listt.remove(w)
        listt.append(w2)
        if good(w2) == False:
            listt.remove(w2)

    tweet = ' '.join(listt)
    tweet = tweet.lower()
    tweet = re.sub("\n", "", tweet)

    return tweet


def Split(t=100):
    posObs = []; negObs = []
    #t = 5

    with open('training.csv', 'r') as csvfile:
        rider = csv.reader(csvfile)
        for row in rider:
            if t == 0:
                break
            result = 'pos' if row[0]=='4' else 'neg'

            if result == 'pos':
                tweet = row[5]
                posObs.append(tuple((getTweet(tweet).split(), result)))

            elif result == 'neg':
                tweet = row[5]
                twee = getTweet(tweet).split()
                negObs.append(tuple((twee, result)))
                #print twee
            #t -= 1

    print posObs[:3], negObs[:3]

    with open('positives1.csv', 'wb') as csvfile:
        a = csv.writer(csvfile, delimiter=',')
        a.writerows(posObs)

    with open('negatives1.csv', 'wb') as csvfile:
        a = csv.writer(csvfile, delimiter=',')
        a.writerows(negObs)

Split()
