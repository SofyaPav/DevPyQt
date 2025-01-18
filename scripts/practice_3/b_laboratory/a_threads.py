"""
Модуль в котором содержаться потоки Qt
"""

import time
import psutil  # pip install psutil
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)  # Сигнал для передачи данных [CPU, RAM]

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # Атрибут для управления задержкой получения данных

    def run(self) -> None:
        if self.delay is None:  # Если задержка не передана
            self.delay = 1  # Устанавливаем значение по умолчанию

        while True:  # Бесконечный цикл получения информации
            cpu_value = psutil.cpu_percent()  # Получаем загрузку CPU
            ram_value = psutil.virtual_memory().percent  # Получаем загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # Передаем данные через сигнал
            time.sleep(self.delay)  # Задержка


class WeatherHandler(QtCore.QThread):
    weatherDataReceived = QtCore.Signal(dict)  # Сигнал для передачи данных о погоде
    weatherErrorOccurred = QtCore.Signal(str)  # Сигнал для передачи ошибок

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)

        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = True  # Устанавливаем статус потока

    def setDelay(self, delay) -> None:
        """
        Метод для установки времени задержки обновления сайта
        """
        self.__delay = delay

    def run(self) -> None:
        while self.__status:
            try:
                response = requests.get(self.__api_url)
                response.raise_for_status()  # Проверяем успешность запроса
                data = response.json()
                self.weatherDataReceived.emit(data)  # Передаем данные через сигнал
            except Exception as e:
                self.weatherErrorOccurred.emit(str(e))  # Передаем ошибку
            time.sleep(self.__delay)  # Задержка
