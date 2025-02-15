import cpuinfo  # pip install py-cpuinfo

def get_cpu_name_cpuinfo():
    return cpuinfo.get_cpu_info()['brand_raw']

print(get_cpu_name_cpuinfo())  # Выведет точное название процессора