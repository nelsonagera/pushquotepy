
import json
from twilio.rest import Client
import time
import requests#htttp

CREDENTIALS_FILE = 'data/credentials.json'
REG_NUM_FILE = 'data/registered_numbers.json'
DELAY = 30


def getCredentials(path):
    with open(path) as f:
        credentials = json.load(f)

    return credentials
def getNumbers(path):
    with open(path) as f:
        numbers = json.load(f)
    return numbers

credentials = getCredentials(CREDENTIALS_FILE)

def fetchQuote(category='famous'):
    url = credentials['mashape']['url']
    param ={"cat": category}
    key=credentials['mashape']['api_key']
    headers={
        "X-Mashape-Key": key,
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
      }
    response = requests.post(url,headers=headers, data= param)
    if response.ok:
        content=response.text
        data=json.loads(content)
        quote = data['quote']+ ' - '  +  data['author']
    else:
        quote = 'No quotes found'

    return quote

def main():

    client      = Client(credentials['twilio']['api_key'],credentials['twilio']['api_secret'])
    numbers     = getNumbers(REG_NUM_FILE)
    while True:
        body = fetchQuote()
        for number in numbers:
            client.messages.create(to=number,from_=credentials['twilio']['number'],body=body)
        time.sleep(DELAY)

if __name__ == '__main__':
     main()
