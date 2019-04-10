import rpc_pb2 as ln, rpc_pb2_grpc as lnrpc
import code
import codecs, grpc, os
import json


macaroon = codecs.encode(open('/root/.lnd/data/chain/bitcoin/mainnet/admin.macaroon', 'rb').read(), 'hex')
os.environ['GRPC_SSL_CIPHER_SUITES'] = 'HIGH+ECDSA'
cert = open('/root/.lnd/tls.cert', 'rb').read()
ssl_creds = grpc.ssl_channel_credentials(cert)
channel = grpc.secure_channel('localhost:10009', ssl_creds)
stub = lnrpc.LightningStub(channel)


request = ln.ListChannelsRequest()
response = stub.ListChannels(request, metadata=[('macaroon', macaroon)])


for chan in response.channels:
   request = ln.NodeInfoRequest(pub_key=chan.remote_pubkey)
   r = stub.GetNodeInfo(request, metadata=[('macaroon', macaroon)])
   chan_partner_alias = r.node.alias
   print( "%s\t%s\t%f" % ( chan_partner_alias, chan.remote_pubkey, ( chan.local_balance / ( chan.local_balance+chan.remote_balance ) ) ) )


# Query routes for one direction
request = ln.QueryRoutesRequest(
   pub_key="027ce055380348d7812d2ae7745701c9f93e70c1adeb2657f053f91df4f2843c71",
   amt=300000,
   num_routes=5,
)
response = stub.QueryRoutes(request, metadata=[('macaroon', macaroon)])
print(response)
topartner = response.routes

request = ln.GetInfoRequest()
response = stub.GetInfo(request, metadata=[('macaroon', macaroon)])
print(response)
mypub = response.identity_pubkey

request = ln.QueryRoutesRequest(
   pub_key=mypub,
   amt=300000,
   num_routes=5,
   source_pub_key="027ce055380348d7812d2ae7745701c9f93e70c1adeb2657f053f91df4f2843c71",
)
response = stub.QueryRoutes(request, metadata=[('macaroon', macaroon)])
print(response)
frompartner = response.routes