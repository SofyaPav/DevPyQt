# Я хочу в pycharm в pyside6 создать кнопку, которая при нажатии на нее будет выполнять функцию 4+4


from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()  # Инициализация пользовательского интерфейса
        self.initSignals()  # Подключение сигналов к слотам

    def initUi(self) -> None:
        """
        Создаем пользовательский интерфейс.
        """
        # Создаем кнопку
        self.button = QtWidgets.QPushButton("Нажми меня")

        # Создаем метку для отображения результата
        self.result_label = QtWidgets.QLabel("Результат будет здесь")

        # Создаем компоновку
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.button)  # Добавляем кнопку
        layout.addWidget(self.result_label)  # Добавляем метку

        # Устанавливаем компоновку для окна
        self.setLayout(layout)
        self.setWindowTitle("Сложение 4 + 4")  # Устанавливаем заголовок окна

    def initSignals(self) -> None:
        """
        Подключаем сигналы к слотам.
        """
        # При нажатии на кнопку вызываем метод calculate
        self.button.clicked.connect(self.calculate)

    def calculate(self):
        """
        Считает 4 + 4 и выводит результат в метку.
        """
        result = 4 + 4
        self.result_label.setText(f"Результат: {result}")


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()