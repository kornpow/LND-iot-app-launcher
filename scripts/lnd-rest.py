import requests
import base64, codecs, json, requests
import binascii
import code
from pprint import pprint
import pandas
from pandas import Series
from math import floor, fsum
from datetime import datetime, timedelta
from hashlib import sha256
pandas.set_option('display.max_colwidth', -1)
import traceback
import os

# LND_DIR = '/home/lightning/.lnd/'
LND_DIR = f'{os.getenv("HOME")}/kornpow_cloud/.lnd/'
print(LND_DIR)
# Get Macaroon into a useable form!
# TODO: delete me?
# with open(LND_DIR + 'mainnet/admin.macaroon', 'rb') as f:
# 	hex_content = binascii.b2a_hex(f.read())

# OR
# This one is better!
macaroon = codecs.encode(open(LND_DIR + 'data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
# macaroon = codecs.encode(open(LND_DIR + 'test.macaroon', 'rb').read(), 'hex')
headers = {'Grpc-Metadata-macaroon': macaroon}

cert_path = LND_DIR + 'tls.cert'

whenbtc = '0200424bd89b5282c310e10a52fd783070556f947b54d93f73fd89534ce0cba708'
bitrefill = '030c3f19d742ca294a55c00376b3b355c3c90d61c6b6b39554dbc7ac19b141c14f'
my_key = '0266368f0319fb67b658b7617caca3e5c2baf06dad4c9a72dab8bd02a95c1b06e7'
lnbig = '03da1c27ca77872ac5b3e568af30673e599a47a5e4497f85c7b5da42048807b3ed'
satsplace = '024655b768ef40951b20053a5c4b951606d4d86085d51238f2c67c7dec29c792ca'
acinq = '03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f'
nodroid = '03077d02d11d2ade200c7fc5ba4fc66c1c599424fb945e88b3896fee6eedc07147'
loop_server = '021c97a90a411ff2b10dc2a8e32de2f29d2fa49d41bfbb52bd416e460db0747d0d'
creampay = '02c69a0b4cb468660348d6d457d9212563ad08fb94d424395da6796fb74a13f276'

# {'Grpc-Metadata-macaroon': b''}
# node_ip = ''
base_url = f'https://{os.getenv("NODE_IP")}:8080'
print(base_url)

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
# payreq = 'lnbc739300n1pwm3cpqpp5uy6jc2d9666yxyl7vqhywj7e0v6fpl799tvrdetg6uh8rk4f28lsdq5vf5kwgr5v4ehg6twvumqcqzpge7hf5437r5m4u4kf4vp3w4dgvyadvnr0v5qul0yxhah67490wf74wkca0x044kn0y95v5k30ec6lyc2pfrfuf6dznlsx9k0wmt8r22gphd02cm'
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

# GET: feereport
# lnreq = sendGetRequest(url14)
url14 = '/v1/fees'

# GET: 
url15 = '/v1/graph/routes/{pub_key}/{amt}'

# POST:
url16 = '/v1/channels/transactions/route'

# GET:
url17 = '/v1/graph/edge/{}'

# POST:
url18 = '/v1/switch'

# POST
data1 = { 
	'fee_rate': 0.00001, 
	'time_lock_delta': 20, 
	'global': True, 
	'base_fee_msat': '250', 
}
url19 = '/v1/chanpolicy'

# ERROR List
# {'error': 'permission denied', 'message': 'permission denied', 'code': 2}

##### Base GET/POST  REQUEST
def sendPostRequest(endpoint,data="",debug=False):
	url = base_url + endpoint
	r = requests.post(url, headers=headers, verify=cert_path, data=json.dumps(data))
	# pprint(r.json())
	return r.json()

def sendGetRequest(endpoint, ext="", body=None, debug=False):
	url = base_url + endpoint.format(ext)
	if debug:
		print(f"GET: {url}")
	r = requests.get(url, headers=headers, verify=cert_path, data=body)
	return r.json()

def sendDeleteRequest(endpoint, data="",debug=False):
	url = base_url + endpoint
	if debug:
		print(f"DELETE: {url}")
	r = requests.delete(url, headers=headers, verify=cert_path, data=json.dumps(data))
	# pprint(r.json())
	return r.json()



##### Payment Functions
def sendPaymentByReq(payreq, outid=None):
	data = {}
	data = {'payment_request': payreq, 'outgoing_chan_id': outid if outid else 0} 
	# if outid != None:
	# 	data = {'payment_request': payreq, 'outgoing_chan_id': outid}
	# data = {'payment_request': payreq, 'payment_hash_string':'2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'}
	lnreq = sendPostRequest(url10, data)
	pprint(lnreq)
	try:
		pay_frame = pandas.DataFrame(lnreq['payment_route']['hops'])
		pay_frame
		pay_frame['alias'] = pay_frame.apply(lambda x: getAlias(x.pub_key), axis=1)
		pay_frame
		return pay_frame
	except KeyError as e:
		print(f"Error: payment_error {lnreq['payment_error']}")
		return lnreq

def rebalance(payreq,outgoing_chan_id,last_hop_pubkey):
	endpoint = '/v1/channels/transactions'
	bdata = {}
	bdata['allow_self_payment'] = True
	bdata['outgoing_chan_id'] = f'{outgoing_chan_id}'
	# bdata['last_hop_pubkey'] = f'{last_hop_pubkey}'
	# bdata['last_hop_pubkey'] = codecs.encode(codecs.decode(last_hop_pubkey, 'hex'), 'base64').decode().rstrip('\n')
	# bdata['last_hop_pubkey'] = base64.b64encode(bytearray.fromhex(last_hop_pubkey) ).decode()
	bdata['last_hop_pubkey'] = base64.b64encode(last_hop_pubkey.encode('UTF-8') ).decode()
	# bdata['last_hop_pubkey'] = last_hop_pubkey
	# bdata['last_hop_pubkey'] = base64.encodebytes(last_hop_pubkey.encode("UTF-8")).decode('ascii')
	print(bdata)
	# return bdata
	# lnreq = sendPostRequest(url,data=bdata,debug=True)
	url = base_url + endpoint
	lnreq = requests.post(url, headers=headers, verify=cert_path, data=json.dumps(bdata))
	return lnreq

def PayByRoute(route,pay_hash=None):
	if pay_hash == None:
		pay_hash = base64.b64encode(b'blah1234').decode()

	data = { 
		'payment_hash_string': pay_hash, 
		'route': route, 
	}
	lnreq = sendPostRequest(url16,data)
	pprint(lnreq)
	return lnreq

def getNewAddress():
	url = '/v1/newaddress'
	lnreq = sendGetRequest(url)
	return lnreq['address']


def getChanPoint(chanid):
	lnreq = sendGetRequest(url17,str(chanid) )
	cp = lnreq['chan_point']
	return cp

def getPendingChannels():
	url = '/v1/channels/pending'
	lnreq = sendGetRequest(url)
	pending_types = list(set(lnreq.keys()) - {'total_limbo_balance'})
	pending_types
	print(lnreq)
	a = pandas.DataFrame(lnreq['pending_open_channels'])
	print(a)
	# for pend in pending_types:
	# 	b = pandas.DataFrame(lnreq[pend][0]['channel'], index=[0])[['remote_node_pub', 'channel_point', 'capacity','local_balance']]
	# 	type_list = pend.split("_")
	# 	b['type'] = type_list[1]
	# 	a = a.append(b)
	# a['alias'] = a['remote_node_pub'].apply(lambda x: getAlias(x))
	return a

# a = pandas.DataFrame(lnreq['pending_open_channels'][0]['channel'], index=[0])[['remote_node_pub', 'channel_point', 'capacity','local_balance']]
# a['type'] = 'open'
# b = pandas.DataFrame(lnreq['pending_force_closing_channels'][0]['channel'], index=[0])[['remote_node_pub', 'channel_point', 'capacity','local_balance']]
# b['type'] = 'force_close'
# c = a.append(b)


# Channel Functions
def getChanPolicy(chanid, pubkey=None):
	lnreq = sendGetRequest(url17,str(chanid) )
	df = pandas.DataFrame.from_dict({lnreq['node1_pub']:lnreq['node1_policy'],lnreq['node2_pub']:lnreq['node2_policy']})
	df = df.T
	df.reset_index(inplace=True)
	df.rename(columns={'index':'pubkey'}, inplace=True)
	df['alias'] = df['pubkey'].apply(lambda x: getAlias(x))
	# If things are null it doesnt return them!!
	df = df.fillna(0)
	# Only get info for one side of channel
	if pubkey:
		df = df[df.pubkey==pubkey]
	# print(df)
	return df

def getBalance(row):
	return row['local_balance'] / (row['local_balance']+row['remote_balance'])

def getToBalance(row):
	return (row['balanced']-0.5) * (row['local_balance']+row['remote_balance'])

def listChannels(chanpoint=None,all=False):
	lnreq = sendGetRequest(url5)
	d = pandas.DataFrame(lnreq['channels'])
	y = d[['active','chan_id','channel_point','remote_pubkey','local_balance','remote_balance']].fillna(0)
	# Convert columns to integers
	y[['local_balance','remote_balance']] = y[['local_balance','remote_balance']].apply(pandas.to_numeric, errors='coerce')
	y['balanced'] = y.apply(getBalance, axis=1)
	y['alias'] = y.apply(lambda x: getAlias(x.remote_pubkey), axis=1)
	y['tobalance'] = y.apply(getToBalance, axis=1)
 	# y = y.set_index("channel_point")
	if chanpoint:
		y = y[y.index==chanpoint]
	if all:
		return y
	else:
		return y[['active','alias','balanced','tobalance','local_balance','remote_balance','chan_id','remote_pubkey']]

def connectPeer(ln_at_url):
	url = '/v1/peers'
	# ln_at_url = '038bdb5538a4e415c42f8fb09750729752c1a1800d321f4bb056a9f582569fbf8e@ln.suredbits.com'
	pubkey,host = ln_at_url.split('@')
	data = { 
		'addr': {'pubkey': pubkey,'host': host}
	}
	# 'perm': True, 
	# 'pubkey': '037f990e61acee8a7697966afd29dd88f3b1f8a7b14d625c4f8742bd952003a590',
	# 'host': '185.5.53.91:9735'
	lnreq = sendPostRequest(url,data)
	return lnreq

def openChannel(pk,sats,fee=1):
	url = '/v1/channels'
	apk = f'{pk}'.encode('UTF-8')
	data = {
		'node_pubkey': base64.b64encode(apk).decode(),
		'node_pubkey_string': f'{pk}',
		'local_funding_amount':f'{sats}',
		'sat_per_byte': f'{fee}'
		}
	lnreq = sendPostRequest(url,data)
	# if 'error' in lnreq.keys():
	pprint(lnreq)
	try:
		txid = codecs.encode(lnreq['funding_txid_bytes'].encode('UTF-8'),'hex')
		print(f"TXID:\n{ txid }")
		return txid
	except KeyError:
		error = lnreq['error']
		print(f"ERROR OPENING CHANNEL:\n\n{error}")
		# Parse out the numbers in the failure, and do something with it
		d = [float(i) for i in list(map(lambda x: x if x.replace('.', '', 1).isdigit() else print(x),error.split(' '))) if i ]
		d = list(map(lambda x: int(x*100000000), d))
		print(d)
		print(d[0]-d[1])
		return error


def streamInvoices():
	url = base_url + '/v1/invoices/subscribe'
	r = requests.get(url+'?add_index=1', stream=True, headers=headers, verify=cert_path)
	for line in r.iter_lines():
		a = json.loads(line.decode("UTF-8"))
		print(a)


def CP2CID(chan_point, chan_list):
	chan_list.reset_index(inplace=True)
	a = chan_list[channel_point==chan_point]
	return a.chan_id
# need channel point to chan_id
# Stuck here
def listChanFees(chan_id=None):
	lnreq = sendGetRequest(url14)
	z = pandas.DataFrame(lnreq['channel_fees'])
	z = z.rename(columns={'chan_point':'channel_point'})
	# z = z.set_index("channel_point")
	clist = listChannels()
	clist = clist.rename(columns={'remote_pubkey':'pubkey'})
	# z['chan_id'] = z['channel_point'].apply(lambda x: CP2CID(x,clist) )
	b = getChanPolicy(clist.iloc[0,:].chan_id,clist.iloc[0,:].remote_pubkey)
# getChanPolicy(a.iloc[0,:].chan_id,)
	print(b)
	c = b.join(z)
	# x = chan_info.join(z).fillna(0)
	return c


# System Functions
def getInfo():
	url = '/v1/getinfo'
	lnreq = sendGetRequest(url)
	return lnreq
	
def getBlockHeight():
	return getInfo()['block_height']
	# return sendGetRequest(url2)['block_height']

def getMyPK():
	return getInfo()['identity_pubkey']

def getAlias(pubkey):
	lnreq = sendGetRequest(url4,pubkey)
	try:
		return lnreq['node']['alias']
	except KeyError as e:
		print(f"{pubkey} doesn't have an alias? Error: {e}")
		return "NONE?"

def getNodeInfo(pubkey):
	lnreq = sendGetRequest(url4,pubkey)
	try:
		return lnreq
	except KeyError as e:
		print(f"{pubkey} doesn't have an alias? Error: {e}")
		return "NONE?"

def decodePR(pr):
	lnreq = sendGetRequest(url6,pr)
	return lnreq

# Receiving Functions
def createInvoice(amt,memo):
	url = '/v1/invoices'
	data = {'memo':memo,'value':amt}
	lnreq = sendPostRequest(url8,data)
	return lnreq

def lookupInvoice(invoice_rhash):
	# lnreq = sendGetRequest(f'/v1/invoice/?r_hash={invoice_rhash}')
	# lnreq = sendGetRequest(f'/v1/invoice/',body={'r_hash':base64.b64encode('a733467edcd121c46138ae7d6aa1b743840513b3bb04dc6d435fde242ce121a0'.encode('UTF-8')).decode()})
	lnreq = sendGetRequest(f'/v1/invoice/',body=base64.b64encode('a733467edcd121c46138ae7d6aa1b743840513b3bb04dc6d435fde242ce121a0'.encode('UTF-8')).decode())
	return lnreq

def listInvoices(max_invs=1000):
	url = '/v1/invoices'
	lnreq = sendGetRequest(url+f"?num_max_invoices={max_invs}")
	df = pandas.DataFrame(lnreq['invoices'])
	print("Available Data Columns: ")
	print(df.columns)
	df = df.fillna('0')
	print(df[['memo','amt_paid_sat','state','settled','creation_date','settle_date','r_preimage']])
	df['creation_date_h'] = df.apply(lambda x: datetime.fromtimestamp(int(x['creation_date'])) if int(x['settle_date']) != 0 else 0, axis=1 )
	df['settle_date_h'] = df.apply(lambda x: datetime.fromtimestamp(int(x['settle_date'])) if int(x['settle_date']) != 0 else 0, axis=1 )
	
	# df['alias'] = Series(b).apply(lambda x: getAlias(x), axis=1 )
	# b= list(a.index)
	base_columns = ['memo','creation_date_h','state','settled','settle_date_h','amt_paid_sat','amt_paid_msat']
	
	return df[base_columns]
	# return df[['memo','amt_paid_sat','state','creation_date_h','settle_date_h','htlcs']]
	# datetime.fromtimestamp(x['creation_date'])

def decodePR(pr):
	lnreq = sendGetRequest(url6,pr)
	return lnreq

def showFunds():
	chain_funds_url = '/v1/balance/blockchain'
	on = sendGetRequest(chain_funds_url)
	offchain_funds_url = '/v1/balance/channels'
	off = sendGetRequest(offchain_funds_url)

	data = {'on-chain':on,'off-offchain':off}

	print(f'On-Chain: {on}\t Off-Chain: {off}')
	print(data)
	funds_frame = pandas.DataFrame(data)
	return funds_frame


def addFees(hop,fee_msat):
	hop['fee_msat'] = str(fee_msat)
	hop['fee'] = str(floor(int(fee_msat)/1000))
	print(getAlias(hop['pub_key']) )	
	pprint(hop)
	return hop

def addForwardandFees(route):
	num_hops = len(route['hops'])
	base_fee = 20100
	# fee_hops = num_hops - 1
	fee_hops = num_hops
	# No fee on last hop
	route['total_fees_msat'] = str( fee_hops * base_fee )
	route['total_fees'] = str( floor(int(route['total_fees_msat']) / 1000) ) 
	route['total_amt_msat'] = str( int( route['total_amt_msat']) + int( route['total_fees_msat'] ) )
	route['total_amt'] = str( floor(int( route['total_amt_msat'])/ 1000 ) )
	# del route['hops'][fee_hops][]
	pprint(route)
	# Iterate of hops and add fees
	hoplist = []
	bh = getBlockHeight()
	# tl = route['total_time_lock']
	tl_delta_total = bh
	max_tld = 0
	# route['hops'].reverse()
	time_lock = bh
	for hop in route['hops']:
		# Update fees on hop object
		ahop = addFees(hop,base_fee)
		tl_delta_total += 10

		# Figure out time lock delta
		pk = hop['pub_key']
		cid = hop['chan_id']
		ln = getChanPolicy(cid)

		if ln['node1_pub'] == pk:
			policy = ln['node1_policy']
		elif ln['node2_pub'] == pk:
			policy = ln['node2_policy']	

		# Determine max time lock of all the hops
		tld = policy['time_lock_delta']
		time_lock += tld
		# if tld > max_tld:
		# 	max_tld = tld
		# 	print(f"Found Higher Max TLD: {max_tld}")

		ahop['expiry'] = time_lock
		hoplist.append(ahop)

		

	# Override hoplist with hops with fees
	# hoplist.reverse()
	route['hops'] = hoplist
	route['total_time_lock'] = time_lock
	return route
	# hoplist = []
	# for hop in route['hops']:
	# 	hop
		

# def getForwards(start,end):
def getForwards(days_past=30):
	start = int( (datetime.now() - timedelta(days=days_past)).timestamp() )
	end = int( datetime.now().timestamp() )
	data = { 'start_time': start, 'end_time': end }
	lnreq = sendPostRequest(url18,data)
	fwd_frame = pandas.DataFrame(lnreq['forwarding_events'])
	# Convert Timestamp to nice datetime
	fwd_frame['datetime'] = fwd_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x)) )
	print(f'Number of Satoshi Made This Month: {pandas.to_numeric(fwd_frame["fee_msat"]).sum()/1000}!')
	print(f'AVG Number of Satoshi Made Per Day: {pandas.to_numeric(fwd_frame["fee_msat"]).sum()/1000/days_past}!')
	return fwd_frame

