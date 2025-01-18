"""
Виджет для работы с потоком WeatherHandler
"""

import sys
from PySide6 import QtWidgets
from a_threads import WeatherHandler


class WeatherApiWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()
        self.initSignals()

    def initUi(self) -> None:
        self.latInput = QtWidgets.QLineEdit()  # Поле для ввода широты
        self.latInput.setPlaceholderText("Широта")

        self.lonInput = QtWidgets.QLineEdit()  # Поле для ввода долготы
        self.lonInput.setPlaceholderText("Долгота")

        self.delayInput = QtWidgets.QSpinBox()  # Поле для ввода времени задержки
        self.delayInput.setRange(1, 60)
        self.delayInput.setValue(10)

        self.weatherOutput = QtWidgets.QPlainTextEdit()  # Поле для вывода погоды
        self.weatherOutput.setReadOnly(True)

        self.startStopButton = QtWidgets.QPushButton("Запустить")  # Кнопка запуска/остановки

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.latInput)
        layout.addWidget(self.lonInput)
        layout.addWidget(QtWidgets.QLabel("Задержка (сек):"))
        layout.addWidget(self.delayInput)
        layout.addWidget(self.weatherOutput)
        layout.addWidget(self.startStopButton)
        self.setLayout(layout)

    def initThreads(self) -> None:
        self.weatherThread = None

    def initSignals(self) -> None:
        self.startStopButton.clicked.connect(self.toggleWeatherThread)

    def toggleWeatherThread(self) -> None:
        if self.weatherThread is None:  # Если поток еще не запущен
            lat = self.latInput.text()
            lon = self.lonInput.text()
            if not lat or not lon:
                self.weatherOutput.setPlainText("Введите координаты!")
                return

            self.weatherThread = WeatherHandler(lat, lon)
            self.weatherThread.weatherDataReceived.connect(self.displayWeatherData)
            self.weatherThread.weatherErrorOccurred.connect(self.displayError)
            self.weatherThread.start()

            self.latInput.setEnabled(False)
            self.lonInput.setEnabled(False)
            self.delayInput.setEnabled(False)
            self.startStopButton.setText("Остановить")
        else:  # Останавливаем поток
            self.weatherThread.__status = False
            self.weatherThread = None

            self.latInput.setEnabled(True)
            self.lonInput.setEnabled(True)
            self.delayInput.setEnabled(True)
            self.startStopButton.setText("Запустить")

    def displayWeatherData(self, data: dict) -> None:
        self.weatherOutput.setPlainText(str(data))

    def displayError(self, error: str) -> None:
        self.weatherOutput.setPlainText(f"Ошибка: {error}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = WeatherApiWidget()
    window.show()
    sys.exit(app.exec())

