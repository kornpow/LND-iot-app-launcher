import sys
import os
sys.path.append("/usr/src/app")
import codecs, grpc, os
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc


import requests
from cryptography.fernet import Fernet

def createAndSaveKey():
	key = Fernet.generate_key()
	with open(os.path.expanduser("~") + "/atestkey.key", 'wb') as f:
		f.write(key)
	return key

def encrypt(message: bytes, key: bytes) -> bytes:
	return Fernet(key).encrypt(message)

def decrypt(token: bytes, key: bytes) -> bytes:
	return Fernet(key).decrypt(token)

url = "https://enteryourawsurlhere.com/dev"

if __name__ == '__main__':
	# Send a post request to specified secret URL, which responds with the encrypted passphrase
	wallet_pass_enc = requests.post(url).text.encode("UTF-8")
	with open(os.path.expanduser("~") + "/atestkey.key", 'rb') as f:
		mykey = f.read()

	wallet_pass = decrypt(wallet_pass_enc, mykey)
	# wallet_pass = bytes(os.environ["LND_PASS"],"UTF-8")
	os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
	cert = open('/root/.lnd/tls.cert', 'rb').read()
	ssl_creds = grpc.ssl_channel_credentials(cert)
	channel = grpc.secure_channel('localhost:10009', ssl_creds)
	stub = lnrpc.WalletUnlockerStub(channel)
	# This is not how we should do this long term
	
	request = ln.UnlockWalletRequest(wallet_password=wallet_pass)
	response = stub.UnlockWallet(request)
	print(response)