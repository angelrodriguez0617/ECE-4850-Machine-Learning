import pandas as pd
import numpy as np
from matplotlib import pyplot as plt 

df = pd.read_excel(r'project1/BTC-USD.xlsx')
print(df)
dates = np.array(df['Date'])
closes = np.array(df['Close'])
mean = sum(closes) / closes.size
alpha = closes - mean
variance = np.dot(alpha.T, alpha) / closes.size
print(f"The mean of the closing prices is: {mean}")
print(f"The mean of the closing prices is: {variance}")
plt.title("Bitcoin Data") 
plt.xlabel("Time (days)") 
plt.ylabel("Close Price (USD)") 
plt.plot(closes) 
plt.show()