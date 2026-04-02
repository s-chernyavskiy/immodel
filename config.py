import json
import os

class Config:
    _instance = None
    _config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8-sig') as f:
            self._config = json.load(f)

    def get(self, key_path: str, default=None):
        keys = key_path.split('.')
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key, default)
            else:
                return default
        return value

    @property
    def num_apartments(self):
        return self._config['simulation']['num_apartments']

    @property
    def simulation_days(self):
        return self._config['simulation']['simulation_days']

    @property
    def time_step_minutes(self):
        return self._config['simulation']['time_step_minutes']

    @property
    def inlet_temp(self):
        return self._config['temperature']['inlet_temp']

    @property
    def ambient_temp(self):
        return self._config['temperature']['ambient_temp']

    @property
    def boiler_initial_temp(self):
        return self._config['temperature']['boiler_initial_temp']

    @property
    def boiler_heat_loss_per_step(self):
        return self._config['temperature']['boiler_heat_loss_per_step']

    @property
    def gost_requirement(self):
        return self._config['temperature']['gost_requirement']

    @property
    def pressure_normal(self):
        return self._config['temperature']['pressure_normal']

    @property
    def normal_mean(self):
        return self._config['water_consumption']['normal_mean']

    @property
    def normal_std(self):
        return self._config['water_consumption']['normal_std']

    @property
    def max_demand_per_apartment(self):
        return self._config['pressure']['max_demand_per_apartment']

    @property
    def rates_by_hour(self):
        return self._config['exponential']['rates_by_hour']

config = Config()