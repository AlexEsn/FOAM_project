import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import griddata
from matplotlib.animation import FuncAnimation

# Ваши данные
c2_step1_mini_duck_copper = {'_0_0_0': 621.8428, '_2_2_0': 623.7642, '_6_6_0': 617.6467, '_4_20_0': 614.1173, '_4_12_0': 619.1042, '_0_8_0': 620.1099, '_2_18_0': 616.7918, '_4_4_0': 620.0076, '_2_10_0': 611.1027, '_0_16_0': 617.2722, '_2_4_0': 619.1191, '_0_2_0': 619.975, '_6_8_0': 613.7497, '_4_6_0': 616.4939, '_6_0_0': 617.9549, '_0_10_0': 615.7165, '_2_20_0': 616.9169, '_4_14_0': 619.0111, '_2_12_0': 615.0275, '_0_18_0': 616.0975, '_0_4_0': 621.6282, '_2_6_0': 618.9948, '_4_8_0': 615.741, '_6_2_0': 619.2579, '_6_10_0': 612.5962, '_4_0_0': 617.6396, '_4_16_0': 614.894, '_0_12_0': 614.0844, '_2_14_0': 617.751, '_0_20_0': 617.7456, '_0_6_0': 619.656, '_2_8_0': 617.5491, '_6_4_0': 617.774, '_4_2_0': 621.0579, '_6_12_0': 611.8686, '_4_10_0': 614.9631, '_4_18_0': 615.5519, '_0_14_0': 617.9203, '_2_16_0': 619.3441, '_2_0_0': 620.8749, '_6_14_0': 615.3382, '_8_0_0': 617.5813, '_8_8_0': 615.3508, '_8_16_0': 614.9662, '_10_2_0': 619.5612, '_10_10_0': 612.3677, '_10_18_0': 617.791, '_12_4_0': 616.2421, '_12_12_0': 615.6871, '_12_20_0': 613.0879, '_8_2_0': 617.4507, '_6_16_0': 613.0379, '_8_10_0': 614.6299, '_10_4_0': 617.2055, '_8_18_0': 612.6031, '_12_6_0': 614.0602, '_10_12_0': 613.9007, '_10_20_0': 612.8109, '_12_14_0': 614.0762, '_14_0_0': 617.7101, '_8_4_0': 617.4561,
                             '_6_18_0': 614.1392, '_10_6_0': 616.101, '_8_12_0': 613.0557, '_8_20_0': 613.4314, '_12_8_0': 611.0876, '_12_0_0': 618.6528, '_12_16_0': 615.746, '_10_14_0': 614.5143, '_14_2_0': 619.3797, '_8_6_0': 615.3026, '_10_8_0': 612.4367, '_6_20_0': 616.0611, '_8_14_0': 614.8857, '_10_0_0': 615.4421, '_12_2_0': 618.2412, '_10_16_0': 616.7581, '_12_10_0': 614.2464, '_14_4_0': 614.629, '_12_18_0': 616.3525, '_14_6_0': 612.8889, '_14_14_0': 614.3802, '_16_0_0': 617.1498, '_16_16_0': 617.9745, '_16_8_0': 615.0309, '_18_2_0': 616.6977, '_18_10_0': 613.8529, '_20_4_0': 617.1874, '_18_18_0': 616.869, '_20_12_0': 614.3073, '_14_8_0': 614.8454, '_14_16_0': 615.5209, '_16_2_0': 619.6522, '_16_10_0': 613.7143, '_18_4_0': 614.3781, '_16_18_0': 616.6089, '_18_12_0': 612.0802, '_20_6_0': 612.1871, '_18_20_0': 614.1018, '_20_14_0': 616.2906, '_14_10_0': 611.5639, '_16_4_0': 617.9298, '_14_18_0': 615.5829, '_16_12_0': 616.9915, '_18_6_0': 614.3813, '_16_20_0': 615.8814, '_18_14_0': 613.8126, '_20_0_0': 618.8143, '_20_8_0': 612.2661, '_20_16_0': 617.567, '_14_12_0': 615.6865, '_16_6_0': 615.1323, '_14_20_0': 616.3118, '_18_8_0': 611.9539, '_16_14_0': 616.8639, '_18_0_0': 616.1102, '_18_16_0': 618.1638, '_20_2_0': 620.965, '_20_18_0': 621.5524, '_20_10_0': 616.0832, '_20_20_0': 616.5326}


# Разделите ключи словаря на списки x, y и z
x, y, z = [], [], []
for key, value in c2_step1_mini_duck_copper.items():
    parts = key.split('_')
    x.append(int(parts[1]))
    y.append(int(parts[2]))
    z.append(value)


# Функция, которую будем минимизировать
def target_function(x_new, y_new):
    z_new = griddata((x, y), z, (x_new, y_new), method='linear')
    return z_new


# Градиент функции


def gradient(x_new, y_new):
    h = 1e-6
    partial_x = (target_function(x_new + h, y_new) -
                 target_function(x_new - h, y_new)) / (2 * h)
    partial_y = (target_function(x_new, y_new + h) -
                 target_function(x_new, y_new - h)) / (2 * h)
    return np.array([partial_x, partial_y])

# Функция градиентного спуска


def gradient_descent(starting_point, learning_rate, num_iterations):
    points = [starting_point]
    for _ in range(num_iterations):
        current_point = points[-1]
        grad = gradient(*current_point)
        new_point = current_point - learning_rate * grad
        points.append(new_point)
    return np.array(points)


# Создание сетки для поверхности
xi, yi = np.meshgrid(np.linspace(min(x), max(x), 100),
                     np.linspace(min(y), max(y), 100))
zi = griddata((x, y), z, (xi, yi), method='linear')

# Инициализация графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Построение поверхности
ax.plot_surface(xi, yi, zi, alpha=0.5, cmap='viridis')

# Начальная точка оптимизации
starting_point = np.array([2.5, 2.5, target_function(2.5, 2.5)])
ax.scatter(*starting_point, color='red', marker='o', label='Starting Point')

# Инициализация пустого графика
line, = ax.plot([], [], [], color='blue', marker='o', label='Gradient Descent')
points, = ax.plot([], [], [], color='blue', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()

# Функция для инициализации анимации


def init():
    line.set_data([], [])
    line.set_3d_properties([])
    return line,

# Функция обновления анимации


def update(frame):
    line.set_data(gd_points_with_z[:frame, 0], gd_points_with_z[:frame, 1])
    line.set_3d_properties(gd_points_with_z[:frame, 2])
    return line,


# Градиентный спуск
learning_rate = 1
num_iterations = 30
gd_points = gradient_descent(starting_point[:2], learning_rate, num_iterations)
gd_points_with_z = np.c_[gd_points, np.array(
    [target_function(*point) for point in gd_points])]

# Создание анимации
ani = FuncAnimation(fig, update, frames=num_iterations,
                    init_func=init, blit=True)

# Сохранение анимации в файл GIF
ani.save('gradient_descent_animation.gif', writer='imagemagick', fps=2)

# Отображение анимации в интерактивном режиме (если нужно)
plt.show()
