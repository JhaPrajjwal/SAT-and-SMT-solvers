from z3 import *

p = Bool("P")
q = Bool("Q")
r = Bool("R")
phi1 = And(p,Not(Not(q)))
phi2 = And(p, Not(And( Not(q),p )) )
phi3 = Not(Not(p))
phi4 = And( Or(p,Not(r)), Or(q,r) )

litreals = {}

def decompose(phi,counter):

    if phi.decl().name() == "not":
        decompose(phi.arg(0), counter+1)

    elif phi.decl().name() == "and" or phi.decl().name() == "or":
        print(phi.arg(0),phi.arg(1))
        decompose(phi.arg(0), counter)
        decompose(phi.arg(1), counter)

    else:
        if phi.decl().name() not in litreals.keys():
            litreals[phi.decl().name()] = True

        if litreals[phi.decl().name()]:
            if counter % 2:
                litreals[phi.decl().name()] = False



decompose(phi4,0)
print(litreals)
