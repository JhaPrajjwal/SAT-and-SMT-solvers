import sys
import random

n = int(sys.argv[1])
m = int(sys.argv[2])

graph = set([])


while len(graph) != m:

    a = random.randint(1,n)
    b = random.randint(1,n)
    
    if a==b:
        if a == n:
            graph.add((a,b-1))
        else:
            graph.add((a,b+1))
    else:
        graph.add((a,b))

with open('edges.txt','w') as f:
    for i in range(m):
        a, b = graph.pop()
        f.write(str(a)+","+str(b)+"\n")


