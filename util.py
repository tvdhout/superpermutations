import numpy as np
from math import factorial
from itertools import permutations as permute
import string

SYMBOLS = string.digits + string.ascii_uppercase


def is_palindrome(string):
    return string == string[::-1]


def get_permutations(n):
    """
    :param n:
    :return: list of all permutations of n unique items
    """
    uniques = list(SYMBOLS[:n])
    return list(map(lambda tup: ''.join(tup), permute(uniques)))


def is_permutation(perm, n):
    """
    :param perm:
    :param n:
    :return: perm is a valid permutation of 1..n
    """
    return len(perm) == n and all(list(map(lambda x: x in perm, list(SYMBOLS[:n]))))


def check_string(n, string, verbose=False):
    """
    :param n: the number of unique numbers in the permutations
    :param string: the super permutation to check for correctness
    :param verbose: show which permutations are missing in the string
    :return: Boolean: True if string is a correct super permutation of n
    """
    permutations = get_permutations(n)
    correct = True
    missing = []
    for permutation in permutations:
        if permutation not in string:
            if not verbose:
                return False
            missing.append(permutation)
            correct = False
    if verbose:
        print(missing)
    return correct


def merge(s1, s2):
    """
    Merge two strings with largest overlap
    :param s1: left string
    :param s2:  right string
    :return: concatenated string with largest overlap
    """
    smallest = min(len(s1), len(s2))
    for i in range(smallest):
        if s1[-smallest + i:] == s2[:smallest - i]:  # overlap between end of s1 and begin of s2
            return s1[:-smallest + i] + s2
    return s1 + s2


def fold_string(string):
    last_c = '*'
    folded = ''
    for c in string:
        if last_c == c:
            continue
        folded += c
        last_c = c
    return folded
