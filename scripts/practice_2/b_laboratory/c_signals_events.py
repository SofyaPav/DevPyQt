# pyside6-designer
# cd E:\it\python\6.1 pyside6_materials\PySide\scripts\practice_2\b_laboratory\ui
# PySide6-uic c_signals_events_form.ui -o c_signals_events_form.py


"""
Реализация программу проверки состояния окна:
Форма для приложения (ui/c_signals_events_form.ui)

Программа должна обладать следующим функционалом:

1. Возможность перемещения окна по заданным координатам.
2. Возможность получения параметров экрана (вывод производить в plainTextEdit + добавлять время).
    * Кол-во экранов
    * Текущее основное окно
    * Разрешение экрана
    * На каком экране окно находится
    * Размеры окна
    * Минимальные размеры окна
    * Текущее положение (координаты) окна
    * Координаты центра приложения
    * Отслеживание состояния окна (свернуто/развёрнуто/активно/отображено)
3. Возможность отслеживания состояния окна (вывод производить в консоль + добавлять время).
    * При перемещении окна выводить его старую и новую позицию
    * При изменении размера окна выводить его новый размер
"""

from ui.c_signals_events_form import Ui_Form
from PySide6 import QtWidgets, QtCore, QtGui
from datetime import datetime

class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        self.ui.pushButtonLT.clicked.connect(lambda: self.move_window(0, 0))  # Подключение кнопок перемещения
        self.ui.pushButtonRT.clicked.connect(lambda: self.move_window(self.screen_width() - self.width(), 0))
        self.ui.pushButtonLB.clicked.connect(lambda: self.move_window(0, self.screen_height() - self.height()))
        self.ui.pushButtonRB.clicked.connect(
            lambda: self.move_window(self.screen_width() - self.width(), self.screen_height() - self.height()))
        self.ui.pushButtonCenter.clicked.connect(self.center_window)

        self.ui.pushButtonMoveCoords.clicked.connect(self.move_to_coordinates)

        self.ui.pushButtonGetData.clicked.connect(self.get_window_info)

        self.old_pos = self.pos()  # отслеживание событий перемещения и изменения размеров
        self.resizeEvent = self.log_resize_event
        self.moveEvent = self.log_move_event


    def move_window(self, x, y):  # функция перемещает окно
        self.move(x, y)  # move - сущ фун

    def center_window(self):  # функция центрирует окно
        screen = QtGui.QGuiApplication.primaryScreen().geometry()
        # .geometry() — возвращает объект QRect, содержащий ширину и высоту экрана
        # Если экран 1920x1080, то screen.width() → 1920, screen.height() → 1080
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)  # move - сущ фун

    def screen_width(self):   # функция возвращает ширину экрана
        return QtGui.QGuiApplication.primaryScreen().geometry().width()

    def screen_height(self):   # функция возвращает высоту экрана
        return QtGui.QGuiApplication.primaryScreen().geometry().height()


    def move_to_coordinates(self):  # функция перемещения окна по координатам из spinBox
        x = self.ui.spinBoxX.value()
        y = self.ui.spinBoxY.value()
        self.move_window(x, y)


    def get_window_info(self):  # функция получения информации о текущем окне
        screen = QtGui.QGuiApplication.primaryScreen()
        geometry = screen.geometry()
        screen_number = QtGui.QGuiApplication.screenAt(self.pos()).name()
        state = {
            "Свернуто": self.isMinimized(),
            "Развернуто": self.isMaximized(),
            "Активно": self.isActiveWindow(),
            "Отображено": self.isVisible(),
        }

        info = (
            f"[{self.current_time()}] Кол-во экранов: {len(QtGui.QGuiApplication.screens())}\n"
            f"Текущее основное окно: {screen.name()}\n"
            f"Разрешение экрана: {geometry.width()}x{geometry.height()}\n"
            f"На каком экране окно находится: {screen_number}\n"
            f"Размеры окна: {self.width()}x{self.height()}\n"
            f"Минимальные размеры окна: {self.minimumWidth()}x{self.minimumHeight()}\n"
            f"Текущее положение: {self.x()}, {self.y()}\n"
            f"Координаты центра окна: {self.x() + self.width() // 2}, {self.y() + self.height() // 2}\n"
            f"Состояние окна: {state}\n"
            "----------------------------------------\n"
        )

        self.ui.plainTextEdit.appendPlainText(info)


    def current_time(self):  # функция для получения текущего времени
        return datetime.now().strftime("%H:%M:%S")


    def log_resize_event(self, event):   # логирование изменения размера окна
        print(f"[{self.current_time()}] Изменён размер окна: {event.size().width()}x{event.size().height()}")

    def log_move_event(self, event):  # логирование перемещения окна
        new_pos = self.pos()
        print(
            f"[{self.current_time()}] Окно перемещено: {self.old_pos.x()},{self.old_pos.y()} → {new_pos.x()},{new_pos.y()}")
        self.old_pos = new_pos

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
