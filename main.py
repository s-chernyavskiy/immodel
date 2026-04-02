import matplotlib.pyplot as plt
import numpy as np
from generator import Generator
from building import Building

def main():
    NUM_APARTMENTS = 100
    BOILER_PROBABILITY = float(input())
    SIMULATION_DAYS = 1000
    TIME_STEP = 5

    g = Generator()
    building = Building(NUM_APARTMENTS, BOILER_PROBABILITY, g, TIME_STEP)

    for day in range(SIMULATION_DAYS):
        building.simulate_day(day)

    temps = np.array(building.temperatures)
    gost_requirement = 50
    print(len(building.temperatures))

    pressures = np.array(building.pressures)
    demands = np.array(building.demands)
    fig, axes = plt.subplots(3, 1, figsize=(10, 8))
    ax1 = axes[0]
    ax1.plot(temps[:24*60//TIME_STEP], linewidth=1)
    ax1.axhline(y=gost_requirement, color='r', label='ГОСТ')
    ax1.set_title('Температура воды')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    ax2 = axes[1]
    ax2.plot(pressures[:24*60//TIME_STEP], linewidth=1, color='orange')
    ax2.axhline(y=0.5, color='r', label='Норма')
    ax2.set_title('Напор в трубах')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    ax3 = axes[2]
    ax3.plot(demands[:24*60//TIME_STEP], linewidth=1, color='green')
    ax3.set_title('Потребление воды')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()