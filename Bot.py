import tweepy
import time

auth = tweepy.OAuthHandler('consumer_key', 'consumer_secret')
auth.set_access_token('access_token', 'access_token_secret')

api = tweepy.API(auth)

lastID = '0'

username = ''   #username of the user you're checking the tweets of

i = 0
def mirrorText(oTweet):

    bruh = ' '.join(word for word in oTweet.split() if word[0]!='@')                            #remove @s (if the user replies to someone the tweet is "@user 'tweet'" and without this your tweet will include the "resu@" at the end)
    bruh = ' '.join([term for term in bruh.split() if not term.startswith("https://t.co/")])    #remove links of images, videos and quote retweets
    newTweet = str(bruh[::-1])                                                                       #mirror the rest of the text
    html_entities = {"&lt;": "<", "&gt;": ">", "&amp;": "&", "&quot;": "\"", "&apos;": "\'", "&cent;": "¢", "&pound;": "£", "&yen;": "¥", "&euro;": "€", "&copy;": "©", "&reg;": "®"}
    for entity in html_entities:
        if entity in bruh:
            bruh = bruh.replace(entity, html_entities.get(entity))
    newTweet = str(bruh[::-1])  
    return newTweet

checkNewTweet = api.user_timeline(screen_name=username,since_id = str(lastID))

for status in checkNewTweet:      #find the latest tweet id
    if int(status.id) >= int(lastID):
        lastID = str(status.id)
        print(f'{lastID} is the new since_id')

checkNewTweet = api.user_timeline(screen_name=str(username),since_id = str(lastID))

while True:
    timeNow = time.strftime('%H:%M:%S', time.localtime())       #update time (only used for debugging)
    print(f'time = {timeNow}')                                  #show time (only used for debugging)
    checkNewTweet = api.user_timeline(screen_name=str(username),since_id = str(lastID))     #update CheckNewTweet
    
    for tweet in checkNewTweet:               #check for new Tweet
        if tweet.text.startswith('RT @') == False:      #check if it's just a retweet (not quote retweet)
            print(tweet.id)
            oTweet = tweet.text
            nTweet= mirrorText(oTweet)          #get mirrored text (without @s)
            api.update_status(status=f'@{username} {nTweet}', in_reply_to_status_id = tweet.id) #tweet it out (the @{username} is there to make it a reply)
            print(f'''
TWEETED
original tweet = "{oTweet}"" || new tweet = "{nTweet}"''')  #print out the tweet (for log)

            i+=1                                #check if any new tweets happened for log
        if tweet.text.startswith('RT @') == True: #check if it's a retweet
            print('there was a tweet but it was a retweet')
    if i == 0:                              
        print(f'No new message (latest tweet id = {str(lastID)})')  #print out the fact that nothing happened (mostly for debugging and making sure that it works)
    else:
        i=0                                 #check if any new tweets happened for log

    for status in checkNewTweet:        #make latest id (lastID)
        if int(status.id) >= int(lastID):
            lastID = str(status.id)
            print(f'{lastID} is the new since_id')
    time.sleep(10)  #wait for 10 seconds (so it takes less performance)