def queryRoute(src_pk, dest_pk, pay_amt=123,frame=False):
	target_url = f"/v1/graph/routes/{dest_pk}/{pay_amt}?source_pub_key={src_pk}&use_mission_control=true&final_cltv_delta=40&fee_limit.fixed=4"
	target_url
	lnreq = sendGetRequest(target_url)
	if frame:
		f = lnreq['routes'][0]
		f['total_fees_msat'] = '0'
		f['total_fees'] = '0'
		return f
	hops = lnreq['routes'][0]['hops']
	hoplist = []
	for hop in hops:
		hoplist.append(hop)
	# It only ever returns 1 route
	return lnreq['routes'][0]['hops']

def routeSetExpiry(hf):
	hf['alias'] = hf['pub_key'].apply(lambda x: getAlias(x) )
	# Store original df
	hf_base = hf.copy()
	# Remove final hop from frame
	hf = hf.head(len(hf)-1)
	# reverse order because first hop has longest expiry
	# hf = hf[::-1]
	# hf.at[len(b)-1,'expiry'] = getBlockHeight() + getChanPolicy(hf.iloc[0]['chan_id'],hf.iloc[0]['pub_key']).iloc[0]['time_lock_delta']
	# print(f'Current Block Height {getBlockHeight()}')
	# chan_fee_info = getChanPolicy(b.iloc[len(b)-1]['chan_id'], b.iloc[len(b)-1]['pub_key'])
	# hf.at[len(b)-1,'expiry'] = getBlockHeight() + chan_fee_info['time_lock_delta']
	# hf.at[len(b)-2,'expiry'] = hf.at[len(b)-1,'expiry'] + chan_fee_info['time_lock_delta']
	# Dont do last hops
	first = True
	for i in range(len(hf)-1, -1,-1):
		print(f"Hop Index:{i} {getAlias(hf.at[i,'pub_key'])}")
		chan_fee_info = getChanPolicy(hf.at[i,'chan_id'], hf.at[i,'pub_key'])
		if first:
			first = False
			hf.at[i,'expiry'] = getBlockHeight() + chan_fee_info.iloc[0]['time_lock_delta']
		else:
			hf.at[i,'expiry'] = hf.at[i+1,'expiry'] + int(chan_fee_info.iloc[0]['time_lock_delta'])

	hf = hf.append(hf_base.tail(1))
	hf.at[len(hf)-1,'expiry'] = hf.at[len(hf)-2,'expiry']
		# try:
		# 	hf.at[i,'expiry'] = hf.iloc[index+1]['expiry'] + int(chan_fee_info['time_lock_delta'])
		# except IndexError as e:
		# 	print("Out of bounds") #, use current height!")
			# hf.at[index,'expiry'] = getBlockHeight() + int(chan_fee_info['time_lock_delta'])
	return hf

