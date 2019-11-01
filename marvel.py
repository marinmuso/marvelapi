import asyncio
import aiofiles
import aiohttp
import hashlib
import json
import os
import time
import requests


PUBLIC_KEY = os.environ['PUBLIC_KEY']
PRIVATE_KEY = os.environ['PRIVATE_KEY']
MARVEL_OBJ = 'characters comics creators events series stories'.split()


def get_ts_hash():
    ts = str(time.time())
    secret = (ts + PRIVATE_KEY + PUBLIC_KEY).encode('utf-8')
    md = hashlib.md5(secret)
    hash = md.hexdigest()
    return ts, hash


def get_api_endpoint(marvel_obj):
    endpoint = ('http://gateway.marvel.com/v1/public/{marvel_obj}?ts={ts}&'
                'apikey={public_key}&hash={hash}')
    ts, hash = get_ts_hash()
    url = endpoint.format(marvel_obj=marvel_obj,
                          ts=ts,
                          public_key=PUBLIC_KEY,
                          hash=hash)
    return url


async def dump_data(data, marvel_obj):
    async with aiofiles.open(f'{marvel_obj}.json', 'a+') as json_file:
        for row in data['data']['results']:
            json_obj = json.dumps(row, indent=2)
            await json_file.write(json_obj)


async def cache_data(marvel_obj):
    url = get_api_endpoint(marvel_obj)
    total_data_points = requests.get(url).json()['data']['total']
    lim = 100
    offset_mult = 0
    print(f'working on {marvel_obj}, total data points: {total_data_points}')
    for _ in range(round(total_data_points/lim)):
        params = {'limit': lim,
                  'offset': lim * offset_mult}
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as res:
                try:
                    data = await res.json()
                    await dump_data(data, marvel_obj)
                except Exception as e:
                    print('error', e)
                    pass
        offset_mult += 1
    print(f'done dumping {marvel_obj}')


async def main():
    semaphore = asyncio.Semaphore()
    async with semaphore:
        tasks = [cache_data(obj) for obj in MARVEL_OBJ]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        print(f'error: {e}')
        pass
