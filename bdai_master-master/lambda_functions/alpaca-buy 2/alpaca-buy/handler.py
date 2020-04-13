import json
from Alpaca_Buy_Function import buyStock

# For any additional packages make sure pipenv shell is enabled then run 
# pipenv install <package-name> for each package
import alpaca_trade_api as tradeapi

def buy(event, context):
    message = buyStock(**event)

    return {
        "statusCode": 201,
        "body": message
    }
