import pandas as pd
import matplotlib
import matplotlib.pyplot as plt

# Get dataframe object from json data in data dir
def get_dataframe(data):
    data = pd.read_json(data)
    data = pd.DataFrame(data)
    data["date"] = pd.to_datetime(data["date"])
    data.set_index(["date"], inplace=True)

    return data

results = get_dataframe(r"data/ACHR.json")








