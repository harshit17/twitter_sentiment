import csv
import re
import pickle
import nltk.classify
from nltk.classify import NaiveBayesClassifier
# from textblob.classifiers import NaiveBayesClassifier


pos_features = []
neg_features = []
features = []
words = []
# classifier = []
word_features = []

train = []
test = []
post = []
negt = []


def getSets():
    global train, test
    t = 600
    with open('positives1.csv', 'r') as csvfile:
        rider = csv.reader(csvfile)
        for row in rider:
            if t == 0:
                break
            post.append(tuple((row[0], row[1])))
            for r in row[0].split():
                r = re.sub("[^a-z]", '', r)
                words.append(r)
            t -= 1

    t = 600
    with open('negatives1.csv', 'r') as csvfile:
        rider = csv.reader(csvfile)
        for row in rider:
            if t == 0:
                break
            for r in row[0].split():
                r = re.sub("[^a-z]", '', r)
                words.append(r)
            negt.append(tuple((row[0], row[1])))
            t -= 1

    lenp = len(post)*3/4
    lenn = len(negt)*3/4

    train = post[:lenp] + negt[:lenn]
    test = post[lenp:] + negt[lenn:]

    print len(post), len(negt)
    print post[:5]


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


def create_classifier():
    global word_features, words, train

    to_classify = ['going', 'class', 'till', 'noonjammin', 'radio']
    word_features = get_word_features(words)
    fe = extract_features(word_features)

    training_set = nltk.classify.apply_features(extract_features, train)
    classifier = NaiveBayesClassifier.train(training_set)

    f = open('my_nltk_classifier.pickle', 'wb')
    pickle.dump(classifier, f)
    f.close()
    t = 10

    print len(words)
    print word_features

    print training_set
    # print len(word_features)
    print extract_features(to_classify)
    print len(training_set)

    print(classifier.classify(extract_features(to_classify)))
    print(classifier.show_most_informative_features(10))


def classify_more():
    f = open('my_nltk_classifier.pickle', 'rb')
    cla = pickle.load(f)
    f.close()

    # print(cla.classify("FakerPattyPattz Oh dear. Were you drinking out of the forgotten table drinks"))  # "neg"
    # print(cla.classify("loverrx thank you. its so much fun "))  # "pos"

    # print("Accuracy: {0}".format(cla.accuracy(test)))

    print 'ACCURACY MEASURES:                           '
    tp = 0
    tn = 0
    fp = 0
    fn = 0

    for t in test:
        res_a = t[1]
        res_p = cla.classify(extract_features(t[0]))

        if res_a == 'pos':
            if res_p == 'pos':
                tp += 1
            else:
                # print t[0], res_a, res_p
                fn += 1
        else:
            if res_p == 'pos':
                # print t[0], res_a, res_p
                fp += 1
            else:
                tn += 1

    print 'Calculated accuracy = ' + str(float(tp + tn) / len(test))
    print 'Calculated error rate = ' + str(float(fp + fn) / len(test))
    print 'Calculated sensitivity (recall) = ' + str(tp / float(tp + fn))
    print 'Calculated specificity = ' + str(tn / float(fp + tn))
    print 'Calculated precision = ' + str(tp / float(tp + fp))

getSets()
#create_classifier()
classify_more()
