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

def bdd_compose(bdd, subst):
    """
    Converts a BDD to an expression, performs composition using the provided substitution,
    and converts the result back to a BDD.
    """
    if bdd.is_zero():
        return bdd
    expr_form = bdd2expr(bdd)
    composed_expr = expr_form.compose(subst)
    return expr2bdd(composed_expr)

def bdd_smoothing(bdd, var_list):
    """
    Converts a BDD to an expression, performs smoothing
    on the specified variables, and converts back to a BDD.
    If smoothing returns None or yields an unsuitable expression, the original BDD is returned.
    """
    if bdd.is_zero():
        return bdd
    expr_form = bdd2expr(bdd)
    # If no variable from var_list appears in the support or the expression is constant, return bdd.
    if expr_form in [True, False] or not any(var in expr_form.support for var in var_list):
        return bdd
    smoothed_expr = expr_form.smoothing(var_list)
    if smoothed_expr is None:
        return bdd
    if isinstance(smoothed_expr, bool):
        return expr2bdd(expr(1)) if smoothed_expr else expr2bdd(expr(0))
    wrapped_expr = expr(smoothed_expr).simplify()
    return expr2bdd(wrapped_expr)

def compose_relation(rel, u_vars, v_vars, x_vars):
    """Compose a relation with itself to form a two-step relation."""
    rel_ux = bdd_compose(rel, {v_vars[i]: x_vars[i] for i in range(len(x_vars))})
    rel_xv = bdd_compose(rel, {u_vars[i]: x_vars[i] for i in range(len(x_vars))})
    return bdd_smoothing(rel_ux & rel_xv, list(x_vars))

def transitive_closure(rel, u_vars, v_vars, x_vars):
    """Compute the transitive closure of a relation using iterative composition."""
    T = rel
    while True:
        composed = compose_relation(T, u_vars, v_vars, x_vars)
        newT = T | composed
        if newT.equivalent(T):
            break
        T = newT
    return T
