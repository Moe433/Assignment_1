import pandas as pd

data_path = "/Users/mohammedqudaih/Assignment_1/archive/UNSW_NB15_engineered_minimal.csv"
df = pd.read_csv(data_path)

print(df.columns.tolist())
