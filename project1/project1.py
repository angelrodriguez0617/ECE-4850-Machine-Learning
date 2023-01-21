import pandas as pd
import numpy as np
import statistics 

df = pd.read_excel(r'project1/BTC-USD.xlsx')
print(df)
dates = np.array(df['Date'])
closes = np.array(df['Close'])
mean = statistics.mean(closes)
stdev = statistics.stdev(closes)
print(f"The mean of the closing prices is {mean}")
print(f"The mean of the closing prices is {stdev}")