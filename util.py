from itertools import permutations as permute
import string

SYMBOLS = string.digits[1:] + string.ascii_uppercase


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


def distance_between(p1, p2):
    """
    compute distance between permutation 1 and 2, in the sense of how many characters to append to permutation 1
    to have the string contain permutation 2
    example: '123' -> '321': we can add '21' to the first permutation to include the second, therefore distance = 2
    :param p1: permutation 1
    :param p2: permutation 2
    :return: distance between 1 and 2
    """
    assert len(p1) == len(p2)
    for i in range(len(p1)):
        if p1[i:] == p2[:len(p1)-i]:
            return i
    return len(p1)


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
            return s1[:-smallest + i] + s2  # take beginning part of s1 (without overlap) and append s2
    return s1 + s2


def path_to_string(path):
    """
    Create a Superpermutation string from a graph path
    :param path: list of permutations in order of visiting
    :return: Superpermutation string by collapsing the path with the most overlap
    """
    string = path[0]
    for perm in path[1:]:
        string = merge(string, perm)
    return string


def fold_string(string):
    """
    Not sure if this will be used, folds consecutive, equal characters in a string together
    e.g. "aabaaaaaacccca" -> "abaca"
    :param string:
    :return:
    """
    last_c = '*'
    folded = ''
    for c in string:
        if last_c == c:
            continue
        folded += c
        last_c = c
    return folded
