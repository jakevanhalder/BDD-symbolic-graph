"""
projectBDD.py: Implementation of a symbolic graph project using pyeda.
This program verifies StatementA:
    For each node u in [prime], there exists a node v in [even] such that u can reach v 
    in a positive even number of steps.
"""
from pyeda.inter import exprvars, expr2bdd, And, Or, expr
from helpers import node_expr, evaluate_relation, evaluate_unary, bdd_compose, bdd_smoothing, transitive_closure

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

# -------------------------------
# 2. Build BDDs for even and prime sets.
# -------------------------------
even_nodes = [node_expr(i, v) for i in range(32) if i % 2 == 0]
EVEN_expr = Or(*even_nodes)
EVEN = expr2bdd(EVEN_expr)

prime_set = {3, 5, 7, 11, 13, 17, 19, 23, 29, 31}
prime_nodes = [node_expr(p, u) for p in prime_set]
PRIME_expr = Or(*prime_nodes)
PRIME = expr2bdd(PRIME_expr)

print("EVEN(14) =", evaluate_unary(EVEN, 14, v))
print("EVEN(13) =", evaluate_unary(EVEN, 13, v))
print("PRIME(7) =", evaluate_unary(PRIME, 7, u))
print("PRIME(2) =", evaluate_unary(PRIME, 2, u))

# -------------------------------
# 3. Compute 2-step relation RR2.
# -------------------------------
x = exprvars('x', NUM_BITS)
R_ux = bdd_compose(RR, {v[i]: x[i] for i in range(NUM_BITS)})
R_xv = bdd_compose(RR, {u[i]: x[i] for i in range(NUM_BITS)})
RR2_temp = R_ux & R_xv
RR2 = bdd_smoothing(RR2_temp, list(x))

print("RR2(27, 6) =", evaluate_relation(RR2, 27, 6, u, v))
print("RR2(27, 9) =", evaluate_relation(RR2, 27, 9, u, v))

# -------------------------------
# 4. Compute transitive closure RR2⋆ for even-length paths.
# -------------------------------

y = exprvars('y', NUM_BITS)
RR2star = transitive_closure(RR2, u, v, y)

# -------------------------------
# 5. Verify StatementA.
# StatementA: For every prime node u there exists an even node v such that u can reach v
# in a positive even number of steps.
# -------------------------------
RR2star_and_EVEN = RR2star & EVEN
reachable_even = bdd_smoothing(RR2star_and_EVEN, list(v))
statement_expr = (~PRIME) | reachable_even
statement_value = bdd_smoothing(statement_expr, list(u))
print("StatementA holds:", statement_value)
