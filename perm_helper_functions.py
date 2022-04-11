from perm import *


def gcd(a, b):
    a, b = abs(a), abs(b)
    while b != 0:
        a, b = b, a % b
    return a


def composition(p, q):
    result = []
    for i in range(len(p)):
        result.append(q[p[i]])
    return result


def inverse(p):
    result = []
    mx = 0
    cycleP = cycles(p)
    for cycle in reversed(cycleP):
        mx = max(mx, max(cycle))
        result.append(list(cycle[::-1]))
    return permutation_from_cycles(mx + 1, result)


def naivePower(p, i):
    if i == 0:
        return list(range(max(p) + 1))
    if i < 0:
        p = inverse(p)
        i = abs(i)
    q = p
    for i in range(0, i - 1):
        q = composition(q, p)
    return q


def period(p):
    cycleP = cycles(p)
    cycleLens = [len(cycleP[i]) for i in range(len(cycleP))]

    lcm = cycleLens[0]
    for i in cycleLens[1:]:
        lcm = int(lcm*i/gcd(lcm, i))
    return lcm


def power(p, i):
    if i == 0:
        return list(range(max(p) + 1))
    if i < 0:
        p = inverse(p)
        i = abs(i)

    q = p
    i = i % (period(q))
    for j in range(0, i - 1):
        q = composition(q, p)
    return q


def naivePeriod(p):
    i = 1
    while not is_trivial(power(p, i)):
        i += 1
    return i
