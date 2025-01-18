"""
Окно, объединяющее два виджета
"""

import sys
from PySide6 import QtWidgets
from b_systeminfo_widget import SystemInfoWidget
from c_weatherapi_widget import WeatherApiWidget


class MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(SystemInfoWidget())
        layout.addWidget(WeatherApiWidget())
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
