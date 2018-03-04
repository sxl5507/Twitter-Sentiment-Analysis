# -*- coding: utf-8 -*-
"""
Created on Mon Feb 19 11:30:22 2018

@author: Siyan
"""

import requests, json, time, datetime, nltk
import pandas as pd
from requests_oauthlib import OAuth1
from textblob import TextBlob
from nltk.tokenize import TweetTokenizer



ckey="WrPEiGACszN0gFii0HjZce7Ml"
csecret="MX41ldSo9U8A8qxOVJGdZE9eSaGlnayaT30XHlFFiplOYXLUaW"
atoken="4822491025-XrAoSNCMu26n4UsviYwZ9syPHFbiTkLrJAD6oKN"
asecret="IPMlkJs6TpXahO9jojwb5HlNBGIA4r9fUrNBJH3iKabbM"

auth = OAuth1(ckey, csecret, atoken, asecret) # OAuth 1.0a
url= 'https://stream.twitter.com/1.1/statuses/filter.json'
#nltk.download('stopwords')
#nltk.download('wordnet')



def Streaming (process_time=10, write_method= 'w', save_name= 'tweets_raw.txt'):
    # process_time (int): how many seconds to stream
    # write_method (str): 'w' to overwrite old data; 'a' append data at end
    # save_name (str): file name to same data
    file= open(save_name, write_method)
    start=time.time()
    
    global reconnect_counter
    # ignore all conection errors and stream again
    while True:
        try:
            print ('Streaming {}s'.format(process_time))
            response= requests.get(url, params=params, auth=auth, stream=True)
            r= response.iter_lines(chunk_size=1) # return byte objects; generator
            while time.time() - start < process_time:
                tweet=next(r).decode('UTF-8')
                if tweet != '': # filter out empty lines
                    data = json.loads(tweet)
                    if 'text' in data.keys(): # validation
                        location= data['user']['location']
                        if location is not None: # only collect text with location info
                            file.write(json.dumps(data['text'])) # "json dumps" make a better format
                            file.write('##@@')
                            file.write(json.dumps(location))
                            file.write('##@@')
                            file.write('"'+ datetime.datetime.now().isoformat(' ', 'seconds') +'"')
                            file.write('\n')
            break
        except KeyboardInterrupt: # allow KeyboardInterrupt
            raise KeyboardInterrupt()
        except:
            reconnect_counter+=1
            print('Error! Reconnect in 3s...')
            time.sleep(3)
            continue
    response.close()
    file.close()





def PrepareData():
    # only keeps tweets with valid location; remove "; parse datetime
    df= pd.read_csv('tweets_raw.txt',names= ['text', 'location', 'time (CST)'],sep='##@@',engine='python')
    df['location'] = df['location'].apply(lambda x: x.strip('"'))
    df= df[df['location'].isin(df_city_state.tolist())]
    df[['text', 'time (CST)']]= df[['text', 'time (CST)']].apply(lambda x: x.str.strip('"'))
    return df




def AnalyzeData(df, analysis_method= 'afinn', write_method= 'a'):
    # sentiment analysis & save processed data to csv
    # analysis_method (str): 'afinn' to match afinn-165 file; 'textblob' to use <TextBlob(x).sentiment>
    # write_method (str): 'w' to overwrite old data; 'a' append data at end
    if analysis_method=='textblob':
        sentiment_analysis= df['text'].apply(lambda x: TextBlob(x).sentiment).tolist()
        df['polarity'], df['subjectivity']= zip(*sentiment_analysis)
        df= df[df['polarity'] != 0.0] # filter out neutral comments

    if analysis_method== 'afinn':
        token= TweetTokenizer(strip_handles=True, reduce_len=True)
        lemm = nltk.stem.WordNetLemmatizer()

        # prepare stop words
        slist=['rt', params['track']] # remove specific words
        stopwords = nltk.corpus.stopwords.words('english')
        stopwords=[*stopwords,*slist]

        # tokenize, remove stopwords, lemmatize, find afinn score and match words for each tweet
        text= df['text'].str.lower().tolist()
        emotion,keywords=[],[]
        for i, t in enumerate(text): #loop over each tweet
            emo,kwd=[],[]
            text[i]= [lemm.lemmatize(word) for word in token.tokenize(t) if word not in stopwords]
            for w in text[i]: # loop over words in each tweet
                if w in term: # term: list of words in afinn file
                     emo.append(term_score[w])
                     kwd.append(w)
                else:
                     emo.append(0) # 0 if no match
            emotion.append(sum(emo))
            keywords.append(','.join(kwd))

        df=df.assign(sentiment=emotion)
        df=df.assign(matched_words=keywords)
        df= df[df['matched_words'] != ''] # filter out rows with no matched word
    else:
        print('Error with analysis_method!')
        return None
    # append data to text
    df.to_csv('tweets_processed.txt', index=False, header=False, sep='\t', mode= write_method)
    return df





def ProcessControl (params, batch=12*60, process_time= 30, sleep_time= 30):
    user_command='r'
    while user_command=='r': # ask user to repeat the process
        hour= input('How many hours to stream?\t')
        if hour=='':
            hour= 12
        else: 
            hour= float(hour) 
        batch= round(hour*60*60/(process_time + sleep_time))
        print('process_time: {}s'.format(process_time))
        print('sleep_time: {}s'.format(sleep_time))
        print('total length: {}h\n'.format(hour))
    
    
        global reconnect_counter
        reconnect_counter=0
        counter=1
        while counter <= batch:
            print('Current batch: {}/{}'.format(counter, batch))
            Streaming(process_time= process_time)
            df= AnalyzeData(PrepareData()) # analysis and saving
            print('Sleep {}s'.format(sleep_time))
            print('Done! Total reconnected {} times\n'.format(reconnect_counter))
            time.sleep(sleep_time)
            counter+=1
    
        print(df.head())
        print('\nShape: {}'.format(df.shape))
        print('Avg. Sentiment: {}'.format(df['sentiment'].sum()/len(df)))
        print('Total reconnected {} times'.format(reconnect_counter))
        print('--------------------------')
        user_command= input('All Done! Enter [r] to repeat?\t')
    





#%% collecting data and control

# import city, state list
df_location= pd.read_csv('us_cities_states_counties.csv', header=0, sep='|')
df_city_state= df_location['City'] + ', ' + df_location['State short'] # new format [city, state]

# import afinn file
afinnfile = open('AFINN-en-165.txt')
term_score = {}
for l in afinnfile:
    term, score  = l.split("\t")
    term_score[term] = int(score)
term= term_score.keys()
afinnfile.close()





params={'track':'Trump', 'lang': 'en'} # commas as logical ORs, spaces are equivalent to logical ANDs
ProcessControl(params)

#df_all= pd.read_csv('tweets_processed.txt', sep= '\t',
#                names=['text','location','time(CST)','sentiment','matched_words'])
#df_all['time(CST)']= pd.to_datetime(df_all['time(CST)'])





