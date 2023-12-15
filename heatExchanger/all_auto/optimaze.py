import subprocess
import shutil
from scipy.optimize import differential_evolution
import numpy as np

# Параметры
min_value = 0
max_value = 20

salome_executable = "~/SALOME-9.11.0-native-UB20.04-SRC/binsalome"
base_path = '.'
python_script = base_path + "/autogenerate_template.py"

all_data = {}


def objective_function(shifts):
    shift_first_cylinder, shift_second_cylinder = map(int, shifts)
    new_name = f"_{shift_first_cylinder}_{shift_second_cylinder}_0"

    source_folder = f"{base_path}/case"
    destination_folder = f"{base_path}/case{new_name}"

    try:
        # Копирование кейса
        shutil.copytree(source_folder, destination_folder)
        print(
            f"Папка {source_folder} успешно скопирована в {destination_folder}")

        # Команда для запуска SALOME и выполнения питон-скрипта внутри SALOME
        command = f'{salome_executable} -t python {python_script} args:{shift_first_cylinder},{shift_second_cylinder},0,{destination_folder}/mesh.unv'
        print(command)
        print("Генерация сетки")

        # Запуск команды с помощью subprocess
        subprocess.run(command, shell=True)

        print("Запуск расчета")
        bash_script_path = f"./case{new_name}/Allmesh >> /dev/null"

        # Запуск расчета сетки
        subprocess.check_output(bash_script_path, shell=True, text=True)

        bash_script_path = f"./case{new_name}/Allrun >> /dev/null"

        # Запуск расчета кейса
        subprocess.check_output(bash_script_path, shell=True, text=True)
    except Exception as e:
        print(f"Произошла ошибка при копировании или расчете сетки: {e}")

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

        return last_value
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    # Определение ограничений на переменные (целые значения)
    bounds = [(min_value, max_value), (min_value, max_value)]

    # Оптимизация с использованием differential_evolution
    result = differential_evolution(objective_function, bounds)

    print(all_data)
    # Вывод результатов оптимизации
    print("Оптимальные сдвиги:", result.x)
    print("Минимальное значение функции:", result.fun)