def routeSetFees(hf):
	# Reset Frames Fees
	hf['fee_msat'] = 0
	hf['fee_sat'] = 0
	pay_amt_msat = hf.iloc[0]['amt_to_forward_msat']
	# No fee for last hop
	for i in range(len(hf)-2, -1,-1):
		chan_fee_info = getChanPolicy(hf.at[i,'chan_id'], hf.at[i,'pub_key'])
		print(chan_fee_info)
		# Calculate fee for each hop
		msats =  floor( int(chan_fee_info.iloc[0]['fee_rate_milli_msat'])/1000000 * 
			int(hf.at[i,'amt_to_forward'])/1000 + 
			int(chan_fee_info.iloc[0]['fee_base_msat']) 
		)
		hf.at[i,'fee_msat'] = 13000													
		hf.at[i,'fee_sat'] = floor(hf.at[i,'fee_msat']/1000)
		# hf.at[i,'fee_msat'] = msats															
		# hf.at[i,'fee_sat'] = floor(msats/1000)
	for i in range(len(hf)-1, -1,-1):
		try:
			hf.at[i,'amt_to_forward_msat'] = int(hf.at[i+1,'amt_to_forward_msat']) + int(hf.at[i,'fee_msat'])
		except KeyError:
			hf.at[i,'amt_to_forward_msat'] = int(pay_amt_msat) + int(hf.at[i,'fee_msat'])
		hf.at[i,'amt_to_forward'] = floor(hf.at[i,'amt_to_forward_msat']/1000)
	print(hf[['fee_sat','fee_msat','amt_to_forward','amt_to_forward_msat']])

	hf['fee'] = hf['fee_sat']
	return hf
	# col = list(set(hf.columns) - set(['fee']))
	# return hf[col]

