from config import config


class Flat:
    def __init__(self, has_boiler: bool, boiler_temp: float = None):
        self.has_boiler = has_boiler
        if boiler_temp is None:
            boiler_temp = config.boiler_initial_temp
        self.boiler_temp = boiler_temp
        self.water_temp = config.ambient_temp

    def use_water(self, volume: float, inlet_temp: float) -> float:
        if self.has_boiler and self.boiler_temp > inlet_temp:
            mixed_temp = (self.boiler_temp * volume + inlet_temp * volume) / (2 * volume)
            return mixed_temp
        return inlet_temp

    def heat_loss(self):
        if self.has_boiler:
            self.boiler_temp = max(
                config.ambient_temp,
                self.boiler_temp - config.boiler_heat_loss_per_step
            )
