import psutil
import os
import platform
from PySide6 import QtWidgets, QtCore  # Используем QtCore для работы с потоками и сигналами
from ui.try_1_6 import Ui_MainWindow


class GetSystemInfoThread(QtCore.QThread):  # Создаем класс для потока получения данных о системе
    update_signal = QtCore.Signal(str, str, str)  # Создаем сигнал для отправки данных (CPU, ядра, нагрузка)

    def run(self):
        # Получаем данные о процессоре, ядрах и нагрузке
        cpu_name = platform.processor()
        number_of_cores = os.cpu_count()
        cpu_load = psutil.cpu_percent(interval=1)

        # Отправляем результат через сигнал в основной поток
        self.update_signal.emit(cpu_name, str(number_of_cores), str(cpu_load))


class GetDiskInfoThread(QtCore.QThread):  # Создаем класс для потока получения данных о дисках
    update_signal = QtCore.Signal(str)  # Сигнал для передачи информации о дисках

    def run(self):
        disks = psutil.disk_partitions(all=True)  # Получаем список всех дисков
        text_ = []
        for disk in disks:
            usage = psutil.disk_usage(disk.mountpoint)
            text_.append(
                f"Диск {disk.device}:\n  Общий объем: {usage.total / (1024 ** 3):.2f} ГБ\n  Занято: {usage.used / (1024 ** 3):.2f} ГБ\n")

        # Отправляем данные о дисках
        self.update_signal.emit("\n".join(text_))


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.get_system_info)
        self.ui.pushButton_2.clicked.connect(self.get_disk_info)

    def get_system_info(self):
        self.thread_system_info = GetSystemInfoThread()  # Создаем поток для получения данных о системе
        self.thread_system_info.update_signal.connect(self.update_system_info)  # Подключаем сигнал
        self.thread_system_info.start()  # Запускаем поток

    def get_disk_info(self):
        self.thread_disk_info = GetDiskInfoThread()  # Создаем поток для получения данных о дисках
        self.thread_disk_info.update_signal.connect(self.update_disk_info)  # Подключаем сигнал
        self.thread_disk_info.start()  # Запускаем поток

    def update_system_info(self, cpu_name, number_of_cores, cpu_load):
        # Обновляем данные о системе в интерфейсе
        self.ui.lineEdit.setText(cpu_name)
        self.ui.lineEdit_2.setText(number_of_cores)
        self.ui.lineEdit_3.setText(cpu_load)

    def update_disk_info(self, disk_info):
        # Обновляем данные о дисках в текстовом поле
        self.ui.textEdit.setText(disk_info)


if __name__ == "__main__":
    app = QtWidgets.QApplication()  # Создание объекта приложения

    window = Window()  # Создание экземпляра окна
    window.show()  # Отображение окна

    app.exec()  # Запуск главного цикла событий
