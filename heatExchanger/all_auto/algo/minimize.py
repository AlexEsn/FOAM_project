import subprocess
import shutil
from scipy.optimize import minimize
import numpy as np

# Параметры
min_value = 0
max_value = 20
min_step = 2  # Минимальный шаг

salome_executable = "~/SALOME-9.11.0-native-UB20.04-SRC/binsalome"
base_path = '.'
python_script = base_path + "/autogenerate_template.py"

last_value = None  # Переменная для хранения предыдущего значения


def objective_function(shifts):
    global last_value
    shift_first_cylinder, shift_second_cylinder = map(int, shifts)
    new_name = f"_{shift_first_cylinder}_{shift_second_cylinder}_0"

    source_folder = f"{base_path}/case"
    destination_folder = f"{base_path}/case{new_name}"

    try:
        # Копирование кейса
        shutil.copytree(source_folder, destination_folder)

        # Команда для запуска SALOME и выполнения питон-скрипта внутри SALOME
        command = f'{salome_executable} -t python {python_script} args:{shift_first_cylinder},{shift_second_cylinder},0,{destination_folder}/mesh.unv'
        subprocess.run(command, shell=True)

        bash_script_path = f"./case{new_name}/Allmesh >> /dev/null"
        subprocess.check_output(bash_script_path, shell=True, text=True)
    except Exception as e:
        print(f"Произошла ошибка при копировании или расчете сетки: {e}")

    try:
        bash_script_path = f"./case{new_name}/Allrun >> /dev/null"
        subprocess.check_output(bash_script_path, shell=True, text=True)

        file_path = f"{base_path}/case{new_name}/postProcessing/heater/cellMaxHeaterT/0/volFieldValue.dat"

        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in reversed(lines):
                if line.strip():
                    current_value = float(line.split()[-1])
                    break

        return current_value
    except Exception as e:
        print(f"Произошла ошибка: {str(e)}")


if __name__ == "__main__":
    bounds = [(min_value, max_value), (min_value, max_value)]
    initial_guess = np.array([min_value, min_value])

    result = minimize(objective_function, initial_guess,
                      bounds=bounds, method='L-BFGS-B', options={'eps': min_step})

    print("Оптимальные сдвиги:", result.x)
    print("Минимальное значение функции:", result.fun)
