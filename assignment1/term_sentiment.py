import sys
import json
import string

def sentimentDictionary(fp):
    afinnfile = open(fp)
    scores = {}
    for line in afinnfile:
        term, score = line.split("\t")  
        scores[term] = int(score)
    return scores
    
def loadTweetJson(fp):
    tweetRawData = open(fp)
    tweetEntries = []
    with open(fp) as tweetRawEntries:
        for line in tweetRawEntries:
            tweetEntries.append(json.loads(line))
    return tweetEntries

def getSentimentPerTerm(sentimentdic, term):
    if sentimentdic.has_key(term):
        return sentimentdic[term]

    return 0

def tweetTokenizer(tweet):
    table = string.maketrans("","")
    tweet = tweet.translate(table, string.punctuation)
    terms = tweet.split()
    return terms

def getSentimentPerTweet(sentimentdic, terms):    
    totalScore = 0
    for term in terms:
        score = getSentimentPerTerm(sentimentdic, term)
        totalScore += score

    return totalScore

def findTermsNotInAFINN(sentimentdic, sentiment, terms, newTermDic):
    for term in terms:
        if sentimentdic.has_key(term) != True:
            if newTermDic.has_key(term) != True:
                if newTermDic.has_key(term):
                    newTermDic[term].append(sentiment)                    
                else:
                    newTermDic[term] = [sentiment]

def calculateSentimentForNewTerm(newTermDic, newTermSentiments):
    for newTerm in newTermDic:
        #only assign a score if it had at least 3 occurrences 
        if len(newTermDic[newTerm]) > 2 :
            sum = 0
            for score in newTermDic[newTerm]:
                sum += score
            newSentiment = sum / (float)(len(newTermDic[newTerm]))
            newTermSentiments[newTerm] = newSentiment
            #print newTerm
            #print "{0} {1} {2}".format(sum, len(newTermDic[newTerm]), newSentiment)



def loopThoughTweets(sentimentdic, tweetJson):
    newTermDic = {}
    for tweet in tweetJson:
        if tweet.has_key(u'text') and tweet[u'text'] != None:
            text = tweet[u'text']
            terms = tweetTokenizer(text.encode('utf-8'))
            totalScore = getSentimentPerTweet(sentimentdic, terms)
            findTermsNotInAFINN(sentimentdic, totalScore, terms, newTermDic)

    for newTerm in newTermDic:
        print "{0} {1}".format(newTerm, len(newTermDic[newTerm])    )

    newTermSentiments = {}
    calculateSentimentForNewTerm(newTermDic, newTermSentiments)
    
    #for newTerm in newTermSentiments:
    #    print "{0} {1}".format(newTerm, newTermSentiments[newTerm])
            

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    sentimentDicrionary = sentimentDictionary(sent_file)
    tweetJson = loadTweetJson(tweet_file)

    loopThoughTweets(sentimentDicrionary, tweetJson)

if __name__ == '__main__':
    main()
