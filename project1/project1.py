import pandas as pd
import numpy as np
import statistics 
from matplotlib import pyplot as plt 

df = pd.read_excel(r'project1/BTC-USD.xlsx')
print(df)
dates = np.array(df['Date'])
closes = np.array(df['Close'])
mean = statistics.mean(closes)
stdev = statistics.stdev(closes)
variance = statistics.variance(closes)
print(f"The mean of the closing prices is: {mean}")
print(f"The mean of the closing prices is: {stdev}")
print(f"The mean of the closing prices is: {variance}")
plt.title("Matplotlib demo") 
plt.xlabel("Time (days)") 
plt.ylabel("Close Price (USD)") 
plt.plot(closes) 
plt.show()