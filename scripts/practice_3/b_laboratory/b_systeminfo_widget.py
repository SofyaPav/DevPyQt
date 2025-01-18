"""
Виджет для работы с потоком SystemInfo
"""

import sys
from PySide6 import QtWidgets
from a_threads import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()
        self.initSignals()

    def initUi(self) -> None:
        self.delayInput = QtWidgets.QSpinBox()  # Поле для ввода времени задержки
        self.delayInput.setRange(1, 10)
        self.delayInput.setValue(1)

        self.cpuLabel = QtWidgets.QLabel("CPU: 0%")  # Поле для вывода информации о CPU
        self.ramLabel = QtWidgets.QLabel("RAM: 0%")  # Поле для вывода информации о RAM

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Задержка (сек):"))
        layout.addWidget(self.delayInput)
        layout.addWidget(self.cpuLabel)
        layout.addWidget(self.ramLabel)
        self.setLayout(layout)

    def initThreads(self) -> None:
        self.systemInfoThread = SystemInfo()  # Создаем поток
        self.systemInfoThread.delay = self.delayInput.value()
        self.systemInfoThread.start()

    def initSignals(self) -> None:
        self.delayInput.valueChanged.connect(self.updateDelay)  # Обновляем задержку
        self.systemInfoThread.systemInfoReceived.connect(self.updateSystemInfo)

    def updateDelay(self, value: int) -> None:
        self.systemInfoThread.delay = value  # Обновляем задержку в потоке

    def updateSystemInfo(self, data: list) -> None:
        cpu, ram = data
        self.cpuLabel.setText(f"CPU: {cpu}%")
        self.ramLabel.setText(f"RAM: {ram}%")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SystemInfoWidget()
    window.show()
    sys.exit(app.exec())
