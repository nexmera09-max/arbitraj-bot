import asyncio
import aiohttp
import time

class GlobalScanner:
    def __init__(self):
        self.binance_url = "https://api.binance.com/api/v3/ticker/bookTicker?symbol=BTCUSDT"
        self.bybit_url = "https://api.bybit.com/v5/market/tickers?category=linear&symbol=BTCUSDT"

    async def fetch(self, session, url):
        try:
            async with session.get(url, timeout=2) as response:
                if response.status == 200:
                    return await response.json()
        except:
            return None

    async def start_hunting(self):
        print("🤖 [SİSTEM BAŞLADI] 7/24 Küresel Arbitraj Motoru devrede...")
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.fetch(session, self.binance_url), self.fetch(session, self.bybit_url)]
                results = await asyncio.gather(*tasks)

                if results[0] and results[1]:
                    try:
                        b_ask = float(results[0]['askPrice'])
                        b_bid = float(results[0]['bidPrice'])
                        by_ask = float(results[1]['result']['list'][0]['ask1Price'])
                        by_bid = float(results[1]['result']['list'][0]['bid1Price'])

                        if b_bid > by_ask:
                            print(f"🚨 [FIRSAT] Bybit'ten AL ({by_ask}) -> Binance'te SAT ({b_bid})")
                        elif by_bid > b_ask:
                            print(f"🚨 [FIRSAT] Binance'ten AL ({b_ask}) -> Bybit'te SAT ({by_bid})")
                    except:
                        pass
                await asyncio.sleep(0.05)

if __name__ == "__main__":
    bot = GlobalScanner()
    asyncio.run(bot.start_hunting())
