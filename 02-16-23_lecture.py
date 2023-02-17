import math
import numpy as np

x = np.array([-2, -1, 0, 1.5, 2.6, 3, 3.2, 3.5, 4, 10])

mu_0 = 2
var_0 = 1
mu_1 = 3
var_1 = 2

def calculate_gauss_pdf(input, mu, var):
    likelyhood = (1/math.sqrt(2*math.pi*var))*math.exp((-1/(2*var))*(input-mu)**2)
    return likelyhood

def compare_likelyhood(likelyhood0, likelyhood1):
    print(f"Likelyhood of 0: {likelyhood0}, likelyhood of 1: {likelyhood1}")
    return likelyhood0 < likelyhood1

for i in range(x.size):
    print(f'x value: {x[i]}')
    print(compare_likelyhood(calculate_gauss_pdf(x[i], mu_0, var_0), calculate_gauss_pdf(x[i], mu_1, var_1)))
    print()