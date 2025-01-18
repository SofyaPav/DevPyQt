from PySide6 import QtWidgets
from a_threads import WeatherHandler


class WeatherApiWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()

    def initUi(self):
        self.input_lat = QtWidgets.QLineEdit()
        self.input_lat.setPlaceholderText("Введите широту")
        self.input_lon = QtWidgets.QLineEdit()
        self.input_lon.setPlaceholderText("Введите долготу")
        self.input_delay = QtWidgets.QSpinBox()
        self.input_delay.setRange(1, 60)
        self.input_delay.setValue(10)

        self.button_toggle = QtWidgets.QPushButton("Запустить")
        self.text_weather = QtWidgets.QPlainTextEdit()
        self.text_weather.setReadOnly(True)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Широта:"))
        layout.addWidget(self.input_lat)
        layout.addWidget(QtWidgets.QLabel("Долгота:"))
        layout.addWidget(self.input_lon)
        layout.addWidget(QtWidgets.QLabel("Время задержки:"))
        layout.addWidget(self.input_delay)
        layout.addWidget(self.button_toggle)
        layout.addWidget(self.text_weather)
        self.setLayout(layout)

        self.button_toggle.clicked.connect(self.toggleThread)

    def initThreads(self):
        self.weather_thread = None

    def toggleThread(self):
        if self.weather_thread is None:
            try:
                lat = float(self.input_lat.text())
                lon = float(self.input_lon.text())
            except ValueError:
                self.text_weather.setPlainText("Введите корректные координаты!")
                return

            self.weather_thread = WeatherHandler(lat, lon)
            self.weather_thread.weatherDataReceived.connect(self.updateWeather)
            self.weather_thread.weatherErrorOccurred.connect(self.displayError)
            self.weather_thread.setDelay(self.input_delay.value())
            self.weather_thread.startUpdating()

            self.input_lat.setEnabled(False)
            self.input_lon.setEnabled(False)
            self.input_delay.setEnabled(False)
            self.button_toggle.setText("Остановить")
        else:
            self.weather_thread.stopUpdating()
            self.weather_thread = None

            self.input_lat.setEnabled(True)
            self.input_lon.setEnabled(True)
            self.input_delay.setEnabled(True)
            self.button_toggle.setText("Запустить")

    def updateWeather(self, data):
        self.text_weather.setPlainText(str(data))

    def displayError(self, error):
        self.text_weather.setPlainText(f"Ошибка: {error}")
