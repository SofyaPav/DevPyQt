import sys
import psutil
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget,
    QTableWidget, QTableWidgetItem, QTabWidget, QComboBox, QPushButton
)
from PySide6.QtCore import QThread, Signal, QTimer

# Фоновый поток для обновления данных
class SystemMonitor(QThread):
    data_updated = Signal(dict)  # Сигнал для передачи данных

    def __init__(self, interval=1):
        super().__init__()
        self.interval = interval * 1000  # Перевод в миллисекунды
        self.running = True

    def run(self):
        while self.running:
            data = {
                "cpu": psutil.cpu_percent(),
                "cores": psutil.cpu_count(logical=True),
                "cpu_name": self.get_cpu_name(),
                "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
                "ram_used": psutil.virtual_memory().percent,
                "disks": self.get_disk_info(),
                "processes": self.get_process_info(),
                "services": self.get_services_info(),
                "tasks": self.get_scheduled_tasks()
            }
            self.data_updated.emit(data)  # Отправляем сигнал с данными
            self.msleep(self.interval)  # Засыпаем

    def get_cpu_name(self):
        """ Получаем название процессора """
        return psutil.cpu_freq().max if hasattr(psutil, 'cpu_freq') else "Unknown"

    def get_disk_info(self):
        """ Информация по дискам """
        return {d.device: psutil.disk_usage(d.mountpoint).percent for d in psutil.disk_partitions()}

    def get_process_info(self):
        """ Список процессов """
        return [(p.info["pid"], p.info["name"], p.info["cpu_percent"], p.info["memory_percent"])
                for p in psutil.process_iter(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])]

    def get_services_info(self):
        """ Список служб (только для Windows) """
        if sys.platform == "win32":
            return [(s.name(), s.status()) for s in psutil.win_service_iter()]
        return [("Не поддерживается", "")]

    def get_scheduled_tasks(self):
        """ Список запланированных задач (Windows) """
        if sys.platform == "win32":
            return [("Планировщик задач не реализован", "")]
        return [("Не поддерживается", "")]

    def stop(self):
        self.running = False
        self.quit()
        self.wait()

# Главное окно
class TaskManager(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Системный монитор")
        self.setGeometry(100, 100, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()

        # Вкладки
        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        # 1 Вкладка: Общие сведения
        self.sys_info_tab = QWidget()
        self.sys_info_layout = QVBoxLayout()
        self.cpu_label = QLabel("CPU: —")
        self.ram_label = QLabel("ОЗУ: —")
        self.disk_label = QLabel("Диски: —")
        self.interval_box = QComboBox()
        self.interval_box.addItems(["1", "5", "10", "30"])
        self.interval_box.currentIndexChanged.connect(self.change_interval)
        self.refresh_button = QPushButton("Обновить")
        self.refresh_button.clicked.connect(self.update_data)

        self.sys_info_layout.addWidget(self.cpu_label)
        self.sys_info_layout.addWidget(self.ram_label)
        self.sys_info_layout.addWidget(self.disk_label)
        self.sys_info_layout.addWidget(QLabel("Интервал обновления (сек):"))
        self.sys_info_layout.addWidget(self.interval_box)
        self.sys_info_layout.addWidget(self.refresh_button)
        self.sys_info_tab.setLayout(self.sys_info_layout)
        self.tabs.addTab(self.sys_info_tab, "Общие сведения")

        # 2Вкладка: Процессы
        self.process_tab = QWidget()
        self.process_layout = QVBoxLayout()
        self.process_table = QTableWidget()
        self.process_table.setColumnCount(4)
        self.process_table.setHorizontalHeaderLabels(["PID", "Имя", "CPU %", "ОЗУ %"])
        self.process_layout.addWidget(self.process_table)
        self.process_tab.setLayout(self.process_layout)
        self.tabs.addTab(self.process_tab, "Процессы")

        # 3Вкладка: Службы
        self.services_tab = QWidget()
        self.services_layout = QVBoxLayout()
        self.services_table = QTableWidget()
        self.services_table.setColumnCount(2)
        self.services_table.setHorizontalHeaderLabels(["Служба", "Статус"])
        self.services_layout.addWidget(self.services_table)
        self.services_tab.setLayout(self.services_layout)
        self.tabs.addTab(self.services_tab, "Службы")

        # 4Вкладка: Запланированные задачи
        self.tasks_tab = QWidget()
        self.tasks_layout = QVBoxLayout()
        self.tasks_table = QTableWidget()
        self.tasks_table.setColumnCount(2)
        self.tasks_table.setHorizontalHeaderLabels(["Задача", "Статус"])
        self.tasks_layout.addWidget(self.tasks_table)
        self.tasks_tab.setLayout(self.tasks_layout)
        self.tabs.addTab(self.tasks_tab, "Запланированные задачи")

        self.central_widget.setLayout(self.layout)

        # Запуск фонового потока
        self.monitor_thread = SystemMonitor()
        self.monitor_thread.data_updated.connect(self.update_ui)
        self.monitor_thread.start()

    def change_interval(self):
        """ Меняем интервал обновления """
        interval = int(self.interval_box.currentText())
        self.monitor_thread.stop()
        self.monitor_thread = SystemMonitor(interval)
        self.monitor_thread.data_updated.connect(self.update_ui)
        self.monitor_thread.start()

    def update_data(self):
        """ Принудительное обновление """
        self.monitor_thread.data_updated.emit({
            "cpu": psutil.cpu_percent(),
            "cores": psutil.cpu_count(logical=True),
            "cpu_name": self.monitor_thread.get_cpu_name(),
            "ram_total": round(psutil.virtual_memory().total / (1024**3), 2),
            "ram_used": psutil.virtual_memory().percent,
            "disks": self.monitor_thread.get_disk_info(),
            "processes": self.monitor_thread.get_process_info(),
            "services": self.monitor_thread.get_services_info(),
            "tasks": self.monitor_thread.get_scheduled_tasks()
        })

    def update_ui(self, data):
        """ Обновляет UI данными """
        self.cpu_label.setText(f"CPU: {data['cpu']}%, Ядер: {data['cores']}, {data['cpu_name']}")
        self.ram_label.setText(f"ОЗУ: {data['ram_used']}% / {data['ram_total']} ГБ")
        self.disk_label.setText(f"Диски: {', '.join([f'{k}: {v}%' for k, v in data['disks'].items()])}")

        self.process_table.setRowCount(0)
        for proc in data["processes"]:
            row = self.process_table.rowCount()
            self.process_table.insertRow(row)
            for col, value in enumerate(proc):
                self.process_table.setItem(row, col, QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.monitor_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TaskManager()
    window.show()
    sys.exit(app.exec())
