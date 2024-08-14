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

results = get_dataframe(r"data/SOUN.json")

results["avg50"] = results["close"].rolling(50).mean()
results["avg200"] = results["close"].rolling(200).mean()

results["close1"] = results["close"].shift(-1)

condition = results["avg50"] > results["avg200"]

results["shares"] = [1 if condition.loc[ei] else 0 for ei in results.index]

profit_condition = results["shares"] >= 0

results["profit"] = [results.loc[ei, "close1"] - results.loc[ei, "close"] if results.loc[ei, "shares"] >= 1 else 0 for ei in results.index]

results["wealth"] = results["profit"].cumsum()

plt.title(f"Total money you have made is {results.loc[results.index[-2], 'wealth']}")
plt.figure(figsize=(10, 8))
results["avg50"].plot()
results["avg200"].plot()

plt.show()