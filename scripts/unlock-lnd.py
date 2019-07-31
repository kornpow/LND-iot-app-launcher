import sys
# We put the Google GRPC stuff here for now
sys.path.append("/usr/src/app")
import codecs, grpc, os
import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc

os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/root/.lnd/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.WalletUnlockerStub(channel)
# This is not how we should do this long term
wallet_pass = bytes(os.environ["LND_PASS"],"UTF-8")
request = ln.UnlockWalletRequest(wallet_password=wallet_pass)
response = stub.UnlockWallet(request)
print(response)