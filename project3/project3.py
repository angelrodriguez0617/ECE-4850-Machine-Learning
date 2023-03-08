import numpy as np
import matplotlib.pyplot as plt
import random
import time
import copy
import os

my_local_file = os.path.join(os.path.dirname(__file__), 'The Project Gutenberg eBook of Webs.txt')
print(f"{my_local_file}")
fo = open(my_local_file, 'r')

# Coonvert all lower
for x in fo.read():
    y = x.lower()
    fo1 = open('test_file.txt', 'a')
    fo1.write(y)