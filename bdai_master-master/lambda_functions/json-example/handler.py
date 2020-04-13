import simplejson as json
#import logging
import boto3
import requests
import pandas as pd
from botocore.exceptions import ClientError
from iexfinance.stocks import get_historical_data
from iexfinance.stocks import Stock
from datetime import date, timedelta
from iexfinance.refdata import get_iex_symbols

S_and_P = ['MMM\n', 'ABT\n', 'ABBV\n', 'ABMD\n', 'ACN\n', 'ATVI\n', 'ADBE\n', 'AMD\n']


def lambda_handler(event, context):
    public_token = "pk_0f6affd8c4f74ccc926906918de34761"
    yesterday = date.today() - timedelta(days=1)

    feeds = []

    with open("/tmp/"+ yesterday.strftime("%Y-%m-%d")+".json", mode ='w', encoding='utf-8') as feedsjson:
        for ticker in S_and_P:
            to_File = {}
            data = get_historical_data(ticker.replace("\n",""), yesterday, end=None, output_format='json',token = public_token)
            print(data)
            if isinstance(data, pd.DataFrame):

                to_File["date"] = yesterday.strftime("%Y-%m-%d")
                to_File["ticker"] = ticker.replace("\n","")
                to_File["open"] = None
                to_File["high"] = None
                to_File["close"] = None
                to_File["volume"] = None

            else:

                to_File["date"] = yesterday.strftime("%Y-%m-%d")
                to_File["ticker"] = ticker.replace("\n","")
                to_File["open"] = data[yesterday.strftime("%Y-%m-%d")]["open"]
                to_File["high"] = data[yesterday.strftime("%Y-%m-%d")]["high"]
                to_File["close"] = data[yesterday.strftime("%Y-%m-%d")]["close"]
                to_File["volume"] = data[yesterday.strftime("%Y-%m-%d")]["volume"]

            feedsjson.write(json.dumps(to_File))
            feedsjson.write("\n")

    s3 = boto3.client('s3')

    filename = yesterday.strftime("%Y-%m-%d")+ ".json"
    bucket_name = 'bdai-data'

    s3.upload_file("/tmp/" + filename, bucket_name,"daily-price-data/"+ filename)


    return {
        'statusCode': 200,
        'body': json.dumps(feeds)
    }
