from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from math import exp

a,b,c,d=0.3,0.02,0.4,0.03
plt.ion()

def func(x,t):

	V=x[0]
	Z=x[1]

	v=(-1)*V*(a-b*Z)
	z=Z*(c-d*V)

	return [v, z] 

x0,x1=float(input("Poc. vlkov: ")),float(input("Poc. zajacov: "))
x0=[x0,x1]

t=[i/100.0 for i in range(0,int(input("Cas sim.: "))*100)]

sol=odeint(func, x0, t)

plt.figure()
plt.plot(t, sol[:,0], label='Vlky')
plt.plot(t, sol[:,1], label='Zajace')
plt.xlabel('Time')
plt.ylabel('x0,x1')
plt.title('Vyvoj mnozstva vlkov a zajacov')
plt.legend(loc=0)

plt.show()
#input()
