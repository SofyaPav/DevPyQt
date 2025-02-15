import sys
import platform
import psutil
import subprocess
from PySide6 import QtWidgets, QtCore


class SystemMonitor(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Мониторинг системы")
        self.setGeometry(100, 100, 800, 600)

        # Главный макет
        main_layout = QtWidgets.QVBoxLayout()

        # Виджеты информации о системе
        self.cpu_label = QtWidgets.QLabel("Процессор:")
        self.cpu_info = QtWidgets.QLabel("")
        self.cpu_load_label = QtWidgets.QLabel("Загрузка CPU:")
        self.cpu_load = QtWidgets.QLabel("")

        self.ram_label = QtWidgets.QLabel("ОЗУ:")
        self.ram_info = QtWidgets.QLabel("")

        self.disk_label = QtWidgets.QLabel("Диски:")
        self.disk_info = QtWidgets.QTextEdit("")
        self.disk_info.setReadOnly(True)

        # Виджет выбора интервала обновления
        self.interval_label = QtWidgets.QLabel("Частота обновления (сек):")
        self.interval_combo = QtWidgets.QComboBox()
        self.interval_combo.addItems(["1", "5", "10", "30"])
        self.interval_combo.currentIndexChanged.connect(self.change_update_interval)

        # Поля вывода процессов, служб и задач
        self.processes_label = QtWidgets.QLabel("Работающие процессы:")
        self.processes_list = QtWidgets.QTextEdit("")
        self.processes_list.setReadOnly(True)

        self.services_label = QtWidgets.QLabel("Службы:")
        self.services_list = QtWidgets.QTextEdit("")
        self.services_list.setReadOnly(True)

        self.tasks_label = QtWidgets.QLabel("Планировщик задач:")
        self.tasks_list = QtWidgets.QTextEdit("")
        self.tasks_list.setReadOnly(True)

        # Кнопка обновления процессов, служб и задач
        self.update_button = QtWidgets.QPushButton("Обновить данные")
        self.update_button.clicked.connect(self.update_all_data)

        # Добавление виджетов в макет
        main_layout.addWidget(self.cpu_label)
        main_layout.addWidget(self.cpu_info)
        main_layout.addWidget(self.cpu_load_label)
        main_layout.addWidget(self.cpu_load)
        main_layout.addWidget(self.ram_label)
        main_layout.addWidget(self.ram_info)
        main_layout.addWidget(self.disk_label)
        main_layout.addWidget(self.disk_info)
        main_layout.addWidget(self.interval_label)
        main_layout.addWidget(self.interval_combo)
        main_layout.addWidget(self.processes_label)
        main_layout.addWidget(self.processes_list)
        main_layout.addWidget(self.services_label)
        main_layout.addWidget(self.services_list)
        main_layout.addWidget(self.tasks_label)
        main_layout.addWidget(self.tasks_list)
        main_layout.addWidget(self.update_button)

        # Контейнер
        container = QtWidgets.QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Таймер для обновления системных данных
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(1000)  # По умолчанию 1 секунда

        # Запускаем обновление при старте
        self.update_all_data()

    def change_update_interval(self):
        """Изменяет интервал обновления данных"""
        interval = int(self.interval_combo.currentText()) * 1000  # Перевод в миллисекунды
        self.timer.setInterval(interval)

    def update_system_info(self):
        """Обновляет данные о системе"""
        self.cpu_info.setText(f"{platform.processor()}, {psutil.cpu_count(logical=True)} ядер")
        self.cpu_load.setText(f"{psutil.cpu_percent()} %")

        ram = psutil.virtual_memory()
        self.ram_info.setText(f"Всего: {ram.total / (1024 ** 3):.2f} ГБ, Используется: {ram.used / (1024 ** 3):.2f} ГБ")

        disk_text = ""
        for part in psutil.disk_partitions():
            usage = psutil.disk_usage(part.mountpoint)
            disk_text += f"Диск {part.device}: Всего {usage.total / (1024 ** 3):.2f} ГБ, Занято {usage.used / (1024 ** 3):.2f} ГБ\n"
        self.disk_info.setText(disk_text)

    def update_all_data(self):
        """Обновляет процессы, службы и задачи"""
        self.update_processes()
        self.update_services()
        self.update_tasks()

    def update_processes(self):
        """Обновляет список работающих процессов"""
        processes = [p.info["name"] for p in psutil.process_iter(attrs=["name"])]
        self.processes_list.setText("\n".join(processes))

    def update_services(self):
        """Обновляет список служб (только для Windows)"""
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["sc", "query", "type=", "service", "state=", "all"],
                    capture_output=True, text=True, encoding="cp866"
                )
                services = result.stdout.split("\n")
                self.services_list.setText("\n".join(services))
            except Exception as e:
                self.services_list.setText(f"Ошибка: {e}")
        else:
            self.services_list.setText("Доступно только на Windows.")

    def update_tasks(self):
        """Обновляет список запланированных задач (Windows)"""
        if platform.system() == "Windows":
            try:
                result = subprocess.run(
                    ["schtasks"],
                    capture_output=True, text=True, encoding="cp866"
                )
                tasks = result.stdout.split("\n")
                self.tasks_list.setText("\n".join(tasks))
            except Exception as e:
                self.tasks_list.setText(f"Ошибка: {e}")
        else:
            self.tasks_list.setText("Доступно только на Windows.")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = SystemMonitor()
    window.show()
    sys.exit(app.exec())
