import numpy as np
from flat import Flat
from bernoulli import BernoulliDistribution
from exponential import ExponentialDistribution
from normal import NormalDistribution
from poisson import PoissonDistribution
from config import config


class Building:
    def __init__(self, boiler_probability: float, generator, time_step: int = None):
        if time_step is None:
            time_step = config.time_step_minutes

        self.num_apartments = config.num_apartments
        self.time_step = time_step
        self.g = generator

        self.bernoulli = BernoulliDistribution(generator)
        self.exp_dist = ExponentialDistribution(generator)
        self.norm_dist = NormalDistribution(generator)
        self.poisson_dist = PoissonDistribution(generator)

        self.apartments = []
        for _ in range(self.num_apartments):
            has_boiler = self.bernoulli.distribute(boiler_probability)
            self.apartments.append(Flat(has_boiler))

        self.pipe_diameter = 0.05
        self.pipe_length = 50
        self.inlet_temp = config.inlet_temp
        self.cold_water_temp = config.get('temperature.cold_water_temp', config.ambient_temp)
        self.system_thermal_mass_liters = config.get('temperature.system_thermal_mass_liters', 4000.0)
        self.heater_power_watts = config.get('temperature.heater_power_watts', 180000.0)
        self.heat_loss_coefficient_w_per_k = config.get('temperature.heat_loss_coefficient_w_per_k', 500.0)
        self.water_specific_heat = config.get('temperature.water_specific_heat_j_per_kg_k', 4186.0)
        self.water_density = config.get('temperature.water_density_kg_per_m3', 1000.0)
        self.heater_setpoint_temp = config.get('temperature.heater_setpoint_temp', self.inlet_temp)
        self.heater_deadband_c = config.get('temperature.heater_deadband_c', 1.0)
        self.heater_enabled = False

        self.temperatures = []
        self.pressures = []
        self.demands = []

    def calculate_pressure(self, total_demand: float) -> float:
        max_demand = self.num_apartments * config.max_demand_per_apartment
        pressure = max(0, 1 - total_demand / max_demand)
        return pressure

    def update_inlet_temperature(self, current_temp: float, total_demand_liters: float) -> float:
        dt_seconds = self.time_step * 60.0
        system_mass_kg = self.system_thermal_mass_liters * self.water_density / 1000.0

        if system_mass_kg <= 0:
            return current_temp

        consumed_mass_kg = max(0.0, total_demand_liters) * self.water_density / 1000.0
        consumed_mass_kg = min(consumed_mass_kg, system_mass_kg)

        # Energy removed by demand as hot water is replaced by colder mains water.
        q_demand_j = consumed_mass_kg * self.water_specific_heat * (current_temp - self.cold_water_temp)
        lower_threshold = self.heater_setpoint_temp - self.heater_deadband_c
        if current_temp <= lower_threshold:
            self.heater_enabled = True
        elif current_temp >= self.heater_setpoint_temp:
            self.heater_enabled = False

        q_heater_j = self.heater_power_watts * dt_seconds if self.heater_enabled else 0.0
        q_loss_j = self.heat_loss_coefficient_w_per_k * (current_temp - config.ambient_temp) * dt_seconds

        delta_temp = (q_heater_j - q_demand_j - q_loss_j) / (system_mass_kg * self.water_specific_heat)
        next_temp = current_temp + delta_temp
        return max(self.cold_water_temp, min(self.heater_setpoint_temp, next_temp))

    def simulate_day(self, day: int):
        steps_per_day = 24 * 60 // self.time_step
        current_inlet_temp = self.inlet_temp

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

                volume = abs(self.norm_dist.distribute(config.normal_mean, config.normal_std))
                total_demand += volume
                outlet_temp = apt.use_water(volume, current_inlet_temp)
                temps.append(outlet_temp)

                apt.heat_loss()

            current_inlet_temp = self.update_inlet_temperature(current_inlet_temp, total_demand)
            pressure = self.calculate_pressure(total_demand)

            self.temperatures.append(current_inlet_temp)
            self.pressures.append(pressure)
            self.demands.append(total_demand)
