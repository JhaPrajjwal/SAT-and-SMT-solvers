"""
Mastermind is a two player game.
There are n colors. Let k < n be a positive number.

1. Player one chooses a hidden sequence of k colors (colors may repeat)
2. The game proceeds iteratively as follows until player two has guessed
   the sequence correctly.
  2.1 Player two makes a guess of sequence of k colors
  2.2 Player one gives feedback to player two by giving
    * the number of correct in both position and color, and
    * the number of correct colors in the wrong positions.

Play online
http://www.webgamesonline.com/mastermind/index.php

"""

"""
Note:
    This code works for number of colors = 8 and holes = 4. But can be easily expanded for other values.
"""


from z3 import *
import argparse
import itertools
import time
import random

n=8
k=4

vs = [  [Bool ("e_{}_{}".format(i,j))  for j in range(n)] for i in range(k)]
color_name =  { 0:'R', 1:'G', 2:'B', 3:'Y', 4:'Br', 5:'O', 6:'Bl', 7:'W' }
base_cons = []

def sum_to_one( ls ):
    A = Or(ls)
    atmost_one_list = []
    for pair in itertools.combinations(ls,2):
        atmost_one_list.append(Or(Not(pair[0]),Not(pair[1])))
    return And(A, And(atmost_one_list))

"""
    The 5 functions below can be implemented more efficiently.
    I brute forced here.
"""

def correct_pos_0( ls ):
    A = True
    for i in range(k):
        A = And(A,Not(vs[i][ls[i]]))
    return A


def correct_pos_1( ls ):
    l = []
    a = vs[0][ls[0]]
    b = vs[1][ls[1]]
    c = vs[2][ls[2]]
    d = vs[3][ls[3]]

    l.append(And(a,Not(b),Not(c),Not(d)))
    l.append(And(b,Not(a),Not(c),Not(d)))
    l.append(And(c,Not(b),Not(a),Not(d)))
    l.append(And(d,Not(b),Not(c),Not(a)))
    l.append(And(a,Not(b)))
    l.append(And(b,Not(a)))
    return Or(l)

def correct_pos_2( ls ):
    l = []
    a = vs[0][ls[0]]
    b = vs[1][ls[1]]
    c = vs[2][ls[2]]
    d = vs[3][ls[3]]

    l.append(And(a,b,Not(c),(Not(d))))
    l.append(And(a,c,Not(b),(Not(d))))
    l.append(And(c,b,Not(a),(Not(d))))
    l.append(And(a,d,Not(b),(Not(c))))
    l.append(And(d,b,Not(c),(Not(a))))
    l.append(And(c,d,Not(b),(Not(a))))
    return Or(l)


def correct_pos_3( ls ):
    l = []
    a = vs[0][ls[0]]
    b = vs[1][ls[1]]
    c = vs[2][ls[2]]
    d = vs[3][ls[3]]

    l.append(And(a,b,c,(Not(d))))
    l.append(And(a,b,d,(Not(c))))
    l.append(And(a,d,c,(Not(b))))
    l.append(And(d,b,c,(Not(a))))
    return Or(l)


def correct_pos_4(ls):
    A = True
    for i in range(k):
        A = And(A,vs[i][ls[i]])
    return A


def white_cond( ls , whites):
    l = []
    for i in range(len(ls)):
        B = False
        for j in range(k):
            B = Or(B, vs[j][ls[i]])
        l.append(B)
    
    cond = PbGe([(l[i],1) for i in range(len(l))], whites)
    return cond


def add_a_guess_solution( guess, reds, whites ):

    if reds == 0:
        cons = correct_pos_0(guess)
    elif reds == 1:
        cons = correct_pos_1(guess)
    elif reds == 2:
        cons = correct_pos_2(guess)
    elif reds == 3:
        cons = correct_pos_3(guess)
    elif reds == 4:
        cons = correct_pos_4(guess)

    
    guess_cons = white_cond(guess,whites)

    s.add( And(guess_cons,cons) )


if n > 8:
    for i in range(8,n):
        color_name[i] = 'C'+str(i)

def print_move( move ):
    for i in range(k):
        c = color_name[move[i]]
        print(c, end=' '),
    print("\n")

        
def get_a_solution():
    sol = [0]*k
    if s.check() == sat:
        m = s.model()
        print("model: ",m)
        for i in range(k):
            for j in range(n):
                val = m[vs[i][j]]
                # val2 = m[pos[j][i]]
                # print(val,val2,vs[i][j],pos[j][i])
                if is_true( val ) :
                    sol[i] = j

        print("yopj",sol)
        return sol
    else:
        print("some thing bad happened! no more moves!\n")
        raise Exception('Failed!')


def get_response():
    red = int(input("Enter red count: "))
    white = int(input("Enter white count: "))
    if white+red > k:
        raise Exception("bad input!")
    return red,white
    

def play_game():
    guess_list = []
    response_list = []
    red = 0
    while red < k:
        if len(guess_list) == 0:
            # start with random guess
            move = [0]*k
        else:
            move = get_a_solution()
        guess_list.append(move)
        print("found a move:")
        print_move( move )
        red, white = get_response()
        add_a_guess_solution( move, red, white )
    print("Game solved!")
    


for i in range(k):
    base_cons.append(sum_to_one(vs[i]))

s = Solver()
s.add( And(base_cons) )

play_game()
