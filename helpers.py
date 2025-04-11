from pyeda.inter import expr2bdd, And, Or, expr
from pyeda.boolalg.bdd import bdd2expr

def node_expr(node, varlist):
    """Returns a Boolean expression representing the node in bitwise format."""
    bits = format(node, '05b')
    return And(*[var if bit == '1' else ~var for bit, var in zip(bits, varlist)])

def evaluate_relation(bdd, i, j, u_vars, v_vars):
    """Evaluates the relation BDD for a given pair (i, j) using variable assignment."""
    assignment = {}
    binary_i = format(i, '05b')
    for idx, bit in enumerate(binary_i):
        assignment[u_vars[idx]] = (bit == '1')
    binary_j = format(j, '05b')
    for idx, bit in enumerate(binary_j):
        assignment[v_vars[idx]] = (bit == '1')
    expr_form = bdd2expr(bdd)
    result_expr = expr_form.restrict(assignment)
    return result_expr.is_one()

def evaluate_unary(bdd, node, varlist):
    """Evaluates a unary relation BDD for a given node using variable assignment."""
    assignment = {}
    binary_node = format(node, '05b')
    for idx, bit in enumerate(binary_node):
        assignment[varlist[idx]] = (bit == '1')
    expr_form = bdd2expr(bdd)
    result_expr = expr_form.restrict(assignment)
    return result_expr.is_one()
