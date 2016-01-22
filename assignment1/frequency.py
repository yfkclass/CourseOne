import sys
import json
import string
from decimal import Decimal
    
def loadTweetJson(fp):
    tweetRawData = open(fp)
    tweetEntries = []
    with open(fp) as tweetRawEntries:
        for line in tweetRawEntries:
            tweetEntries.append(json.loads(line))
    return tweetEntries

def tweetTokenizer(tweet):
    table = string.maketrans("","")
    tweet = tweet.translate(table, string.punctuation)
    terms = tweet.split()
    return terms

def countTokensInTweet(tweet, termDictionary):
    terms = tweetTokenizer(tweet)
    
    for term in terms:
        if termDictionary.has_key(term):
            termDictionary[term]+=1
        else:
            termDictionary[term]=1

def countOccurancesOfAllTermsInAllTweets(termDictionary):
    sum = 0
    for key, value in termDictionary.iteritems():
        sum += value
    return sum

def printFrequencyHistogram(termDictionary, countOfAllTermsInAllTweets):
    for key, value in termDictionary.iteritems():
        str = "{0} {1}".format(key, Decimal(value)/Decimal(countOfAllTermsInAllTweets))
        print str

def loopThroughTweets(tweetJson):
    termDictionary = {}
    for tweet in tweetJson:
        if tweet.has_key(u'text'):
            text = tweet[u'text']
            countTokensInTweet(text.encode('utf-8'), termDictionary)
    return termDictionary

def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]
    
    #sent_file = "AFINN-111.txt"
    #tweet_file = "output.txt"

    tweetJson = loadTweetJson(tweet_file)
    termDictionary = loopThroughTweets(tweetJson)

    countOfAllTermsInAllTweets = countOccurancesOfAllTermsInAllTweets(termDictionary)

    printFrequencyHistogram(termDictionary, countOfAllTermsInAllTweets)
                     
    
if __name__ == '__main__':
    main()
