import re 

def clean_tweet(tweet):
    
    try:
    
        #temp = tweet.lower()
        temp = re.sub("@[A-Za-z0-9_]+","", tweet)
        temp = re.sub("#[A-Za-z0-9_]+","", temp)

        temp = re.sub(r"http\S+", "", temp)
        temp = re.sub(r"www.\S+", "", temp)

        #temp = re.sub('[()!?]', ' ', temp)
        #temp = re.sub('\[.*?\]',' ', temp)

        #temp = re.sub("[^a-z0-9]"," ", temp)
    except:
        temp = tweet.copy()
    
    return temp