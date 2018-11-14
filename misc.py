import math

def comb(N, k):
    return math.factorial(N) / (math.factorial(N-k) * math.factorial(k))