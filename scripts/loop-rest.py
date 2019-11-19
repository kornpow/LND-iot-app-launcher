import base64, json, requests
import codecs
from pprint import pprint

# LND_DIR = '/home/lightning/.lnd/'
# cert_path = LND_DIR + 'tls.cert'

def sendPostRequest(endpoint,data=""):
	r = requests.post(base_url + endpoint, data=json.dumps(data))
	pprint(r.json())
	return r.json()

def sendGetRequest(endpoint, data=""):
	global base_url
	target_url = base_url + endpoint.format(data)
	print("Sending Request to URL: {}".format(target_url))
	r = requests.get(target_url)
	pprint(r.text)
	return r.text

macaroon = codecs.encode(open(LND_DIR + 'data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon}
base_url = 'http://127.0.0.1:8081'
url1 = '/v1/loop/in'
url2 = '/v1/loop/in/quote/{}'
url3 = '/v1/loop/out/quote/{}'
url4 = ''



loopreq = sendGetRequest(url2,250000)


data = { 
	'max_swap_fee': "6000", 
	'loop_in_channel': "660721825987952640", 
	'max_miner_fee': "2000", 
	'amt': "400000",
	'external_htlc': True, 
}
loopreq = sendPostRequest(url1,data)
