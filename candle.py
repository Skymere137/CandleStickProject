import pandas as pd
import numpy as np
import json
import os
from custom_queue import Queue
import mplfinance as mpf
import matplotlib.pyplot as plt

class EstablishDataframe:
    def __init__(self, data, window=4, rvol_window=20):
        self.data = data
        self.data = pd.read_json(self.data)
        self.data = pd.DataFrame(self.data)
        self.data["date"] = pd.to_datetime(self.data["date"])
        self.data.set_index(["date"], inplace=True)
        self.queue = Queue(5)
        self.data = self.data_margin(self.data)
        self.window_size = pd.Timedelta(days=window)
        self.rvol_window = pd.Timedelta(days=rvol_window)

        for index in self.data.index:
            window_start = index - self.window_size
            window_data = self.data.loc[window_start:index, "close"]
            self.data.at[index, "mvAvg"] = window_data.mean()
            self.data["EMA"] = self.data["close"].ewm(span=window, adjust=False).mean()
            if self.queue.values:
                self.data.at[index, "RoC"] = self.calculate_roc(self.data.loc[index, "EMA"], self.queue.values[-1]["EMA"])
            else:
                self.data.at[index, "RoC"] = 0

            rvol_start = index - self.rvol_window
            rvol_data = self.data.loc[rvol_start:index, "volume"]
            avg_vol = rvol_data.mean()
            self.data.at[index, "rVol"] = self.calculate_rvol(self.data.loc[index, "volume"], avg_vol)
            if self.queue.values:
                self.data.at[index, "x_day_high"] = self.queue.max_value("high", 4)

            self.queue.enqueue(self.data.loc[index])

        
        
    def data_margin(self, dataframe):
        try: 
            dataframe = dataframe.loc["2024-01-14": "2025-03-29"]  
            return dataframe
        except:
            return None
    
    def bull_or_bear(self, _open, _close):
        try:
            if _open < _close:
                return True
            if _close < _open:
                return False
            
        except TypeError as e:
            print(e)
            return None

    def calculate_roc(self, current_value, prev_value):
        
        return ((current_value - prev_value) / prev_value) * 100

    def calculate_rvol(self, current_vol, avg_vol):
        return current_vol/avg_vol


