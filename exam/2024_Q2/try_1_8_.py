# pyside6-designer
# cd E:\it\python\6.1 pyside6_materials\PySide\exam\2024_Q2\ui
# PySide6-uic try_1_8.ui -o try_1_8.py

'''
import psutil
from PySide6 import QtWidgets
from ui.try_1_8 import Ui_MainWindow


class Window(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.cpu_load)

    def cpu_load(self):
        cpu_load = psutil.cpu_percent(interval=1)
        self.ui.lineEdit.setText(str(cpu_load))


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
'''

import psutil
from PySide6 import QtWidgets, QtCore
from ui.try_1_8 import Ui_MainWindow


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        #  Запуск автообновления каждые 1000 мс (1 сек)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.cpu_load)  # Подключаем метод обновления
        self.timer.start(1000)  # Запускаем таймер (1000 мс = 1 сек)

    def cpu_load(self):
        cpu_load = psutil.cpu_percent(interval=0)  # Получаем загруженность CPU
        self.ui.lineEdit.setText(f"{cpu_load:.2f} %")  # Обновляем поле


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
