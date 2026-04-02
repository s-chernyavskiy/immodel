from generator import Generator
from building import Building
import numpy as np
import matplotlib.pyplot as plt

def run_scenario(boiler_probability, num_apartments=100, days=30):
    g = Generator()
    building = Building(num_apartments, boiler_probability, g)

    for day in range(days):
        building.simulate_day(day)

    return building

# Сравнение
print("Сравнение сценариев: без бойлеров vs с бойлерами (30%)")

# Сценарий без бойлеров
print("\nСимуляция без бойлеров...")
building_no_boilers = run_scenario(0.0)

# Сценарий с бойлерами
print("Симуляция с бойлерами (30%)...")
building_with_boilers = run_scenario(0.3)

# Сравнение температур
temps_no = np.array(building_no_boilers.temperatures)
temps_with = np.array(building_with_boilers.temperatures)

print(f"\nМинимальная температура без бойлеров: {np.min(temps_no):.1f}°C")
print(f"Минимальная температура с бойлерами: {np.min(temps_with):.1f}°C")
print(f"Улучшение: {np.min(temps_with) - np.min(temps_no):.1f}°C")

# Сравнение напора
pressure_no = np.array(building_no_boilers.pressures)
pressure_with = np.array(building_with_boilers.pressures)

print(f"\nСредний напор без бойлеров: {np.mean(pressure_no):.2f}")
print(f"Средний напор с бойлерами: {np.mean(pressure_with):.2f}")
print(f"Улучшение: {(np.mean(pressure_with) - np.mean(pressure_no)) * 100:.1f}%")