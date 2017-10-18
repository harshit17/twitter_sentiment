from textblob.classifiers import NaiveBayesClassifier
import csv
import re
import nltk
import pickle

train = []
test = []
post = []
negt = []
word_features = []


def getSets():
    global train, test
    t = 600
    with open('positives.csv', 'r') as csvfile:
        rider = csv.reader(csvfile)
        for row in rider:
            if t == 0:
                break
            post.append(tuple((row[0], row[1])))
            t -= 1

    t = 600
    with open('negatives.csv', 'r') as csvfile:
        rider = csv.reader(csvfile)
        for row in rider:
            if t == 0:
                break
            negt.append(tuple((row[0], row[1])))
            t -= 1

    lenp = len(post)*3/4
    lenn = len(negt)*3/4

    train = post[:lenp] + negt[:lenn]
    test = post[lenp:] + negt[lenn:]

    print len(post), len(negt)


def get_word_features(wordlist):
    wordlist = nltk.FreqDist(wordlist)
    wordlist = wordlist.most_common(100)
    # w = []
    # for k in wordlist:
    #     if len(k)>1:
    #         w.append(k)
    return wordlist


def extract_features(document):
    document_words = set(document)
    feature = {}
    for word in word_features:
        try:
            word = re.sub("[^a-z]", '', str(word))
        except:
            print word
        feature[word] = True if word in document_words else False
    return feature


def Make_Classifier():
    global train, test
    cl = NaiveBayesClassifier(train)

    f = open('my_classifier.pickle', 'wb')
    pickle.dump(cl, f)
    f.close()


def Classify():

    f = open('my_classifier.pickle', 'rb')
    cla = pickle.load(f)
    f.close()

    print(cla.classify("FakerPattyPattz Oh dear. Were you drinking out of the forgotten table drinks"))  # "neg"
    print(cla.classify("loverrx thank you. its so much fun "))  # "pos"

    #print("Accuracy: {0}".format(cla.accuracy(test)))

    tp =0; tn = 0; fp = 0; fn = 0

    for t in test:
        res_a = t[1]
        res_p = cla.classify(t[0])

        if res_a == 'pos':
            if res_p == 'pos':
                tp += 1
            else:
                fn += 1
        else:
            if res_p == 'pos':
                fp += 1
            else:
                tn += 1

    print 'Calculated accuracy = ' + str(float(tp+tn)/len(test))
    print 'Calculated error rate = ' + str(float(fp+fn)/len(test))
    print 'Calculated sensitivity (recall) = ' + str(tp / float(tp + fn))
    print 'Calculated specificity = ' + str(tn / float(fp + tn))
    print 'Calculated precision = ' + str(tp / float(tp + fp))

    cla.show_informative_features()

getSets()
# Make_Classifier()
Classify()
# print good('http://twitpic.com/2y1zl')
