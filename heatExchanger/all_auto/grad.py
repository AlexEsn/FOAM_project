import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Функция, для которой мы будем оптимизировать


def target_function(x, y):
    return x**2 + y**2

# Градиент функции


def gradient(x, y):
    grad_x = 2 * x
    grad_y = 2 * y
    return np.array([grad_x, grad_y])

# Функция градиентного спуска


def gradient_descent(starting_point, learning_rate, num_iterations):
    points = [starting_point]
    for _ in range(num_iterations):
        current_point = points[-1]
        grad = gradient(*current_point)
        new_point = current_point - learning_rate * grad
        points.append(new_point)
    return np.array(points)


# Создание 3D графика
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Создание сетки для отображения поверхности
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
x, y = np.meshgrid(x, y)
z = target_function(x, y)

# Отображение поверхности
ax.plot_surface(x, y, z, alpha=0.5, cmap='viridis')

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
learning_rate = 0.1
num_iterations = 20
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
