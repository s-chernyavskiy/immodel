import math

from generator import Generator
from config import config


class ExponentialDistribution:
    def __init__(self, generator: Generator):
        self.g = generator
        self.rates = config.rates_by_hour

    def distribute(self, rate: float) -> float:
        u = self.g.random()
        return -math.log(1 - u) / rate if rate > 0 else float('inf')

    def get_rate_by_hour(self, hour: int) -> float:
        rates = self.rates
        if rates['morning_start'] <= hour <= rates['morning_end']:
            return rates['morning_rate']
        elif rates['evening_start'] <= hour <= rates['evening_end']:
            return rates['evening_rate']
        elif hour >= rates['night_start'] or hour <= rates['night_end']:
            return rates['night_rate']
        else:
            return rates['day_rate']

    def get_next_event_time(self, current_time: float) -> float:
        hour = int(current_time) % 24
        rate = self.get_rate_by_hour(hour)
        if rate == 0:
            return float('inf')
        interval = self.distribute(rate)
        return current_time + interval
