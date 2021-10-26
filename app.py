import hashlib
import hmac
import json
import requests

from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"

# API info
API_HOST = 'https://api.bitkub.com'
API_KEY = os.environ['API_KEY']
API_SECRET = b + os.environ['API_SECRET']

def json_encode(data):
	return json.dumps(data, separators=(',', ':'), sort_keys=True)

def sign(data):
	j = json_encode(data)
	print('Signing payload: ' + j)
	h = hmac.new(API_SECRET, msg=j.encode(), digestmod=hashlib.sha256)
	return h.hexdigest()

# check server time
response = requests.get(API_HOST + '/api/servertime')
ts = int(response.text)
print('Server time: ' + response.text)

# place bid
header = {
	'Accept': 'application/json',
	'Content-Type': 'application/json',
	'X-BTK-APIKEY': API_KEY,
}

@app.route('/buy')
	data = {
		'sym': 'THB_BTC',
		'amt': 10, # THB amount you want to spend
		'rat': 260000,
		'typ': 'limit',
		'ts': ts,
	}
	signature = sign(data)
	data['sig'] = signature

	print('Payload with signature: ' + json_encode(data))
	response = requests.post(API_HOST + '/api/market/place-bid', headers=header, data=json_encode(data))

	print('Response: ' + response.text)
	return ('Response: ' + response.text)
