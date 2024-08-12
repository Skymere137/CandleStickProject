import requests
import asyncio
import pandas as pd
import json
import os

token = os.environ["dataToken"]

loop = asyncio.get_event_loop()

async def get_symbol(symbol):
    url = f"https://eodhd.com/api/eod/{symbol}.US?api_token={token}&fmt=json"
    data = requests.get(url).json()
    return data

async def get_watchlist():
    url = f"""https://eodhd.com/api/screener?api_token={token}&sort=market_capitalization.desc&filters=[
    ["market_capitalization", "<", 2000000000],
    ["exchange", "=", "us"], ["avgvol_1d", ">", "20000000"]
    ]&limit=5&offset=0"""

    data = requests.get(url).json()

    watchlist = {}

    for item in data["data"]:
        if item["market_capitalization"] > 300000000:
            ticker =  item["code"]
            mkt_cap = item["market_capitalization"]
            current_price = item["adjusted_close"]
            volume = item["avgvol_200d"]
            date = item["last_day_data_date"]

            watchlist[item["name"]] = {
                "ticker": ticker,
                "mkt_cap": mkt_cap,
                "price": current_price,
                "volume": volume,
                "date": date
            }
    return watchlist
async def get_watchlist_data(dict):
    for key, value in dict.items():
        data = await get_symbol(value["ticker"])
        os.chdir(f"{os.path.dirname(os.path.abspath(__file__))}/data")
        with open(f"{value['ticker']}.json", "w") as file:
            json.dump(data, file)

async def run_tasks():
    watchlist = await get_watchlist()
    
    await asyncio.gather(asyncio.create_task(get_watchlist_data(watchlist)))

if __name__ == "__main__":
    results = asyncio.run(run_tasks())