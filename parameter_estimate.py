import sys
import numpy as np
from scipy.optimize import curve_fit

x = [1,5,10,15,20,25]
y = []

def func(d, n, A):
	return -10 * n * np.log10(d) + A


for i in range(len(x)):
	y.append(float(sys.argv[i+1]))

popt, pcov = curve_fit(func, x, y)

print(popt)