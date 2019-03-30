#!/usr/bin/python

from z3 import *
import argparse
import itertools
import time

problem1 = [
 [ 9, 0, 0,   0, 1, 0,   5, 0, 0],
 [ 7, 0, 0,   8, 0, 3,   0, 0, 2],
 [ 0, 0, 0,   0, 0, 0,   3, 0, 8],

 [ 0, 7, 8,   0, 2, 5,   6, 0, 0],
 [ 0, 0, 0,   0, 0, 0,   0, 0, 0],
 [ 0, 0, 2,   3, 4, 0,   1, 8, 0],

 [ 8, 0, 9,   0, 0, 0,   0, 0, 0],
 [ 5, 0, 0,   4, 0, 1,   0, 0, 9],
 [ 0, 0, 1,   0, 5, 0,   0, 0, 4]
]

problem2 = [
[ 0, 8, 0,   0, 0, 3,   0, 0, 0],
[ 5, 0, 3,   0, 4, 0,   2, 0, 0],
[ 7, 0, 4,   0, 8, 0,   0, 0, 3],

[ 0, 7, 0,   0, 0, 0,   5, 0, 0],
[ 0, 3, 0,   8, 0, 5,   0, 6, 0],
[ 0, 0, 1,   0, 0, 0,   0, 9, 0],

[ 9, 0, 0,   0, 3, 0,   7, 0, 6],
[ 0, 0, 7,   0, 2, 0,   3, 0, 1],
[ 0, 0, 0,   6, 0, 0,   0, 2, 0]
]

problem = problem2
# problem = problem2

# define the problem variables
# Hint: three dimentional array
V = [ [ [Bool("x_{}_{}_{}".format(i,j,k))  for k in range(9)] for j in range(9)] for i in range(9)]
# print(V)

def sum_to_one( ls ):
    A = Or(ls)
    atmost_one_list = []
    for pair in itertools.combinations(ls,2):
        atmost_one_list.append(Or(Not(pair[0]),Not(pair[1])))
    return And(A, And(atmost_one_list))

# Accumulate constraints in the following list 
Fs = []


# Encode already filled positions
A = True
for i in range(9):
    for j in range(9):
        if problem[i][j]:
            A = And(A, V[i][j][problem[i][j]-1])

Fs.append(A)

# Encode for i,j  \sum_k x_i_j_k = 1
B = True
for i in range(9):
    for j in range(9):
        B = And(B, sum_to_one(V[i][j]))

Fs.append(B)

# Encode for j,k  \sum_i x_i_j_k = 1
C = True

for j in range(9):
    for k in range(9):
        l = []
        for i in range(9):
            l.append(V[i][j][k])
        C = And(C, sum_to_one(l))

Fs.append(C)


# Encode for i,k  \sum_j x_i_j_k = 1
D = True

for i in range(9):
    for k in range(9):
        l = []
        for j in range(9):
            l.append(V[i][j][k])
        D = And(D, sum_to_one(l))

Fs.append(D)

# Encode for i,j,k  \sum_r_s x_3i+r_3j+s_k = 1
E = True
for p in [0,3,6]:
    for pp in [0,3,6]:
        for k in range(9):
            l = []
            for i in range(3):
                for j in range(3):
                    l.append(V[i+p][j+pp][k])
            E = And(E,sum_to_one(l))

Fs.append(E)

s = Solver()
s.add( And( Fs ) )

if s.check() == sat:
    m = s.model()
    for i in range(9):
        if i % 3 == 0 :
            print( "|------|------|------|")
        for j in range(9):
            if j % 3 == 0 :
                print ("|",end="")
            for k in range(9):
                # FILL THE GAP
                # val model for the variables
                val = m[V[i][j][k]]
                if is_true( val ):
                    print ("{}".format(k+1),end=",")
            # if problem[i][j]:
            #     print("{}".format(problem[i][j]),end=",")
        print ("|,")
    print ("|------|------|------|")
else:
    print ("sudoku is unsat")

