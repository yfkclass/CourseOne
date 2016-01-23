import sys
import json
import string

states = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}
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
            tweet = json.loads(line)
            if tweet.has_key(u'delete') != True:
                tweetEntries.append(tweet)
            elif tweet.has_key(u'user'):
                  print 'ah'
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

def getSentimentPerTweet(sentimentdic, tweetJson):
    if (tweetJson.has_key(u'text') and tweetJson[u'text'] != None):
        tweet = tweetJson[u'text'].encode('utf-8')
        
        terms = tweetTokenizer(tweet)
        totalScore = 0
        for term in terms:
            score = getSentimentPerTerm(sentimentdic, term)
            totalScore += score

    return totalScore

totalCount = 0
count = 0
notUSCount = 0
noCountry = 0
deleteCount = 0
catchAllCount = 0
geoCount = 0
coordinatesCount = 0
faildGetStateCount = 0
failParseState = 0
userNoLocation = 0
userHasLocation = 0

def convertToAbbreviation(stateName):
    global states
    for stateKey in states:
        if states[stateKey] == stateName:
            return stateKey
    return 'undefined'

def getGeoLocation(tweet):
    #print "---------------------------------------" 
    global count
    global totalCount
    global notUSCount
    global noCountry
    global deleteCount
    global catchAllCount
    global geoCount
    global coordinatesCount
    global faildGetStateCount
    global failParseState
    global userNoLocation
    global userHasLocation
    totalCount+=1

    state = 'undefined'
    try:
        if (tweet.has_key(u'place') and tweet[u'place'] != None):
            place = tweet[u'place'] 
            if place.has_key(u'country_code'):
                country = place[u'country_code']
                if country == "US":
                    if ( place.has_key(u'full_name') and place[u'full_name'] != None):
                        cityAndState = place[u'full_name'].encode('utf-8')
                        
                        locationTokens = cityAndState.replace(' ', '').split(',')
                        if len(locationTokens) == 2:
                            if(locationTokens[1] == 'USA'):
                                state = convertToAbbreviation(locationTokens[0])
                            else:
                                state = locationTokens[1]                            
                            count+=1                                    
                        else:
                            failParseState+=1
                    else:
                        faildGetStateCount+=1
                
                else:
                    notUSCount+=1                
            else:
                noCountry+=1            
        elif(tweet.has_key(u'user') and tweet[u'user'] != None):
            if(tweet[u'user'].has_key(u'location') and tweet[u'user'][u'location'] != None):
                location = tweet[u'user'][u'location'].encode('utf-8')
                #print location
                userHasLocation+=1
            else:
                userNoLocation+=1
        elif (tweet.has_key(u'geo') and tweet[u'geo'] != None):
            geoCount+=1
        elif (tweet.has_key(u'coordinates') and tweet[u'coordinates'] != None):
            coordinatesCount+=1

        else:
            catchAllCount+=1
    except:
        state = 'undefined'
          
    #print "USCount            {0}".format(count)
    #print "faildGetStateCount {0}".format(faildGetStateCount)
    #print "failParseState     {0}".format(failParseState)
    #print "notUSCount         {0}".format(notUSCount)
    #print "noCountry          {0}".format(noCountry)
    #print "userHasLocation    {0}".format(userHasLocation)
    #print "userNoLocation     {0}".format(userNoLocation)
    #print "deleteCount        {0}".format(deleteCount)
    #print "catchAllCount      {0}".format(catchAllCount)
    #print "geoCount           {0}".format(geoCount)
    #print "coordinatesCount   {0}".format(coordinatesCount)
    #print "totalCount         {0}".format(totalCount)
    #print "aggregate          {0}".format(count + notUSCount + noCountry + userHasLocation + userNoLocation +deleteCount + catchAllCount + geoCount )

    return state;

def getTweetId(tweet):
    id = -1
    if (tweet.has_key(u'id') and tweet[u'id'] != None):
        id = tweet[u'id'] 
    return id

def loopThoughTweets(sentimentdic, tweetJson):
    
    stateSentimentSum = {}
    for tweet in tweetJson:
        state = getGeoLocation(tweet)
        if(state != 'undefined'):
            id = getTweetId(tweet)
            sentiment = getSentimentPerTweet(sentimentdic, tweet)
            if stateSentimentSum.has_key(state):
                stateSentimentSum[state] += sentiment
            else:
                stateSentimentSum[state] = sentiment
            #print "{0} {1} {2} {3}".format(id, state, sentiment, stateSentimentSum[state])

    maxSentiment = 0
    happiestState = 'undefined'
    for state in stateSentimentSum:
        print "{0} {1} ".format(state, stateSentimentSum[state])
        if stateSentimentSum[state] > maxSentiment:
            maxSentiment = stateSentimentSum[state]
            happiestState = state

    print "{0} {1} ".format(happiestState, maxSentiment)
    


    
def main():
    sent_file = sys.argv[1]
    tweet_file = sys.argv[2]

    sentimentDicrionary = sentimentDictionary(sent_file)
    tweetJson = loadTweetJson(tweet_file)

    loopThoughTweets(sentimentDicrionary, tweetJson)
                         
    
if __name__ == '__main__':
    main()
