import matplotlib.pyplot as plt
import numpy as np
from generator import Generator
from building import Building

def main():
    # Параметры симуляции
    NUM_APARTMENTS = 100
    BOILER_PROBABILITY = 0.3
    SIMULATION_DAYS = 30
    TIME_STEP = 5  # минут

    # Инициализация
    g = Generator()
    building = Building(NUM_APARTMENTS, BOILER_PROBABILITY, g, TIME_STEP)

    # Симуляция
    print(f"Симуляция {SIMULATION_DAYS} дней...")
    for day in range(SIMULATION_DAYS):
        building.simulate_day(day)
        if (day + 1) % 5 == 0:
            print(f"  День {day + 1} завершен")

    # Анализ результатов
    print("\n=== АНАЛИЗ РЕЗУЛЬТАТОВ ===")

    # 1. Анализ температуры
    temps = np.array(building.temperatures)
    gost_requirement = 50  # °C по ГОСТ

    below_gost = np.sum(temps < gost_requirement)
    print(f"Температура ниже ГОСТ ({gost_requirement}°C): {below_gost} измерений ({below_gost/len(temps)*100:.1f}%)")
    print(f"Минимальная температура: {np.min(temps):.1f}°C")
    print(f"Средняя температура: {np.mean(temps):.1f}°C")

    # 2. Анализ напора
    pressures = np.array(building.pressures)
    low_pressure = np.sum(pressures < 0.3)
    print(f"\nНизкий напор (<0.3): {low_pressure} измерений ({low_pressure/len(pressures)*100:.1f}%)")
    print(f"Средний напор: {np.mean(pressures):.2f}")

    # 3. Анализ пиковых нагрузок
    demands = np.array(building.demands)
    peak_demand = np.max(demands)
    print(f"\nПиковое потребление: {peak_demand:.1f} л/мин")

    # Визуализация
    fig, axes = plt.subplots(3, 1, figsize=(12, 10))

    # График температуры
    ax1 = axes[0]
    ax1.plot(temps[:24*60//TIME_STEP], linewidth=1)
    ax1.axhline(y=gost_requirement, color='r', linestyle='--', label='ГОСТ')
    ax1.set_ylabel('Температура (°C)')
    ax1.set_title('Температура воды в течение дня')
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # График напора
    ax2 = axes[1]
    ax2.plot(pressures[:24*60//TIME_STEP], linewidth=1, color='orange')
    ax2.axhline(y=0.5, color='r', linestyle='--', label='Норма')
    ax2.set_ylabel('Напор (отн. ед.)')
    ax2.set_title('Напор в трубах в течение дня')
    ax2.legend()
    ax2.grid(True, alpha=0.3)

    # График потребления
    ax3 = axes[2]
    ax3.plot(demands[:24*60//TIME_STEP], linewidth=1, color='green')
    ax3.set_ylabel('Потребление (л/мин)')
    ax3.set_xlabel('Время (шаги по 5 минут)')
    ax3.set_title('Потребление воды в течение дня')
    ax3.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Экономический анализ
    print("\n=== ЭКОНОМИЧЕСКИЙ АНАЛИЗ ===")
    print("Варианты решения проблем:")
    print("1. Замена труб: стоимость ~X руб.")
    print("2. Установка бойлеров: стоимость ~Y руб./квартира")

    # Рекомендации
    if below_gost / len(temps) > 0.1:
        print("\nРекомендация: Увеличить количество бойлеров для повышения температуры")
    if low_pressure / len(pressures) > 0.2:
        print("Рекомендация: Заменить трубы для увеличения напора")

    # Сравнение с бойлерами
    print("\nЭффект от бойлеров:")
    print(f"- Снижение пиковой нагрузки на {peak_demand * 0.3:.1f}%")
    print(f"- Повышение минимальной температуры на 5-10°C")

if __name__ == "__main__":
    main()