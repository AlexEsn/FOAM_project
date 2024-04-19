import subprocess
import shutil
import random
from deap import base, creator, tools, algorithms
import numpy as np
import multiprocessing
import random

# Параметры
min_value = 0
max_value = 20

salome_executable = "~/SALOME-9.11.0-native-UB20.04-SRC/binsalome"
base_path = '.'
python_script = base_path + "/autogenerate_with_block.py"

all_data = {}


def objective_function(blocks):
    blocks_name = '_'.join(map(str, blocks))
    new_name = f"_{blocks_name}"

    source_folder = f"{base_path}/case"
    destination_folder = f"{base_path}/case{new_name}"

    try:
        # Копирование кейса
        shutil.copytree(source_folder, destination_folder)
        print(
            f"Папка {source_folder} успешно скопирована в {destination_folder}")

        # Команда для запуска SALOME и выполнения питон-скрипта внутри SALOME
        args = ','.join(map(str, blocks))
        command = f'{salome_executable} -t python {python_script} args:{destination_folder}/mesh.unv,{args}'
        print(command)
        print("Генерация сетки")
        # Запуск команды с помощью subprocess
        subprocess.run(command, shell=True)
    except Exception as e:
        print(f"Произошла ошибка при копировании или расчете сетки: {e}")
    try:
        print("Запуск расчета")
        bash_script_path = f"./case{new_name}/Allmesh >> /dev/null"

        # Запуск расчета сетки
        subprocess.check_output(bash_script_path, shell=True, text=True)

        bash_script_path = f"./case{new_name}/Allrun >> /dev/null"
        # bash_script_path = f"./case{new_name}/Allrun-parallel >> /dev/null"

        # Запуск расчета кейса
        subprocess.check_output(bash_script_path, shell=True, text=True)
    except Exception as e:
        print(f"Произошла ошибка при расчете: {e}")

    try:

        print("Ищем последнее значение")
        file_path = f"{base_path}/case{new_name}/postProcessing/heater/cellMaxHeaterT/0/volFieldValue.dat"

        # Пытаемся открыть файл
        with open(file_path, 'r') as file:
            lines = file.readlines()
            # Ищем строку с последним значением
            for line in reversed(lines):
                if line.strip():
                    last_value = float(line.split()[-1])
                    break
            print(f"Последнее значение: {last_value:.6e}")
        all_data[new_name] = last_value

        return (last_value, )  # Возвращаем кортеж
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


def evaluate_parallel(individual):
    return objective_function(individual),


# Создание классов для определения типа оптимизации
creator.create("FitnessMin", base.Fitness, weights=(-1.0, ))
creator.create("Individual", list, fitness=creator.FitnessMin)

# Определение функций для работы с особями и популяцией
toolbox = base.Toolbox()
toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat,
                 creator.Individual, toolbox.attr_bool, n=36)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)
toolbox.register("evaluate", objective_function)

if __name__ == "__main__":
    # Process Pool
    cpu_count = multiprocessing.cpu_count() // 2
    print(f"CPU count: {cpu_count}")
    pool = multiprocessing.Pool(cpu_count)
    toolbox.register("map", pool.map)

    # Инициализация популяции
    population = toolbox.population(n=1)

    # Определение параметров эволюционного алгоритма
    cxpb, mutpb, ngen = 0.7, 0.2, 100

    # Запуск эволюционного алгоритма с использованием пула процессов
    algorithms.eaSimple(population, toolbox, cxpb, mutpb, ngen,
                        stats=None, halloffame=None, verbose=True)

    # Закрытие пула процессов после выполнения
    pool.close()
    pool.join()

    # Вывод результатов оптимизации
    best_individual = tools.selBest(population, k=1)[0]
    print("Оптимальные сдвиги:", best_individual)
    print("Минимальное значение функции:", best_individual.fitness.values[0])
    print(all_data)
