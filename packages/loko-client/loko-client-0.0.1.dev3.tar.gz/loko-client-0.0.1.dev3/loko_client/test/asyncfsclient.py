import sys
import asyncio
from loko_client.business.fs_client import AsyncFSClient

async def get_chunked_file(path):
    resp = await fsclient.read(path, content=True)
    async for line in resp:
        print(line)

GATEWAY = 'http://localhost:9999/routes/'
fsclient = AsyncFSClient(gateway=GATEWAY)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
task = loop.create_task(fsclient.ls('data/data/datasets'))
r = loop.run_until_complete(task)
print(r)
### read file ###
task = loop.create_task(fsclient.read('data/data/datasets/titanic.csv', mode='r'))
content = loop.run_until_complete(task)
print(content)
### read content ###
task = loop.create_task(get_chunked_file('data/data/datasets/titanic.csv'))
loop.run_until_complete(task)
# sys.exit(0)
### save file ###
task = loop.create_task(fsclient.save('data/data/test/test.csv', body=content))
r = loop.run_until_complete(task)
print(r)
task = loop.create_task(fsclient.save('data/data/test2/test.csv', body=content))
r = loop.run_until_complete(task)
print(r)
### save dir ###
task = loop.create_task(fsclient.save('data/data/test3'))
r = loop.run_until_complete(task)
print(r)
### delete dir ###
task = loop.create_task(fsclient.delete('data/data/test2/'))
r = loop.run_until_complete(task)
print(r)
### delete file ###
task = loop.create_task(fsclient.delete('data/data/test/test.csv'))
r = loop.run_until_complete(task)
print(r)
### copy file in existing directory ###
task = loop.create_task(fsclient.save('data/data/test3/test.csv', content))
r = loop.run_until_complete(task)
print(r)
task = loop.create_task(fsclient.copy('data/data/test3/test.csv', 'data/data/test3/test2.csv'))
r = loop.run_until_complete(task)
print(r)
### move file in existing directory ###
task = loop.create_task(fsclient.move('data/data/test3/test.csv', 'data/data/test.csv'))
r = loop.run_until_complete(task)
print(r)
### update ###
task = loop.create_task(fsclient.update('data/data/test.csv', 'hello'.encode()))
r = loop.run_until_complete(task)
print(r)