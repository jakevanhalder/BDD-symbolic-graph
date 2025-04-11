"""
projectBDD.py: Implementation of a symbolic graph project using pyeda.
This program verifies StatementA:
    For each node u in [prime], there exists a node v in [even] such that u can reach v 
    in a positive even number of steps.
"""
from pyeda.inter import exprvars, expr2bdd, And, Or, expr
from helpers import node_expr, evaluate_relation

NUM_BITS = 5

u = exprvars('u', NUM_BITS)
v = exprvars('v', NUM_BITS)

# -------------------------------
# 1. Build the edge relation R.
# -------------------------------
edge_expr_terms = []
for i in range(32):
    j1 = (i + 3) % 32
    j2 = (i + 8) % 32
    term = And(node_expr(i, u), Or(node_expr(j1, v), node_expr(j2, v)))
    edge_expr_terms.append(term)

R_expr = Or(*edge_expr_terms)
RR = expr2bdd(R_expr)

# Test cases for R.
print("RR(27, 3) =", evaluate_relation(RR, 27, 3, u, v))
print("RR(16, 20) =", evaluate_relation(RR, 16, 20, u, v))
