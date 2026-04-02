import math
from generator import Generator


class PoissonDistribution:
    def __init__(self, generator: Generator):
        self.g = generator

    # P(X = k) = e^(-l) * l^k / k
    def distribute(self, lam: float) -> int:
        if lam <= 0:
            return 0
        L = math.exp(-lam)
        p = 1.0
        k = 0

        while p > L:
            k += 1
            p *= self.g.random()

        return k - 1