def hopFrame(hops):
	# Create Frame
	hframe = pandas.DataFrame(hops)
	# Make sure this has a value, for some reason API doesnt return anything if false
	hframe['tlv_payload'] = hframe['tlv_payload'].fillna(False)

	# Add fee columns
	if "fee_msat" not in list(hframe.columns):
		hframe.insert(1,'fee_msat','0')
	if "fee_sat" not in list(hframe.columns):
		hframe.insert(1,'fee_sat','0')

	# Store original hop dataframe
	hframe_base = hframe
	# Reverse order
	# hframe = hframe.iloc[::-1]
	# policy = pandas.DataFrame()
	# Get policy for first hop
	# policy = policy.append()
	# for index, row in hframe.iterrows():
	# 	policy = policy.append(getChanPolicy(row['chan_id'],row['pub_key']))

	# policy = policy.fillna(0)
	# policy = policy.rename(columns={'pubkey':'pub_key'})
	# hframe = hframe.merge(policy,on='pub_key')
	return hframe


# ON-CHAIN
def listChainTxns(show_columns=False,add_columns=None):
	url = '/v1/transactions'
	lnreq = sendGetRequest(url)
	lnframe = pandas.DataFrame(lnreq['transactions'])
	lnframe['ts_h'] = lnframe.apply(lambda x: datetime.fromtimestamp(int(x['time_stamp'])), axis=1 )
	default_columns = ['ts_h','num_confirmations','amount','tx_hash','total_fees']
	if add_columns != None:
		default_columns = default_columns + add_columns
	if show_columns:
		print(lnframe.columns)

	return lnframe[default_columns]

