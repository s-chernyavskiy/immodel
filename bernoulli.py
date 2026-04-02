from generator import Generator

class BernoulliDistribution:
    def __init__(this, generator: Generator):
        this.g = generator

    # p(1) = p, p(0) = 1 - p 
    def distribute(this, p: float) -> int:
        return 1 if this.g.random() < p else 0