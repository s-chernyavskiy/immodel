import numpy as np
from flat import Flat
from bernoulli import BernoulliDistribution
from exponential import ExponentialDistribution
from normal import NormalDistribution
from poisson import PoissonDistribution

class Building:
    def __init__(self, num_apartments: int, boiler_probability: float,
                 generator, time_step: int = 5):
        self.num_apartments = num_apartments
        self.time_step = time_step
        self.g = generator

        self.bernoulli = BernoulliDistribution(generator)
        self.exp_dist = ExponentialDistribution(generator)
        self.norm_dist = NormalDistribution(generator)
        self.poisson_dist = PoissonDistribution(generator)

        self.apartments = []
        for _ in range(num_apartments):
            has_boiler = self.bernoulli.distribute(boiler_probability)
            self.apartments.append(Flat(has_boiler))

        self.pipe_diameter = 0.05
        self.pipe_length = 50
        self.inlet_temp = 60.0

        self.temperatures = []
        self.pressures = []
        self.demands = []

    def calculate_pressure(self, total_demand: float) -> float:
        max_demand = self.num_apartments * 0.5
        pressure = max(0, 1 - total_demand / max_demand)
        return pressure

    def simulate_day(self, day: int):
        steps_per_day = 24 * 60 // self.time_step

        for step in range(steps_per_day):
            current_time = day * 24 + step * self.time_step / 60
            hour = int(current_time) % 24

            rate = self.exp_dist.get_rate_by_hour(hour)
            lam = rate * self.time_step / 60

            num_openings = self.poisson_dist.distribute(lam)

            total_demand = 0
            temps = []

            for _ in range(num_openings):
                apt = np.random.choice(self.apartments)

                volume = abs(self.norm_dist.distribute(10, 5))
                total_demand += volume

                outlet_temp = apt.use_water(volume, self.inlet_temp)
                temps.append(outlet_temp)

                apt.heat_loss()

            pressure = self.calculate_pressure(total_demand)

            self.temperatures.append(np.mean(temps) if temps else self.inlet_temp)
            self.pressures.append(pressure)
            self.demands.append(total_demand)