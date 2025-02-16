# PySide6-uic exam_task_form.ui -o exam_task_form.py

import psutil
import subprocess
import platform
from PySide6 import QtWidgets, QtCore
from ui.exam_task_form import Ui_MainWindow


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.get_system_info)

        self.change_update_interval()
        self.ui.comboBox.currentIndexChanged.connect(self.change_update_interval)

    def change_update_interval(self):
        interval = int(self.ui.comboBox.currentText()) * 1000
        self.timer.setInterval(interval)
        self.timer.start()

    def get_system_info(self):
        self.get_cpu_name()
        self.get_number_of_cores()
        self.cpu_load()
        self.get_disk_info()
        self.ram_total()
        self.ram_load()
        self.get_processes()
        self.get_services()
        self.get_scheduled_tasks()

    def get_cpu_name(self):
        cpu_name = platform.processor()
        self.ui.lineEdit.setText(cpu_name)

    def get_number_of_cores(self):
        number_of_f_cores = psutil.cpu_count(logical=False)
        number_of_l_cores = psutil.cpu_count(logical=True)
        self.ui.lineEdit_2.setText(f"физических - {number_of_f_cores}, логических - {number_of_l_cores} ")

    def cpu_load(self):
        cpu_load = psutil.cpu_percent(interval=None)
        self.ui.lineEdit_3.setText(f" {cpu_load} %")

    def ram_total(self):
        ram_total = round(psutil.virtual_memory().total/(1024 ** 3),2)
        self.ui.lineEdit_4.setText(f" {ram_total} ГБ")

    def ram_load(self):
        ram_load = psutil.virtual_memory().percent
        self.ui.lineEdit_5.setText(f" {ram_load} %")

    def get_disk_info(self):
        disks = psutil.disk_partitions(all=True)
        text_ = []
        for disk in disks:
            usage = psutil.disk_usage(disk.mountpoint)
            text_.append(f"Диск {disk.device}:\n  Общий объем: {usage.total / (1024 ** 3):.2f} ГБ\n  Занято: {usage.used / (1024 ** 3):.2f} ГБ\n")
        self.ui.textEdit.setText("\n".join(text_))

    def get_processes(self):
        processes = []
        for process in psutil.process_iter(attrs=['name']):
            processes.append(process.info['name'])
        self.ui.textEdit_2.setText("\n".join(processes))

    def get_services(self):
        var = subprocess.run(
            ["sc", "query", "type=", "service", "state=", "all"],
            capture_output=True, text=True, encoding="cp866")

        services = []
        for line in var.stdout.split("\n"):
            if "SERVICE_NAME" in line:
                service_name = line.split(":")[1].strip()
                services.append(service_name)

        self.ui.textEdit_3.setText("\n".join(services))

    def get_scheduled_tasks(self):
        var = subprocess.run(
            ["schtasks"],
            capture_output=True, text=True, encoding="cp866" )
        scheduled_tasks = var.stdout.split("\n")
        self.ui.textEdit_4.setText("\n".join(scheduled_tasks))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()