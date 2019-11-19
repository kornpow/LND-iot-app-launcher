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

# LND_DIR = '/home/lightning/.lnd/'
LND_DIR = '/home/skorn/kornpow_cloud/.lnd/'

# with open(LND_DIR + 'mainnet/admin.macaroon', 'rb') as f:
# 	hex_content = binascii.b2a_hex(f.read())

macaroon = codecs.encode(open(LND_DIR + 'data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
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

# {'Grpc-Metadata-macaroon': b'0201036c6e6402cf01030a106271d20b342cb9715ab7f5813f88d00a1201301a160a0761646472657373120472656164120577726974651a130a04696e666f120472656164120577726974651a170a08696e766f69636573120472656164120577726974651a160a076d657373616765120472656164120577726974651a170a086f6666636861696e120472656164120577726974651a160a076f6e636861696e120472656164120577726974651a140a057065657273120472656164120577726974651a120a067369676e6572120867656e65726174650000062042d508b098e94db9256b10f4fe9134b516777bc5b38d3e17b757fddcf9d1d7c7'}
base_url = 'https://45.63.16.216:8080'

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

##### Base GET/POST  REQUEST
def sendPostRequest(endpoint,data=""):
	url = base_url + endpoint
	r = requests.post(url, headers=headers, verify=cert_path, data=json.dumps(data))
	# pprint(r.json())
	return r.json()

def sendGetRequest(endpoint, data=""):
	url = base_url + endpoint.format(data)
	print(f"GET: {url}")
	r = requests.get(url, headers=headers, verify=cert_path)
	# pprint(r.json())
	return r.json()



##### Payment Functions
def sendPaymentByReq(payreq, outid = None):
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

def getChanPoint(chanid):
	lnreq = sendGetRequest(url17,str(chanid) )
	cp = lnreq['chan_point']
	return cp

# Channel Functions
def getChanPolicy(chanid, pubkey=None):
	lnreq = sendGetRequest(url17,str(chanid) )
	df = pandas.DataFrame.from_dict({lnreq['node1_pub']:lnreq['node1_policy'],lnreq['node2_pub']:lnreq['node2_policy']})
	df = df.T
	df.reset_index(inplace=True)
	df.rename(columns={'index':'pubkey'}, inplace=True)
	df['alias'] = df['pubkey'].apply(lambda x: getAlias(x))
	if pubkey:
		df = df[df.pubkey==pubkey]
	# print(df)
	return df

def getBalance(row):
	return row['local_balance'] / (row['local_balance']+row['remote_balance'])

def listChannels(chanpoint=None,all=False):
	lnreq = sendGetRequest(url5)
	d = pandas.DataFrame(lnreq['channels'])
	y = d[['chan_id','channel_point','remote_pubkey','local_balance','remote_balance']].fillna(0)
	# Convert columns to integers
	y[['local_balance','remote_balance']] = y[['local_balance','remote_balance']].apply(pandas.to_numeric, errors='coerce')
	y['balanced'] = y.apply(getBalance, axis=1)
	y['alias'] = y.apply(lambda x: getAlias(x.remote_pubkey), axis=1)
	y = y.set_index("channel_point")
	if chanpoint:
		y = y[y.index==chanpoint]
	if all:
		return y
	else:
		return y[['alias','balanced','local_balance','remote_balance','chan_id','remote_pubkey']]

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
def getBlockHeight():
	return sendGetRequest(url2)['block_height']

def getMyPK():
	return sendGetRequest(url2)['identity_pubkey']

def getAlias(pubkey):
	lnreq = sendGetRequest(url4,pubkey)
	try:
		return lnreq['node']['alias']
	except KeyError as e:
		print(f"{pubkey} doesn't have an alias? Error: {e}")
		return "NONE?"

def decodePR(pr):
	lnreq = sendGetRequest(url6,pr)
	return lnreq

# Receiving Functions
def createInvoice(amt,memo):
	data = {'memo':memo,'value':amt}
	lnreq = sendPostRequest(url8,data)
	return lnreq

def listInvoices(max_invs=25):
	lnreq = sendGetRequest(url8+f"?num_max_invoices={max_invs}")
	df = pandas.DataFrame(lnreq['invoices'])
	print("Available Data Columns: ")
	print(df.columns)
	df = df.fillna('0')
	print(df[['memo','amt_paid_sat','state','settled','creation_date','settle_date','r_preimage']])
	df['creation_date_h'] = df.apply(lambda x: datetime.fromtimestamp(int(x['creation_date'])) if int(x['settle_date']) != 0 else 0, axis=1 )
	df['settle_date_h'] = df.apply(lambda x: datetime.fromtimestamp(int(x['settle_date'])) if int(x['settle_date']) != 0 else 0, axis=1 )
	
	# df['alias'] = Series(b).apply(lambda x: getAlias(x), axis=1 )
	# b= list(a.index)
	
	return df[['memo','amt_paid_sat','state','creation_date_h','settle_date_h','htlcs']]
	# datetime.fromtimestamp(x['creation_date'])

def decodePR(pr):
	lnreq = sendGetRequest(url6,pr)
	return lnreq



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
def getForwards():
	start = int( (datetime.now() - timedelta(days=30)).timestamp() )
	end = int( datetime.now().timestamp() )
	data = { 'start_time': start, 'end_time': end }
	lnreq = sendPostRequest(url18,data)
	fwd_frame = pandas.DataFrame(lnreq['forwarding_events'])
	# Convert Timestamp to nice datetime
	fwd_frame['datetime'] = fwd_frame['timestamp'].apply(lambda x: datetime.fromtimestamp(int(x)) )
	return fwd_frame

def queryRoute(src_pk, dest_pk, pay_amt=100):
	target_url = url15.format(pub_key=dest_pk,amt=pay_amt) + f"?source_pub_key={src_pk}&use_mission_control=true&final_cltv_delta=144&fee_limit.fixed=4"
	target_url
	lnreq = sendGetRequest(target_url)
	hops = lnreq['routes'][0]['hops']
	hoplist = []
	for hop in hops:
		hoplist.append(hop)

	# It only ever returns 1 route
	return lnreq['routes'][0]

def hopFrame(hops):
	# Create Frame
	hframe = pandas.DataFrame(hops)
	# Add fee columns
	if "fee_msat" not in list(hframe.columns):
		hframe.insert(1,'fee_msat','0')
	if "fee_sat" not in list(hframe.columns):
		hframe.insert(1,'fee_sat','0')

	# Reverse order
	hframe = hframe.iloc[::-1]
	policy = pandas.DataFrame()
	for index, row in hframe.iterrows():
		policy = policy.append(getChanPolicy(row['chan_id'],row['pub_key']))

	policy = policy.rename(columns={'pubkey':'pub_key'})
	hframe = hframe.merge(policy,on='pub_key')
	

	pay_amt_msat = hframe.iloc[0]['amt_to_forward_msat']
	for index, row in hframe[1:].iterrows():
		msats =  floor(int(row['fee_rate_milli_msat'])/1000000 * int(row['amt_to_forward'])/1000 + int(row['fee_base_msat']) )
		hframe.at[index,'fee_msat'] = msats
		hframe.at[index,'fee_sat'] = floor(msats/1000)

	total_fee_msat = fsum(hframe['fee_msat'].astype(int))
	# Reverse order again
	hframe = hframe.iloc[::-1]

	for index, row in hframe.iterrows():
		pass

	# hframe['fees'] = hframe.apply( lambda x: getChanPolicy(x['chan_id'],x['pub_key']) , axis=1)
	# getChanPolicy('664234765602914304','02c69a0b4cb468660348d6d457d9212563ad08fb94d424395da6796fb74a13f276')
	# Export back to list of dicts
	pprint(hframe.to_dict('records'))


	# fee_msat
	# fee_sat
	return hframe


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


	# code.interact(local=locals())

# route = blahroute()
apr = 'lnbc20u1pwuhyrupp54uph3jdveeu7f5ylxu6l2ztwynvydckc5ps2gnt5c6ty40f9vwvqdqswfjkyctvv9hxxef3cqzpgelz29mm4m7r5vsuxarkuex0h7c0qlhefe37l56gn677e6gpafayns7df02dq7pacrt29dcfdavu2usy9s2s4urlk0ta02cad6qhg50qpgwkfxs'
pr = decodePR(apr)

ph = pr['payment_hash']
# getAlias('')
# getChanPolicy('')


# lnreq = PayByRoute(send_route)
# lnreq

# aroute = {'hops': [{'amt_to_forward': '75',
#                              'amt_to_forward_msat': '75000',
#                              'chan_capacity': '8000000',
#                              'chan_id': '659227589725585409',
#                              'expiry': 603682,
#                              'fee_msat': '400',
#                              'pub_key': '03da1c27ca77872ac5b3e568af30673e599a47a5e4497f85c7b5da42048807b3ed',
#                              'tlv_payload': True},
#                             {'amt_to_forward': '75',
#                              'amt_to_forward_msat': '75000',
#                              'chan_id': '622281799946731520',
#                              'expiry': 603538,
#                              'pub_key': '03864ef025fde8fb587d989186ce6a4a186895ee44a926bfc370e2c366597a3f8f',
#                              'tlv_payload': True},
#                             {'amt_to_forward': '75',
#                              'amt_to_forward_msat': '75000',
#                              'chan_id': '632587522506096640',
#                              'expiry': 603538,
#                              'pub_key': '024655b768ef40951b20053a5c4b951606d4d86085d51238f2c67c7dec29c792ca'}],
#                    'total_amt': '75',
#                    'total_amt_msat': '75400',
#                    'total_fees_msat': '400',
#                    'total_time_lock': 603712}


# route1 = queryRoute(my_key,nodroid,2000)
# lnreq = PayByRoute(route1,ph)


# a = listChannels()
aroute = blahroute()
hframe = hopFrame(aroute['hops'])
# b = listChanFees()


code.interact(local=locals())




# Start at pubkey of node to rebalance
# Set Source their and dest to bitrefill
# Set Source of bitrefill to dest target node

# longest expiry, first hop
# last hop isnt really hop at all, its the destination

# The expiry is about when you get your outbound funds back but the last hop has no outbound funds
# Yeah like if you pay a direct peer some money there is no compensation necessary for forwarding
# fractions of a msat: rounded down


# 1sat + (250,000 * 1 / 1000000)
# 1sat + (250,000 * 0.000001) = 1.25sat
# LNBig:
# 1sat + (250,000 * 3200 / 1000000)
# 1sat + (250000 * 0.003200)  = 801sat 