def closeChannel(channel_point,output_index=0,force=False):
	url = f'/v1/channels/{channel_point}/{output_index}?force={force}'
	query = {
		'force':force,
		'sat_per_byte':'1'
	}
	# ,query
	x = sendDeleteRequest(url)
	return x
	# DELETE /v1/channels/{channel_point.funding_txid_str}/{channel_point.output_index}

def listCoins():
	url = '/v1/utxos'
	lnreq = sendGetRequest(url)
	lnframe = pandas.DataFrame(lnreq['utxos'])
	return lnframe


def blahroute():
	# # def buildRoute():
	# # 	# Destination pubkey
	# whenbtc --> lnbig
	# Hop1
	hoplist = []
	pay_amt = 5000

	dest_pub_key = creampay
	src_pub_key = my_key
	target_url = url15.format(pub_key=dest_pub_key,amt=pay_amt) + f"?source_pub_key={src_pub_key}&use_mission_control=false&final_cltv_delta=144"
	target_url
	lnreq = sendGetRequest(target_url)
	hops = lnreq['routes'][0]['hops']
	for hop in hops:
		hoplist.append(hop)

	dest_pub_key = bitrefill
	src_pub_key = creampay
	target_url = url15.format(pub_key=dest_pub_key,amt=pay_amt) + f"?source_pub_key={src_pub_key}&use_mission_control=false&final_cltv_delta=144"
	target_url
	lnreq = sendGetRequest(target_url)
	hops = lnreq['routes'][0]['hops']
	for hop in hops:
		hoplist.append(hop)


	dest_pub_key = lnbig
	src_pub_key = bitrefill
	target_url = url15.format(pub_key=dest_pub_key,amt=pay_amt) + f"?source_pub_key={src_pub_key}&use_mission_control=false&final_cltv_delta=144"
	target_url
	lnreq = sendGetRequest(target_url)
	hops = lnreq['routes'][0]['hops']
	for hop in hops:
		hoplist.append(hop)

	dest_pub_key = my_key
	src_pub_key = lnbig
	target_url = url15.format(pub_key=dest_pub_key,amt=pay_amt) + f"?source_pub_key={src_pub_key}&use_mission_control=false&final_cltv_delta=144"
	target_url
	lnreq = sendGetRequest(target_url)
	hops = lnreq['routes'][0]['hops']
	for hop in hops:
		hoplist.append(hop)

	# Add fees in sat and msat manually?? 
	# hoplist = lambda x


	hop_frame = pandas.DataFrame(hoplist)
	hop_frame = hop_frame.rename(columns={'pub_key':'remote_pubkey'})
	hop_frame['alias'] = hop_frame.apply(lambda x: getAlias(x.remote_pubkey), axis=1)

	hop_frame



	# hops_fees = [addFees(hop) for hop in hoplist] 
	send_route = lnreq['routes'][0]


	# Uses routes object, but add all hops
	send_route['hops'][:] = []
	send_route['hops'] = hoplist



	# send_route = addForwardandFees(send_route)
	pprint(send_route)



	# chan_info = getChannelBalance()
	# balances = chan_info[['alias','chan_id','balanced','local_balance','remote_balance']]
	# balances


	# invoice = createInvoice(pay_amt,'rebalance test')
	# pay_hash = decodePR(invoice['payment_request'])['payment_hash']

	# reverse order of hops
	# send_route['hops'].reverse()

	return send_route
	# lnreq = PayByRoute(send_route)
	# lnreq





code.interact(local=locals())




# Start at pubkey of node to rebalance
# Set Source their and dest to bitrefill
# Set Source of bitrefill to dest target node

# bosworth
# longest expiry, first hop
# last hop isnt really hop at all, its the destination

# The expiry is about when you get your outbound funds back but the last hop has no outbound funds
# Yeah like if you pay a direct peer some money there is no compensation necessary for forwarding
# fractions of a msat: rounded down

# roasbeef
# if the last node gets a CLTV of 40, and the onion says it should be 50, then they’ll reject the HTLC
# we send the information twice basically: what the penultimate node shoudl extend, and what the final node should receive

