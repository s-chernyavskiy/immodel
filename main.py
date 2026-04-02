import time
import matplotlib.pyplot as plt
import numpy as np
from generator import Generator
from building import Building
from config import config


def main(boiler_probability: float):
    g = Generator()
    building = Building(boiler_probability, g)

    simulation_days = config.simulation_days
    time_step = config.time_step_minutes

    for day in range(simulation_days):
        print(f"{day / simulation_days * 100:.2f}%")
        building.simulate_day(day)

    temps = np.array(building.temperatures)
    gost_requirement = config.gost_requirement

    print(len(building.temperatures))

    pressures = np.array(building.pressures)
    demands = np.array(building.demands)

    steps_per_day = 24 * 60 // time_step
    hour_labels = np.linspace(0, 24, steps_per_day)

    fig_size = config.get('plots.figure_size', [10, 8])
    fig, axes = plt.subplots(3, 1, figsize=tuple(fig_size))

    ax1 = axes[0]
    ax1.plot(hour_labels, temps[:steps_per_day], linewidth=1)
    ax1.axhline(y=gost_requirement, color='r', linestyle='--', label='ГОСТ')
    ax1.set_title('Температура воды в течение дня')
    ax1.set_xlabel('Часы')
    ax1.set_ylabel('Температура (°C)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.plot(hour_labels, pressures[:steps_per_day], linewidth=1, color='orange')
    ax2.axhline(y=config.pressure_normal, color='r', linestyle='--', label='Норма')
    ax2.set_title('Напор в трубах в течение дня')
    ax2.set_xlabel('Часы')
    ax2.set_ylabel('Напор (отн. ед.)')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = axes[2]
    ax3.plot(hour_labels, demands[:steps_per_day], linewidth=1, color='green')
    ax3.set_title('Потребление воды в течение дня')
    ax3.set_xlabel('Часы')
    ax3.set_ylabel('Потребление (л/мин)')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    boiler_prob = float(input())

    start = time.time()
    main(boiler_prob)
    end = time.time()

    print(f"elapsed: {end - start:.2f}")
