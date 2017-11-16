from scipy.integrate import odeint
from thread import start_new_thread as new
import numpy as np
from math import exp, sin, cos
from time import sleep, time, gmtime
import sys, pickle, socket

def beta(x3):
    return abs(1+((N**2)*(sin(x3)**2)/(N01**2)))**(-1)

def func(x, t): #tu sa pocita diferencialna cast
    
    X1,X2,X3,X4=x[0],x[1],x[2],x[3]
    beta3=beta(X3)
    s3=sin(X3)
    c3=cos(X3)
    
    fa=(.01313482817*X1 +10.10509022*X2 + 46.76016035*X3 + 4.218843951*X4)*kP
    fa+=X1*(-kI)*kP
    
    x1=X2
    x2=beta3*(a23*s3*c3+a22*X2+a24*c3*X4+a25*s3*X4*X4+ b2*fa)
    x3=X4
    x4=beta3*(a43*s3+a42*c3*X2+a44*X4+a45*c3*s3*X4*X4+ b4*c3*fa)
    
    return [x1,x2,x3,x4,fa] 

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
for i in range(20000,30000):
    try:
        s.bind(("", i)) #listen to all on port from input 
        print "waiting for connection on port %d"%i
    except: pass
s.listen(1) #wait for one connection
conn, addr = s.accept() #connection accepted
print 'Connected by', addr
while 1:
    data = conn.recv(1024)

    if data[0:4]=="exec":
        exec(data[4:])
        conn.sendall("ack")
        print ">> Variables loaded"
    elif data[0:4]=="exit":
        conn.close()
        exit(0)
    elif data[0:4]=="simu":
	timestamp=time()
	medzicas=timestamp
	gmt=gmtime(time())
	hodina, minuta, sekunda=gmt.tm_hour, gmt.tm_min, gmt.tm_sec
        print ">> Start of simulation at time %d:%d:%d"%(hodina, minuta, sekunda)
        conn.sendall("gmt")
        data=conn.recv(256)
        length=int(data)
        print ">> Length of data field:",length
        print ">> ...acknowledged"
        conn.sendall("ack")
        data=conn.recv(length)
        exec(data)
        print ">> Time frame loaded in %.1fms."%(time()*1000-medzicas*1000)
        medzicas=time()
        conn.sendall("gmx")
        data=conn.recv(1024)
        exec(data)
        print ">> default values: ", x0
        print">> Simulating..."
        #Numericke prepocitanie diferencialnych rovnic
        
        data=odeint(func, x0, t)
        
        print ">> Simulated succesfully in %.1fms."%(time()*1000-medzicas*1000)
        medzicas=time()
        print ">> Length of simulated data to be transmitted: %dkB"%(int(len(data))*5/1024)
        conn.sendall("data%d"%len(data))
        
        f = conn.makefile('wb', len(data)+1024 )
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)
        f.close()
	print ">> Simulated and transmitted in %.1fms.\n"%((time()-timestamp)*1000)
        
    else:
        exit()
        #print data



