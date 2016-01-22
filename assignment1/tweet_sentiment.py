import sys
import json
import string

def sentimentDictionary(fp):
    afinnfile = open(fp)
    scores = {}
    for line in afinnfile:
        term, score  = line.split("\t")  
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

def getSentimentPerTweet(sentimentdic, tweet):
    #table = string.maketrans("","")
    #tweet = tweet.translate(table, string.punctuation)
    terms = tweetTokenizer(tweet)
    totalScore = 0
    for term in terms:
        score = getSentimentPerTerm(sentimentdic, term)
        totalScore += score

    return totalScore

def loopThoughTweets(sentimentdic, tweetJson):    
    for tweet in tweetJson:
        if tweet.has_key(u'text'):
            text = tweet[u'text']
            totalScore = getSentimentPerTweet(sentimentdic, text.encode('utf-8'))
            print totalScore   
    
    
def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    #sent_file = "AFINN-111.txt"
    #tweet_file = "output.txt"
    
    sentimentDicrionary = sentimentDictionary(sent_file)
    tweetJson = loadTweetJson(tweet_file)

    loopThoughTweets(sentimentDicrionary, tweetJson)
                         
    
if __name__ == '__main__':
    main()
