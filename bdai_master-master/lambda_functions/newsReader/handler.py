import feedparser
import pandas as pd
import re
import boto3
import os
import sys
from urllib.parse import unquote_plus
import nltk
import warnings
from datetime import datetime
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

a ="http://feeds.marketwatch.com/marketwatch/marketpulse/"
b = "https://www.cnbc.com/id/10000664/device/rss/rss.html"
feed = feedparser.parse( b)
analyser = SentimentIntensityAnalyzer()

def sentiment_analyzer_scores(sentence):
    score = analyser.polarity_scores(sentence)
    print("{:-<40} {}".format(sentence, str(score)))



stocks = {"Uber":"UBER US","Xylem": "XYL US","Wabtec": "WAB US","WPP": "WPP LN","Vodafone Group": "VOD LN","Teva Pharmaceutical Industries": "TEVA IT","Tesla": "TSLA US","Tableau Software": "DATA US","Synchrony Financial": "SYF US","SoftBank Group": "9984 JP","Rosneft Oil": "ROSN LI","Range Resources": "RRC US","Pyxus International": "PYX US","Prudential": "PRU LN","Petrobras": "PETR4 BZ","Osram Licht": "OSR GR","Nike": "NKE US","NXP Semiconductors": "NXPI US","McDermott International": "MDR US","Marathon Petroleum": "MPC US","Manulife Financial": "MFC CN","Lennar": "LEN US","L Brands": "LB US","Kroger": "KR US","Knight-Swift Transportation Holdings": "KNX US","Kering": "KER FP","Johnson Controls International": "JCI US","Iqvia Holdings": "IQV US","InterGlobe Aviation": "INDIGO IN","ITV": "ITV LN","Harley-Davidson": "HOG US","Hammerson": "HMSO LN","Gilead Sciences": "GILD US","General Electric": "GE US","Ford Motor": "F US","Fast Retailing": "9983 JP","Fannie Mae/Freddie Mac": "FNMA US/FMCC US","Energy Transfer": "ET US","Deutsche Bank": "DBK GR","Dell Technologies": "DELL US","Comcast": "CMCSA US","Cheniere Energy": "LNG US","Centrica": "CNA LN","Canopy Growth": "CGC US","CK Asset Holdings": "1113 HK","CBS": "CBS US","Boston Properties": "BXP US","Bausch Health": "BHC US","Barclays": "BARC LN","Anthem": "ANTH US","Anheuser-Busch InBev": "ABI BB","Amazon": "AMZN","Google": "GOOG","Microsoft": "MSFT","Apple": "AAPL","Facebook": "FB","Netflix": "NFLX","JP Morgan": "JPM","Bank of America": "BAC"}

def rss_processor(feed):
  title =feed.feed.title
  #retrival_time = feed.feed.time
  colTitle = []
  colPublished = []
  colTicker =[]
  colArticle = []
  colDescription= []
  colSentiment = []
  for i in feed.entries:
    for key in stocks:
      if key in i.title:
        ticker = stocks.get(key)
      else:
        ticker=None
    sia = SentimentIntensityAnalyzer()

    sentiment = sia.polarity_scores(i.description)['compound']

    colTitle.append(title)
    colPublished.append(i.published)
    colTicker.append(ticker)
    colArticle.append(i.title)
    cleaned = re.sub("<[^>]*>","", i.description)
    colDescription.append(cleaned)
    colSentiment.append(sentiment)
    print(title+"   |    "+str(sentiment)+"   |    "+i.published+"   |    " + i.title + "\n" + cleaned + "\n \n \n")
    sentiment_analyzer_scores(cleaned)
  
  data = {'Source':colTitle,'Time':colPublished,'Ticker Symbol':colTicker,'Title':colArticle,'Full Article':colDescription,'Sentiment':colSentiment}
  df = pd.DataFrame(data)
  print(df)
  #df.to_sql()
  
 

rss_processor(feed)


# Returns a datetime object containing the local date and time
dateTimeObj = datetime.now()
# Create an S3 client
s3 = boto3.client('s3')
print(dateTimeObj.year, '/', dateTimeObj.month, '/', dateTimeObj.day)
print(dateTimeObj.hour, ':', dateTimeObj.minute, ':', dateTimeObj.second, '.', dateTimeObj.microsecond)
file_name= 'output-', dateTimeObj.year, '-', dateTimeObj.month, '-', dateTimeObj.day ,'-',dateTimeObj.hour, '-', dateTimeObj.minute, '-', dateTimeObj.second,'.csv'
df.to_csv('/tmp/'+ file_name)

def lambda_handler(event, context):
    bucket_name = "news-reader-bucket"
    lambda_path = "/tmp/" + file_name
    s3_path = "/news/" + file_name

    s3 = boto3.resource("s3")
    s3.Bucket(bucket_name).put_object(Key=s3_path, Body=encoded_string)
