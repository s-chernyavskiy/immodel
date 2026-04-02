import math
from generator import Generator

class NormalDistribution:
    def __init__(self, generator: Generator):
        self.g = generator
        self.has_spare = False
        self.spare = 0.0

    def distribute(self, mean: float, std: float) -> float:
        if self.has_spare:
            self.has_spare = False
            return mean + std * self.spare

        u1 = self.g.random()
        u2 = self.g.random()

        r = math.sqrt(-2.0 * math.log(u1))
        theta = 2.0 * math.pi * u2

        z1 = r * math.cos(theta)
        z2 = r * math.sin(theta)

        self.spare = z2
        self.has_spare = True

        return mean + std * z1