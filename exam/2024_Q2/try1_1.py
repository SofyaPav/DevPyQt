# Задача.
# Разработать приложение для мониторинга нагрузки системы и системных процессов (аналог диспетчера задач).
#
# Обязательные функции в приложении:
#
# Показ общих сведений о системе (в текстовом виде!):
# Название процессора, количество ядер, текущая загрузка
# Общий объём оперативной памяти, текущая загрузка оперативаной памяти
# Количество, жестких дисков + информация по каждому (общий/занятый объём)
# Обеспечить динамический выбор обновления информации (1, 5, 10, 30 сек.)
# Показ работающих процессов
# Показ работающих служб
# Показ задач, которые запускаются с помощью планировщика задач




import sys
import psutil
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PySide6.QtCore import QTimer
from task_manager_ui import Ui_MainWindow  # Подключаем UI

class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_info)

        self.ui.comboBoxInterval.currentIndexChanged.connect(self.set_update_interval)

        self.update_info()
        self.set_update_interval()

    def set_update_interval(self):
        """ Меняет интервал обновления данных """
        interval = int(self.ui.comboBoxInterval.currentText()) * 1000
        self.timer.start(interval)

    def update_info(self):
        """ Обновляет сведения о системе """
        self.ui.labelCPU.setText(f"Процессор: {psutil.cpu_percent()}%")
        self.ui.labelMemory.setText(f"ОЗУ: {psutil.virtual_memory().percent}%")

        disks = psutil.disk_partitions()
        disk_info = "\n".join([f"{d.device}: {psutil.disk_usage(d.mountpoint).percent}%" for d in disks])
        self.ui.labelDisks.setText(f"Диски:\n{disk_info}")

        self.update_processes()
        self.update_services()

    def update_processes(self):
        """ Заполняет таблицу процессов """
        self.ui.tableProcesses.setRowCount(0)
        for proc in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent']):
            row = self.ui.tableProcesses.rowCount()
            self.ui.tableProcesses.insertRow(row)
            for col, value in enumerate(proc.info.values()):
                self.ui.tableProcesses.setItem(row, col, QTableWidgetItem(str(value)))

    def update_services(self):
        """ Заполняет таблицу служб (на Windows) """
        if sys.platform == "win32":
            import wmi
            c = wmi.WMI()
            self.ui.tableServices.setRowCount(0)
            for service in c.Win32_Service():
                row = self.ui.tableServices.rowCount()
                self.ui.tableServices.insertRow(row)
                self.ui.tableServices.setItem(row, 0, QTableWidgetItem(service.Name))
                self.ui.tableServices.setItem(row, 1, QTableWidgetItem(service.State))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())