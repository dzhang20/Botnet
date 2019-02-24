import logging
import asyncio
import sys

from Crypto import Signature, PublicKey, Hash

from kademlia.network import Server

if sys.argc != 5:
    print("Usage: python set.py <bootstrap node> <bootstrap port> <key_file> <job_desc_file>")
    sys.exit(1)

loop = asyncio.get_event_loop()

server = Server()
server.listen(8469)
bootstrap_node = (sys.argv[1], int(sys.argv[2]))
loop.run_until_complete(server.bootstrap([bootstrap_node]))

with open(sys.argv[3], 'r') as f:
    key = PublicKey.RSA.import_key(f.read())
    verifier = Signature.pkcs1_15.new()

value = {}
with open(sys.argv[4], 'r') as f:
    value['job_data'] = f.read()

hash = Hash.SHA256.new(data=value['job_data']).digest()
value['sig'] = verifier.sign(hash)

loop.run_until_complete(server.set('task', value))
server.stop()
loop.close()
