# pyside6-designer
# cd E:\it\python\6.1 pyside6_materials\PySide\exam\2024_Q2\ui
# PySide6-uic try_1_7.ui -o try_1_7.py
import psutil

'''
import os
import platform
from PySide6 import QtWidgets
from ui.try_1_7 import Ui_MainWindow

class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.get_cpu_name)
        self.ui.pushButton_2.clicked.connect(self.get_number_of_cores)

    def get_cpu_name(self):
        cpu_name = platform.processor()
        self.ui.lineEdit.setText(cpu_name)

    def get_number_of_cores(self):
        number_of_cores = os.cpu_count()
        self.ui.lineEdit_2.setText(str(number_of_cores))

if __name__ == "__main__":
    app = QtWidgets.QApplication()  
    window = Window()  
    window.show()  
    app.exec()  
'''

import os
import platform
from PySide6 import QtWidgets, QtCore
from ui.try_1_7 import Ui_MainWindow


class CpuNameThread(QtCore.QThread):
    """Поток для получения названия процессора"""
    update_signal = QtCore.Signal(str)  # Сигнал для передачи данных

    def run(self):
        cpu_name = platform.processor()  # Получаем название процессора
        self.update_signal.emit(cpu_name)  # Отправляем результат в UI


class CoreCountThread(QtCore.QThread):
    """Поток для получения количества ядер"""
    update_signal = QtCore.Signal(str)

    def run(self):
        core_count = os.cpu_count()  # Получаем количество ядер
        self.update_signal.emit(str(core_count))  # Отправляем результат


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Подключение кнопок к потокам
        self.ui.pushButton.clicked.connect(self.get_cpu_name)
        self.ui.pushButton_2.clicked.connect(self.get_number_of_cores)

    def get_cpu_name(self):
        """Запуск потока для получения названия процессора"""
        self.cpu_thread = CpuNameThread()
        self.cpu_thread.update_signal.connect(self.update_cpu_name)
        self.cpu_thread.start()

    def get_number_of_cores(self):
        """Запуск потока для получения количества ядер"""
        self.core_thread = CoreCountThread()
        self.core_thread.update_signal.connect(self.update_core_count)
        self.core_thread.start()

    def update_cpu_name(self, cpu_name):
        """Обновление названия процессора в UI"""
        self.ui.lineEdit.setText(cpu_name)

    def update_core_count(self, core_count):
        """Обновление количества ядер в UI"""
        self.ui.lineEdit_2.setText(core_count)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()

