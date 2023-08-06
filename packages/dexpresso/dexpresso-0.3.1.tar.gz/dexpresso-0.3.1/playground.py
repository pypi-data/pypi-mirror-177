import asyncio
import time

import aiohttp  # pip install aiohttp aiodns


async def get(
    session: aiohttp.ClientSession,
    address: str,
    **kwargs
) -> dict:
    url = f"https://mainnet-idx.algonode.cloud/v2/accounts/{address}"
    # print(f"Requesting {url}")
    resp = await session.request('GET', url=url, **kwargs)
    # Note that this may raise an exception for non-2xx responses
    # You can either handle that here, or pass the exception through
    data = await resp.json()
    # print(data['account']['amount'])
    return data['account']['amount']


async def main(addresses, **kwargs):
    # Asynchronous context manager.  Prefer this rather
    # than using a different session for each GET request
    async with aiohttp.ClientSession() as session:
        tasks = []
        for c in addresses:
            tasks.append(get(session=session, address=c, **kwargs))
        # asyncio.gather() will wait on the entire task set to be
        # completed.  If you want to process results greedily as they come in,
        # loop over asyncio.as_completed()
        htmls = await asyncio.gather(*tasks, return_exceptions=True)
        return htmls


if __name__ == '__main__':
    now = time.time()
    addresses = ['ZW3ISEHZUHPO7OZGMKLKIIMKVICOUDRCERI454I3DB2BH52HGLSO67W754',
                 'YQTBGJDL5K5GFHWQEUTFPOJ5JSXOJH67G57NOMXRAMRQJ5LWJAOMWTPREM',
                 'MLD3LCNGOK2SXAVNUYMW3WVG5LBN4Z5HFARB3VLMZCENFWWJE7H2TLOASM',
                 ] * 33
    # Either take colors from stdin or make some default here
    asyncio.run(main(addresses))  # Python 3.7+
    now2 = time.time()
    print(now2 - now)
