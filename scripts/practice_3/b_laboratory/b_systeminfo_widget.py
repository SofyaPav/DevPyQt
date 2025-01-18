from PySide6 import QtWidgets
from a_threads import SystemInfo


class SystemInfoWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.initUi()
        self.initThreads()

    def initUi(self):
        self.label_cpu = QtWidgets.QLabel("CPU: 0%")
        self.label_ram = QtWidgets.QLabel("RAM: 0%")
        self.input_delay = QtWidgets.QSpinBox()
        self.input_delay.setRange(1, 10)
        self.input_delay.setValue(1)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(QtWidgets.QLabel("Время задержки:"))
        layout.addWidget(self.input_delay)
        layout.addWidget(self.label_cpu)
        layout.addWidget(self.label_ram)
        self.setLayout(layout)

    def initThreads(self):
        self.system_thread = SystemInfo()
        self.system_thread.systemInfoReceived.connect(self.updateInfo)
        self.system_thread.start()

        self.input_delay.valueChanged.connect(self.setDelay)
        self.setDelay(self.input_delay.value())

    def setDelay(self, value):
        self.system_thread.delay = value

    def updateInfo(self, data):
        cpu, ram = data
        self.label_cpu.setText(f"CPU: {cpu}%")
        self.label_ram.setText(f"RAM: {ram}%")
