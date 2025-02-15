import platform  # Для получения информации о процессоре
from PySide6 import QtWidgets  # модуль из библиотеки PySide6, который содержит классы для работы с виджетами,
# такими как окна, кнопки, текстовые поля и т.д
from ui.try_1_3 import Ui_MainWindow  # импортируемый класс, который сгенерирован Qt Designer для интерфейса приложения


class Window(QtWidgets.QMainWindow):  # Создаем класс Window, который наследуется от QtWidgets.QMainWindow,
    # что позволяет нам создавать главное окно приложения
    def __init__(self, parent=None):
        super().__init__(parent)  # super().__init__(parent) — вызывает конструктор родительского класса (QMainWindow),
        # чтобы инициализировать все функции и методы, которые присущи основному окну

        self.ui = Ui_MainWindow()  # В конструкторе (методе __init__) мы создаем экземпляр класса Ui_MainWindow,
        # который содержит описание интерфейса, созданного с помощью Qt Designer.
        self.ui.setupUi(self)  # Мы также вызываем метод setupUi(self), который "настраивает" интерфейс для этого окна

        self.ui.pushButton.clicked.connect(self.get_cpu_name) # подключаем кнопку pushButton (созданную в Qt Designer)
        # к методу get_cpu_name. Это означает, что когда пользователь нажмет на кнопку, вызовется метод get_cpu_name()

    def get_cpu_name(self):
        cpu_name = platform.processor()  # вызываем метод get_cpu_info, который возвращает информацию о процессоре
        self.ui.lineEdit.setText(cpu_name)  # вставляем эту информацию в lineEdit (текстовое поле)


if __name__ == "__main__":
    app = QtWidgets.QApplication()  # Создание объекта приложения

    window = Window()  # Создание экземпляра окна
    window.show()  # Отображение окна

    app.exec()  # Запуск главного цикла событий