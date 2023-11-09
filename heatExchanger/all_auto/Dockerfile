# Используем официальный образ Ubuntu 20.04
FROM ubuntu:20.04

# Копируем архив SALOME в контейнер
COPY SALOME-9.11.0-native-UB20.04.tar.gz /tmp/SALOME-9.11.0.tgz

# Распаковываем архив SALOME
RUN tar xzf /tmp/SALOME-9.11.0.tgz -C /opt \
    && rm /tmp/SALOME-9.11.0.tgz

# Устанавливаем окружение Salome
ENV ROOT="/opt/SALOME-9.11.0-native-UB20.04-SRC"

# Устанавливаем рабочий каталог
WORKDIR $ROOT

# Устанавливаем необходимые Linux-пакеты
RUN ./sat/sat config SALOME-9.11.0-native --check_system

# Подготавливаем исходные файлы приложения
# RUN ./sat/sat prepare SALOME-9.11.0-native

# Собираем SALOME-9.11.0-native
# RUN ./sat/sat -t compile SALOME-9.11.0-native

# Создаем лаунчер для SALOME
# RUN ./sat/sat launcher SALOME-9.11.0-native

# Устанавливаем окружение библиотек
# RUN ./sat/sat environ SALOME-9.11.0-native
# RUN apt-get update -y && apt-get upgrade -y

# Устанавливаем окружение SALOME
# ENV PATH="/opt/SALOME-9.11.0:$PATH"

# Устанавливаем рабочий каталог
# WORKDIR /root

# Запускаем bash при запуске контейнера
# CMD ["/bin/bash"]
