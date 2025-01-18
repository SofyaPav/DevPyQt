import time
import psutil
from PySide6 import QtCore
import requests


class SystemInfo(QtCore.QThread):
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # Задержка выполнения

    def run(self) -> None:
        if self.delay is None:
            self.delay = 1  # Установка стандартной задержки, если она не задана

        while True:
            cpu_value = psutil.cpu_percent()
            ram_value = psutil.virtual_memory().percent
            self.systemInfoReceived.emit([cpu_value, ram_value])  # Передача данных о загрузке
            time.sleep(self.delay)


class WeatherHandler(QtCore.QThread):
    weatherDataReceived = QtCore.Signal(dict)
    weatherErrorOccurred = QtCore.Signal(str)

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10
        self.__status = False

    def setDelay(self, delay) -> None:
        self.__delay = delay

    def startUpdating(self):
        self.__status = True
        self.start()

    def stopUpdating(self):
        self.__status = False

    def run(self) -> None:
        while self.__status:
            try:
                response = requests.get(self.__api_url)
                response.raise_for_status()
                data = response.json()
                self.weatherDataReceived.emit(data)
            except requests.RequestException as e:
                self.weatherErrorOccurred.emit(str(e))
            time.sleep(self.__delay)
