'''
"""
Файл для повторения темы QThread

Напомнить про работу с QThread.

Предлагается создать небольшое приложение, которое будет с помощью модуля request
получать доступность того или иного сайта (возвращать из потока status_code сайта).

Поработать с сигналами, которые возникают при запуске/остановке потока,
передать данные в поток (в данном случае url),
получить данные из потока (статус код сайта),
попробовать управлять потоком (запуск, остановка).

Опционально поработать с валидацией url
"""

from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
'''

"""
Файл для повторения темы QThread

Напомнить про работу с QThread.

Предлагается создать небольшое приложение, которое будет с помощью модуля request
получать доступность того или иного сайта (возвращать из потока status_code сайта).

Поработать с сигналами, которые возникают при запуске/остановке потока,
передать данные в поток (в данном случае url),
получить данные из потока (статус код сайта),
попробовать управлять потоком (запуск, остановка).

Опционально поработать с валидацией url
"""
# pip install -r /path/to/requirements.txt
# pip install -r requirements.txt

from PySide6 import QtWidgets, QtCore
import requests  # pip install requests
import time


class WebCheck(QtCore.QThread):
    result = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.__url = None

    def setUrl(self, url):
        self.__url = url

    def run(self):
        self.started.emit()

        try:
            response = requests.get(self.__url)
            status_code = response.status_code
            time.sleep(2)
            self.result.emit(int(status_code))
        except Exception:
            self.result.emit(-1)
        self.finished.emit()


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Проверка доступности")

        layout = QtWidgets.QVBoxLayout(self)

        self.url_edit = QtWidgets.QLineEdit()
        self.check_button = QtWidgets.QPushButton("Проверить")
        self.check_button.clicked.connect(self.check_website)

        self.label = QtWidgets.QLabel()

        layout.addWidget(self.url_edit)
        layout.addWidget(self.check_button)
        layout.addWidget(self.label)

        self.check_thread = WebCheck()

        self.check_thread.started.connect(self.check_started)
        self.check_thread.result.connect(self.update_result)
        self.check_thread.finished.connect(self.check_finished)

    def check_started(self):
        self.label.setText("Проверка...")

    def check_finished(self):
        # self.label.setText("Проверка окончена")
        self.check_button.setEnabled(True)

    def update_result(self, data):
        if data == -1:
            self.label.setText("Произошла ошибка")
        else:
            self.label.setText(f"Статус код: {data}")

    def check_website(self):
        url = self.url_edit.text()
        self.check_thread.setUrl(url)
        self.check_thread.start()
        self.check_button.setEnabled(False)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
