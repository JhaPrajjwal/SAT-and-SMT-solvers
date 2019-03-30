from z3 import * 
import itertools
import time 
import matplotlib.pyplot as plt

def solve(n):
    vs = [  [Int("x_{}_{}".format(i,j))  for j in range(n)] for i in range(n)]
    flatten = list(itertools.chain.from_iterable(vs))

    # create constraints
    #   -- all entries are between 1-9
    #   -- all entries are distinct
    #   There is a sum value t
    #   -- sum of rows is t
    #   -- sum of columns is t
    #   -- sum of diagonals is t

    distinct_cons = Distinct(flatten) 

    range_cons = True

    for i in range(n*n):
        range_cons = And( And(flatten[i]>0,flatten[i]< (n*n+1) ), range_cons)


    l = []
    diag1 = 0
    diag2 = 0
    for i in range(n):
        sum1 = 0 
        sum2 = 0
        for j in range(n):
            sum1 += vs[i][j]
            sum2 += vs[j][i]

        l.append(sum1)
        l.append(sum2)
        diag1 += vs[i][i]
        diag2 += vs[i][n-i-1]
    
    l.append(diag1)
    l.append(diag2)

    sum_cons = True
    for i in range(len(l)):
        sum_cons = And(sum_cons, l[i]==l[0])

    s = Solver()
    phi = And(And(range_cons, distinct_cons), sum_cons)
    s.add(phi)

    r = s.check()
    if r == sat:
        print("sat: ",n)
        m = s.model()
        for i in range(n):
            print( "|-----|-----|-----|" )
            for j in range(n):
                print("|  ", end ="")
                val = m[vs[i][j]]
                print( val, end ="  ")
            print("|")
        print( "|-----|-----|-----|" )  
    else:
        print("unsat: ",n)


time_list = []
for i in range(1,6):
    start = time.time()
    solve(i)
    end = time.time()
    time_list.append(end-start)

plt.plot(time_list,[1,2,3,4,5])
plt.show()

    
