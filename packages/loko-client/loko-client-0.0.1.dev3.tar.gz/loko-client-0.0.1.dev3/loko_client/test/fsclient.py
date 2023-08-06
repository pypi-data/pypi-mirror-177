from loko_client.business.fs_client import FSClient

GATEWAY = 'http://localhost:9999/routes/'

fsclient = FSClient(gateway=GATEWAY)
print(fsclient.ls('data/data/datasets'))
content = fsclient.read('data/data/datasets/titanic.csv', mode='rb')
print(content.decode())
### save file ###
print(fsclient.save('data/data/test/test.csv', content))
print(fsclient.save('data/data/test2/test.csv', content))
### save dir ###
print(fsclient.save('data/data/test3'))
### delete dir ###
print(fsclient.delete('data/data/test2/'))
### delete file ###
print(fsclient.delete('data/data/test/test.csv'))
### copy file in existing directory ###
print(fsclient.save('data/data/test3/test.csv', content))
print(fsclient.copy('data/data/test3/test.csv', 'data/data/test3/test2.csv'))
### move file in existing directory ###
print(fsclient.move('data/data/test3/test.csv', 'data/data/test.csv'))
### update ###
print(fsclient.update('data/data/test.csv', 'hello'.encode()))
