import pandas as pd
import json
import os
import mplfinance as mpf
import candle_utils


def pattern(row):
    open = row["open"]
    close = row["close"]
    high = row["high"]
    low = row["low"]
    volume = row["volume"]
    result = ""
    bullish = None
    bullish_patterns_funcs = [is_bull]
    bearish_patterns_funcs = [is_bear]

    if open < close:
        bullish = True
    if open > close:
        bullish = False
    
    if bullish is True:
        for func in bullish_patterns_funcs:
            return func(open, close, high, low)
        
    if bullish is False:
        for func in bearish_patterns_funcs:
            return func(open, close, high, low)

    elif bullish is None:
        return "Doji"
    
def is_bull(open, close, high, low):
    try:
        star_ratio = (open - low) / (close - open)
        full_ratio = (close - open) / ((high - close) + (open- low))
    except ZeroDivisionError:
        star_ratio = float("inf")
        full_ratio = float("inf")

    if star_ratio > 10:
        return "Possible Doji" 
    if star_ratio > 3:      
        return "Bullish Star"
    if full_ratio> 5:
        return "Bullish Full"
    
    return "No match Could be found!!!"
        
def is_bear(open, close, high, low):
    try:
        star_ratio = ((high - open) / (open - close))
        full_ratio = ((open - close) / ((high - open) + (close - low)))
    except ZeroDivisionError:
        star_ratio = float("inf")
        full_ratio = float("inf")

    if star_ratio > 10:
        return "Possible Doji"
    if star_ratio > 3:
        return "Bearish Star"
    if full_ratio > 5:
        return "Bearish Full"

    return "No match Could be found!!!"

def fib_retracement(high, low):
    ranges = high - low
    red = (ranges * 0.236) + low
    oj = (ranges * 0.382) + low
    mid = (ranges * 0.5) + low
    green = (ranges * 0.618) + low
    teal = (ranges * 0.786) + low
    fib_nums = [red, oj, mid, green, teal]
    return fib_nums

data = pd.read_json(r"testing_data/ACHR.json")
data = pd.DataFrame(data)

data["date"] = pd.to_datetime(data["date"])
data.set_index(["date"], inplace=True)

data["pattern"] = [pattern(row) for _, row in data.iterrows()]
data["pattern"] = data["pattern"].astype(str)

highlight = data[data["volume"] >= data["volume"].quantile(0.9)]
highlight = highlight.reindex(data.index)

volume_max = float(data["volume"].median())

ap = mpf.make_addplot(highlight["close"], scatter=True, marker=".", color="blue", markersize=100)

mpf.plot(data, type="candle", style="charles", title="Candle Stick Chart", ylabel="price", addplot=ap)

# hline = mpf.make_addplot([volume_max] * len(data), color="green", linestyle="dashed", secondary_y=False)
# mpf.plot(data[["volume"]], type="line", title="Volume Chart", ylabel="volume", addplot=hline)

