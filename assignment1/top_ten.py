import sys
import json
import string
    
def loadTweetJson(fp):
    tweetRawData = open(fp)
    tweetEntries = []
    with open(fp) as tweetRawEntries:
        for line in tweetRawEntries:
            tweetEntries.append(json.loads(line))
    return tweetEntries

def getListOfHashTags(tweet):
    listOfHashtags = []
    if(tweet.has_key(u'entities') and tweet[u'entities'] != None):
        if(tweet[u'entities'].has_key(u'hashtags') and tweet[u'entities'][u'hashtags'] != None):
            hashtags = tweet[u'entities'][u'hashtags']
            if len(hashtags) > 0 :
                for hashtag in hashtags:
                    if(hashtag.has_key(u'text') and hashtag[u'text'] != None):
                        hashtagText = hashtag[u'text'].encode('utf-8')
                        listOfHashtags.append(hashtagText)                        
    return listOfHashtags

def loopThoughTweets(tweetJson):    
    hashtagHistogram = {}
    for tweet in tweetJson:
        listOfHashtags = getListOfHashTags(tweet)
        for hashtag in listOfHashtags :            
            if hashtagHistogram.has_key(hashtag):
                hashtagHistogram[hashtag] += 1
            else:
                hashtagHistogram[hashtag] = 1
           
    for hashtag in hashtagHistogram:
        print "{0} {1} ".format(hashtag, hashtagHistogram[hashtag])
        
    
def main():
    tweet_file = sys.argv[1]

    tweetJson = loadTweetJson(tweet_file)

    loopThoughTweets(tweetJson)
                         
    
if __name__ == '__main__':
    main()
