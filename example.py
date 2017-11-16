import numpy as np
from math import sin, cos
import matplotlib.pyplot as plt
import matplotlib.animation as animation

ls=0.451
def update_line(n, data, line, ls):
    x=float(data[n].split(" ")[0])
    fi=float(data[n].split(" ")[2])
    line.set_data([x,x+ls*sin(fi)],[0,ls*cos(fi)])
    return line,

fig1 = plt.figure()
subor=file("simulation.dat","r")
data=subor.read().split("\n")
cas=data[0]
data=data[1:]
subor.close()

l, = plt.plot([], [], '-o')

plt.xlim(-1, 1)
plt.ylim(-1, 1)
plt.xlabel('x1')
plt.title('Real time animation')

line_ani = animation.FuncAnimation(fig1, update_line, np.arange(0,len(data)), fargs=(data, l, ls),
    interval=int(cas), blit=True)
#line_ani.save('lines.avi')

plt.show()