import requests
import base64, codecs, json, requests
import binascii
import code
from pprint import pprint
import pandas



class LNDRest(object):
	def __init__(self):
		# LND_DIR = '/home/lightning/.lnd/'
		LND_DIR = '/home/skorn/kornpow_cloud/.lnd/'

		macaroon = codecs.encode(open(LND_DIR + 'data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')

		cert_path = LND_DIR + 'tls.cert'

		headers = {'Grpc-Metadata-macaroon': macaroon}

		# {'Grpc-Metadata-macaroon': b'0201036c6e6402cf01030a106271d20b342cb9715ab7f5813f88d00a1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a120a067369676e6572120867656e65726174650000062042d508b098e94db9256b10f4fe9134b516777bc5b38d3e17b757fddcf9d1d7c7'}
		# base_url = 'https://45.63.16.216:8080'
		base_url = 'https://localhost:8080'


		# GET: channelbalance
		url1 = '/v1/balance/channels'
		# GET: getinfo
		url2 = '/v1/getinfo'
		# GET: listpayments
		url3 = '/v1/payments'
		# GET: getnodeinfo
		url4 = '/v1/graph/node/{}'
		# GET listchannels, POST: openchannelsync
		# data = {'sat_per_byte': None, 'local_funding_amount': None, 'node_pubkey_string':None}
		url5 = '/v1/channels'
		# GET: decodepayreq
		url6 = '/v1/payreq/{}'
		# GET: pendingchannels
		url7 = '/v1/channels/pending'
		# POST: addinvoice, GET: listinvoices
		url8 = '/v1/invoices'
		# GET: walletbalance
		url9 = '/v1/balance/blockchain'
		# POST: sendpayment
		payreq = 'lnbc739300n1pwm3cpqpp5uy6jc2d9666yxyl7vqhywj7e0v6fpl799tvrdetg6uh8rk4f28lsdq5vf5kwgr5v4ehg6twvumqcqzpge7hf5437r5m4u4kf4vp3w4dgvyadvnr0v5qul0yxhah67490wf74wkca0x044kn0y95v5k30ec6lyc2pfrfuf6dznlsx9k0wmt8r22gphd02cm'
		outid = '660721825987952640'
		# data = {'payment_request': payreq }
		# data = {'payment_request': payreq, 'outgoing_chan_id': outid}
		url10 = '/v1/channels/transactions'
		# GET: newaddress
		url11 = '/v1/newaddress'
		# POST: connect
		# data = {'pubkey': '3abf6f44c355dec0d5aa155bdbdd6e0c8fefe318eff402de65c6eb2e1be55dc3e', 'host': '18.221.23.28:9735'}
		# w['addr'] = data
		url12 = '/v1/peers'
		# POST: unlockwallet
		# data = {'wallet_password':base64.b64encode(b'').decode()}
		url13 = '/v1/unlockwallet'

def sendPostRequest(self,endpoint,data=""):
	r = requests.post(self.base_url + endpoint, headers=self.headers, verify=self.cert_path, data=json.dumps(data))
	pprint(r.json())
	return r.json()

def sendGetRequest(self,endpoint, data=""):
	r = requests.get(self.base_url + endpoint.format(data), headers=self.headers, verify=cert_path)
	pprint(r.json())

	return r.json()
	# payframe = pandas.DataFrame(r.json()['payments'])

# lnreq = sendPostRequest(url10, data)
# lnreq = sendGetRequest(url9)

lnd = LNDRest()

code.interact(local=locals())
