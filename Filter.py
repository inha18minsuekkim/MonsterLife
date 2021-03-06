#from getRequest import getMonsterData
import asyncio
import aiohttp
from functools import reduce
import pandas as pd
res = []
flag = True
async def getMonsterData(session,monstername):
    global flag
    data = {'monster':monstername}
    async with session.post('http://wachan.me/farm_read2.php',data=data) as resp:
        tmp = await resp.json(content_type='text/html')
        print(tmp)
        if not tmp['error']:
            tmp = pd.DataFrame(tmp)
            tmp.drop('error',axis=1)
            tmp['farm_list'] = tmp['farm_list'].apply(lambda x: x[0])
            res.append(tmp)
        else:
            flag = False
async def Filter(args):
    global flag
    flag = True
    async with aiohttp.ClientSession() as session:
        await asyncio.gather(*[getMonsterData(session,x) for x in args])
    tmp = reduce(lambda left, right: pd.merge(left, right, on='farm_list'), res)
    if flag:
        return tmp['farm_list'].to_list()
    else:
        return None

if __name__ == '__main__':
    print(asyncio.run(Filter([u'릴리노흐',u'장난감 흑기사',u'바이킹 군단'])))
