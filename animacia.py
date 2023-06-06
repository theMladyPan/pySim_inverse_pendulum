import numpy as np
from math import sin, cos
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class Animacia:
    def __init__(self):
        self.ls=0.451
    def update_line(self,n, data, line, ls):
        x=float(data[n].split(" ")[0])
        fi=float(data[n].split(" ")[2])
        line.set_data([x,x-ls*sin(fi)],[0,ls*cos(fi)])
        return line,

    def rozpohybuj(self):
        fig1 = plt.figure()
        subor=file("simulation.dat","r")
        data=subor.read().split("\n")
        cas=data[0]
        data=data[1:]
        subor.close()
        a = [abs(float(i.split(" ")[0])) for i in data]
        l, = plt.plot([], [], '-o')
        a=max(a)
        a=max([a,self.ls])
        plt.xlim(-a-self.ls, a+self.ls)
        plt.ylim(-a, a+self.ls)
        plt.xlabel('x1')
        plt.title('Real time animation @%dfps'%(1000/int(cas)))

        line_ani = animation.FuncAnimation(fig1, self.update_line, np.arange(0,len(data)), fargs=(data, l, self.ls),
            interval=int(cas), blit=True)

        plt.show()

def animuj(event=None):
    anim1=Animacia()
    anim1.rozpohybuj()   
    
if __name__=="__main__":
    animuj()