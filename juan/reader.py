import numpy as np
import matplotlib.pyplot as plt
f = open("data.txt", "r")
a = 0
while a == 0:
    f.readline
    x = np.linspace(10., 100., 50)
    y = x**10 + x**5 + x**2 + 100
    plt.plot(x, y)
    plt.show()