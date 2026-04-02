import math

from generator import Generator


class ExponentialDistribution:
    def __init__(self, generator: Generator):
        self.g = generator

    def distribute(self, rate: float) -> float:
        u = self.g.random()
        return -math.log(1 - u) / rate if rate > 0 else float('inf')

    def get_rate_by_hour(self, hour: int) -> float:
        if 6 <= hour <= 9:
            return 4.0
        elif 18 <= hour <= 22:
            return 3.0
        elif 23 <= hour or hour <= 5:
            return 0.1
        else:
            return 1.0

    def get_next_event_time(self, current_time: float) -> float:
        hour = int(current_time) % 24
        rate = self.get_rate_by_hour(hour)
        if rate == 0:
            return float('inf')
        interval = self.distribute(rate)
        return current_time + interval
