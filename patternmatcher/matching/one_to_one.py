# -*- coding: utf-8 -*-
from typing import Iterator, Tuple

from ..expressions import Expression, Substitution
from .common import match as _match


def match(expression: Expression, pattern: Expression) -> Iterator[Substitution]:
    r"""Tries to match the given `pattern` to the given `expression`.

    Yields each match in form of a substitution that when applied to `pattern` results in the original
    `expression`.

    Parameters:
        expression:
            An expression to match.
        pattern:
            The pattern to match.

    Yields:
        All possible substitutions as dictionaries where each key is the name of the variable
        and the corresponding value is the variables substitution. Applying the substitution to the pattern
        results in the original expression (except for :class:`Wildcard`\s)
    """
    return _match([expression], pattern, {})


def match_anywhere(expression: Expression, pattern: Expression) -> Iterator[Tuple[Substitution, Tuple[int, ...]]]:
    """Tries to match the given `pattern` to the any subexpression of the given `expression`.

    Yields each match in form of a substitution and a position tuple.
    The substitution is a dictionary, where the key is the name of a variable and the value either an expression
    or a list of expressins (iff the variable is a sequence variable).
    When applied to `pattern`, the substitution results in the original matched subexpression.
    The position is a tuple of indices, e.g. the empty tuple refers to the `expression` itself,
    `(0, )` refers to the first child (operand) of the expression, `(0, 0)` to the first child of
    the first child etc.

    Parameters:
        expression:
            An expression to match.
        pattern:
            The pattern to match.

    Yields:
        All possible substitution and position pairs.
    """
    predicate = None
    if pattern.head is not None:
        predicate = lambda x: x.head == pattern.head
    for child, pos in expression.preorder_iter(predicate):
        for subst in _match([child], pattern, {}):
            yield subst, pos