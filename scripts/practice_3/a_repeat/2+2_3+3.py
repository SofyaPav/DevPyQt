import time
from PySide6 import QtCore, QtWidgets


class CalculationThread(QtCore.QThread):
    """
    Поток для выполнения вычислений.
    """
    resultReady = QtCore.Signal(str)  # Сигнал для передачи результата

    def __init__(self, expression: str, parent=None):
        super().__init__(parent)
        self.expression = expression  # Выражение для вычисления

    def run(self) -> None:
        """
        Выполняет вычисление в отдельном потоке.
        """
        time.sleep(1)  # Имитация задержки
        try:
            result = eval(self.expression)  # Выполнение вычисления
            self.resultReady.emit(f"{self.expression} = {result}")  # Отправка результата
        except Exception as e:
            self.resultReady.emit(f"Ошибка: {e}")


class Window(QtWidgets.QWidget):
    """
    Основное окно приложения.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Два потока с вычислениями")
        self.initUi()

    def initUi(self) -> None:
        """
        Создание интерфейса.
        """
        self.layout = QtWidgets.QVBoxLayout(self)

        self.resultArea = QtWidgets.QPlainTextEdit()
        self.resultArea.setReadOnly(True)  # Только для чтения

        self.buttonCalculate2Plus2 = QtWidgets.QPushButton("Посчитать 2 + 2")
        self.buttonCalculate3Plus3 = QtWidgets.QPushButton("Посчитать 3 + 3")

        self.layout.addWidget(self.resultArea)
        self.layout.addWidget(self.buttonCalculate2Plus2)
        self.layout.addWidget(self.buttonCalculate3Plus3)

        self.buttonCalculate2Plus2.clicked.connect(self.startThread2Plus2)
        self.buttonCalculate3Plus3.clicked.connect(self.startThread3Plus3)

    def startThread2Plus2(self):
        """
        Запуск потока для вычисления 2 + 2.
        """
        self.thread2Plus2 = CalculationThread("2 + 2")
        self.thread2Plus2.resultReady.connect(self.showResult)
        self.thread2Plus2.start()

    def startThread3Plus3(self):
        """
        Запуск потока для вычисления 3 + 3.
        """
        self.thread3Plus3 = CalculationThread("3 + 3")
        self.thread3Plus3.resultReady.connect(self.showResult)
        self.thread3Plus3.start()

    def showResult(self, result: str):
        """
        Отображение результата в текстовом поле.
        """
        self.resultArea.appendPlainText(result)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
