class Flat:
    def __init__(self, has_boiler: bool, boiler_temp: float = 70.0):
        self.has_boiler = has_boiler
        self.boiler_temp = boiler_temp
        self.water_temp = 25.0

    def use_water(self, volume: float, inlet_temp: float) -> float:
        if self.has_boiler and self.boiler_temp > inlet_temp:
            mixed_temp = (self.boiler_temp * volume + inlet_temp * volume) / (2 * volume)
            return mixed_temp
        return inlet_temp

    def heat_loss(self, ambient_temp: float = 25.0):
        if self.has_boiler:
            self.boiler_temp = max(ambient_temp, self.boiler_temp - 0.5)