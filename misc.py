import math

def comb(N, k):
    if N < k:
      raise RuntimeError('Calc comb fiailed.')
      
    return int(math.factorial(N) / (math.factorial(N-k) * math.factorial(k)))