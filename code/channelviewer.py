import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
import code
import codecs, grpc, os


macaroon = codecs.encode(open('/root/.lnd/data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/root/.lnd/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)


request = ln.ListChannelsRequest()
response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])

print(response)
