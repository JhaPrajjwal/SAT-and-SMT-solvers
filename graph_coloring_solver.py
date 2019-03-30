from z3 import *
import time
import matplotlib.pyplot as plt

N = 500
D = 3


def color(edges,k):
    # print(edges,k)
    vs = [  [Bool("x_{}_{}".format(i,j))  for j in range(D)] for i in range(N)]

    # each vertex has atleast one color
    A = True
    for i in range(N):
        A = And(A, Or(vs[i]) ) 

    # col is different for adjacent vertices
    B = True
    for u,v in edges:
        for i in range(D):
            B = And(B, Or(Not(vs[u-1][i] ),Not( vs[v-1][i])))

    # print(A,B)
    s = Solver()
    s.add(And(A,B))
    start = time.time()
    res = s.check()
    end = time.time()
    if res == sat:
        print("sat: edges = ", k, end-start)
    else:
        print("unsat: edges = ", k, end-start)
    
    return end-start
    


f = open('edges.txt','r') 
edges = []
for x in f:
    u, v = (x.split(','))
    u, v = int(u), int(v)
    edges.append((u,v))


time_list = []
x = []
for k in range(10,5001,10):
    
    val = color(edges[:k],k)
    time_list.append(val)
    x.append(k)

print(time_list)
plt.plot(x,time_list)
plt.show()
    
