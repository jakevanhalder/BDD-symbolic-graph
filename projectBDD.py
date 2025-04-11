"""
projectBDD.py: Implementation of a symbolic graph project using pyeda.
This program verifies StatementA:
    For each node u in [prime], there exists a node v in [even] such that u can reach v 
    in a positive even number of steps.
"""
from pyeda.inter import exprvars, expr2bdd, And, Or, expr

NUM_BITS = 5

u = exprvars('u', NUM_BITS)
v = exprvars('v', NUM_BITS)
