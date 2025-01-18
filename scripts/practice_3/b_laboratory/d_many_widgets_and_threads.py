from PySide6 import QtWidgets
from b_systeminfo_widget import SystemInfoWidget
from c_weatherapi_widget import WeatherApiWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()

    def initUi(self):
        self.system_widget = SystemInfoWidget()
        self.weather_widget = WeatherApiWidget()

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.system_widget)
        layout.addWidget(self.weather_widget)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = MainWindow()
    window.show()

    app.exec()
