# import cpuinfo  # pip install py-cpuinfo
#
# def get_cpu_name_cpuinfo():
#     return cpuinfo.get_cpu_info()['brand_raw']
#
# print(get_cpu_name_cpuinfo())  # Выведет точное название процессора


# import os
#
# cpu_cores = os.cpu_count()  # Возвращает количество логических ядер
# print(f"Количество ядер процессора: {cpu_cores}")
#
# import psutil


import psutil
# cpu_load = psutil.cpu_percent(interval=1)  # Получаем загрузку CPU за 1 секунду
# print(f"Текущая загрузка процессора: {cpu_load}%")
# print(type(cpu_load))

import psutil

# def get_disk_letters():
#     return [disk.device for disk in psutil.disk_partitions(all=True)]
#
# print("Диски:", get_disk_letters())



def get_disk_info():
    disks = psutil.disk_partitions(all=True)  # Получаем список всех дисков
    for disk in disks:
        usage = psutil.disk_usage(disk.mountpoint)  # Получаем статистику по диску
        print(f"Диск {disk.device}")
        print(f"  Общий объем: {usage.total / (1024 ** 3):.2f} ГБ")
        print(f"  Занято: {usage.used / (1024 ** 3):.2f} ГБ")


get_disk_info()

# usage.total - количество занятого места на диске в байтах
# 1 ГБ (гигабайт) = 1024 × 1024 × 1024 байта = 1024³ байта
# :.2f - форматирует число, оставляя 2 знака после запятой
