import time
import psutil
from PySide6 import QtCore


class SystemInfo(QtCore.QThread):
    # Создаем сигнал, который передаст данные в формате списка [CPU, RAM]
    systemInfoReceived = QtCore.Signal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.delay = None  # Атрибут для управления задержкой получения данных

    def run(self) -> None:
        if self.delay is None:  # Если задержка не передана, устанавливаем значение по умолчанию
            self.delay = 1

        while True:  # Запускаем бесконечный цикл
            cpu_value = psutil.cpu_percent(interval=0.1)  # Получаем загрузку CPU
            ram_value = psutil.virtual_memory().percent  # Получаем загрузку RAM
            self.systemInfoReceived.emit([cpu_value, ram_value])  # Отправляем данные через сигнал
            time.sleep(self.delay)  # Задержка между итерациями


class WeatherHandler(QtCore.QThread):
    # Создаем сигналы
    weatherDataReceived = QtCore.Signal(dict)  # Сигнал для передачи данных о погоде
    weatherErrorOccurred = QtCore.Signal(str)  # Сигнал для передачи ошибок

    def __init__(self, lat, lon, parent=None):
        super().__init__(parent)
        self.__api_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
        self.__delay = 10  # Задержка между запросами
        self.__status = True  # Статус потока, по умолчанию поток активен

    def setDelay(self, delay) -> None:
        """
        Установка времени задержки между запросами.
        """
        self.__delay = delay

    def stop(self) -> None:
        """
        Остановка потока.
        """
        self.__status = False

    def run(self) -> None:
        while self.__status:  # Пока поток активен
            try:
                response = requests.get(self.__api_url)  # Выполняем запрос к API
                response.raise_for_status()  # Проверяем, успешен ли запрос
                data = response.json()  # Преобразуем ответ в JSON
                self.weatherDataReceived.emit(data)  # Отправляем данные через сигнал
            except Exception as e:  # Обрабатываем исключения
                self.weatherErrorOccurred.emit(str(e))  # Передаем ошибку через сигнал

            time.sleep(self.__delay)  # Задержка между запросами
