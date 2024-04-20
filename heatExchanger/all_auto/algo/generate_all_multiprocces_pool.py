import subprocess
import shutil
from itertools import product
from multiprocessing import Manager, Pool
import random

# Параметры
min_value = 0
step = 5
max_value = 20

salome_executable = "~/SALOME-9.11.0-native-UB20.04-SRC/binsalome"
base_path = '.'
python_script = base_path + "/autogenerate_with_block.py"
core_num = 6


def run_simulation(blocks, all_data):
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

    print("Запуск расчета")

    bash_script_path = f"./case{new_name}/Allmesh >> /dev/null"

    try:
        result = subprocess.check_output(
            bash_script_path, shell=True, text=True)
        print(result)
        print("Расчет сетки успешно выполнен.")
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка при выполнении расчета сетки: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")

    bash_script_path = f"./case{new_name}/Allrun >> /dev/null"

    try:
        result = subprocess.check_output(
            bash_script_path, shell=True, text=True)
        print(result)
        print("Расчет кейса успешно выполнен.")
        print("Ищем последнее значение")
        file_path = f"{base_path}/case{new_name}/postProcessing/heater/cellMaxHeaterT/0/volFieldValue.dat"

        # Пытаемся открыть файл
        try:
            with open(file_path, 'r') as file:
                lines = file.readlines()
                # Ищем строку с последним значением
                for line in reversed(lines):
                    if line.strip():
                        last_value = float(line.split()[-1])
                        break
                print(f"Последнее значение: {last_value:.6e}")

                # Добавляем значение в разделяемый словарь
                all_data[new_name] = last_value
        except FileNotFoundError:
            print(f"Файл '{file_path}' не найден.")
        except Exception as e:
            print(f"Произошла ошибка: {str(e)}")
    except subprocess.CalledProcessError as e:
        print(f"Произошла ошибка при выполнении расчета кейса: {e}")
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")


if __name__ == "__main__":
    # Создаем разделяемый словарь для сбора результатов от каждого процесса
    with Manager() as manager:
        all_data = manager.dict()

        # Создаем список с возможными значениями
        # values = [i for i in range(min_value, max_value + step, step)]
        # Получаем все возможные комбинации с повторениями из двух чисел
        # combinations_with_repeats = list(product(values, repeat=2))

        # Создаем и запускаем отдельный процесс для каждой комбинации
        random_array = [random.choice([0, 1]) for _ in range(36)]
        run_simulation(random_array, all_data=all_data)
        # with Pool(core_num) as pool:
        #     pool.starmap(run_simulation, [(s1, s2, 0, all_data)
        #                  for s1, s2 in combinations_with_repeats])
        #     pool.join

        # Выводим результаты из разделяемого словаря
        print(all_data)
        print(len(all_data))
