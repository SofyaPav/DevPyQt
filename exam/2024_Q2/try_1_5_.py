# pyside6-designer
# cd E:\it\python\6.1 pyside6_materials\PySide\exam\2024_Q2\ui
# PySide6-uic try_1_5.ui -o try_1_5.py
import psutil
import os
import platform  # Для получения информации о процессоре
from PySide6 import QtWidgets  # модуль из библиотеки PySide6, который содержит классы для работы с виджетами,
# такими как окна, кнопки, текстовые поля и т.д
from ui.try_1_5 import Ui_MainWindow  # импортируемый класс, который сгенерирован Qt Designer для интерфейса приложения


class Window(QtWidgets.QMainWindow):  # Создаем класс Window, который наследуется от QtWidgets.QMainWindow,
    # что позволяет нам создавать главное окно приложения
    def __init__(self, parent=None):
        super().__init__(parent)  # super().__init__(parent) — вызывает конструктор родительского класса (QMainWindow),
        # чтобы инициализировать все функции и методы, которые присущи основному окну

        self.ui = Ui_MainWindow()  # В конструкторе (методе __init__) мы создаем экземпляр класса Ui_MainWindow,
        # который содержит описание интерфейса, созданного с помощью Qt Designer.
        self.ui.setupUi(self)  # Мы также вызываем метод setupUi(self), который "настраивает" интерфейс для этого окна

        self.ui.pushButton.clicked.connect(self.get_system_info)
        self.ui.pushButton_2.clicked.connect(self.get_disk_info)

    def get_system_info(self):
        self.get_cpu_name()
        self.get_number_of_cores()
        self.cpu_load()


    def get_cpu_name(self):
        cpu_name = platform.processor()  # вызываем метод get_cpu_info, который возвращает информацию о процессоре
        self.ui.lineEdit.setText(cpu_name)  # вставляем эту информацию в lineEdit (текстовое поле)

    def get_number_of_cores(self):
        number_of_cores = os.cpu_count()  # Возвращает количество логических ядер
        self.ui.lineEdit_2.setText(str(number_of_cores))  # вставляем эту информацию в lineEdit (текстовое поле)

    def cpu_load(self):
        cpu_load = psutil.cpu_percent(interval=1)
        self.ui.lineEdit_3.setText(str(cpu_load))


    def get_disk_info(self):
        disks = psutil.disk_partitions(all=True)  # Получаем список всех дисков
        text_ = []
        for disk in disks:
            usage = psutil.disk_usage(disk.mountpoint)  # Получаем статистику по диску
            text_.append(f"Диск {disk.device}:\n  Общий объем: {usage.total / (1024 ** 3):.2f} ГБ\n  Занято: {usage.used / (1024 ** 3):.2f} ГБ\n")
        self.ui.textEdit.setText("\n".join(text_))



if __name__ == "__main__":
    app = QtWidgets.QApplication()  # Создание объекта приложения

    window = Window()  # Создание экземпляра окна
    window.show()  # Отображение окна

    app.exec()  # Запуск главного цикла событий