"""
Файл для повторения темы сигналов

Напомнить про работу с сигналами и изменением Ui.

Предлагается создать приложение, которое принимает в lineEditInput строку от пользователя,
и при нажатии на pushButtonMirror отображает в lineEditMirror введённую строку в обратном
порядке (задом наперед).
"""

from PySide6 import QtWidgets


class Window(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__initUi()
        self.__initSignals()

    def __initUi(self):
        self.lineEditInput = QtWidgets.QLineEdit()
        # self — ссылка на текущий экземпляр класса Window, а через него создается и привязывается виджет QLineEdit
        # lineEditInput - атрибут класса Window, содержащий экземпляр класса QLineEdit
        # QtWidgets-модуль (пространство имен), содержащий элементы интерфейса
        # QLineEdit - класс внутри модуля QtWidgets
        # ()-вызов конструктора класса QLineEdit, который создает новый экземпляр этого
        #   класса (в данном случае виджет для ввода текста).

        self.lineEditMirror = QtWidgets.QLineEdit()
        # self — ссылка на текущий экземпляр класса Window, а через него создается и привязывается виджет QLineEdit
        # lineEditMirror - атрибут
        # QtWidgets-модуль (пространство имен)
        # QLineEdit() - класс внутри модуля QtWidgets
        # ()-Указывает вызов конструктора класса, что приводит к созданию экземпляра

        self.pushButtonMirror = QtWidgets.QPushButton('Mirror')
        # self — ссылка на текущий экземпляр класса Window, а через него создается и привязывается виджет QPushButton
        # pushButtonMirror - имя атрибута (придумываем

        self.pushButtonClear = QtWidgets.QPushButton('Clear')  # pushButtonClear - атрибут

        h_line = QtWidgets.QHBoxLayout()
        # h_line - локальная переменная, ее значение - экземпляр класса QHBoxLayout
        # QtWidgets-модуль (пространство имен)
        # QHBoxLayout - класс внутри модуля QtWidgets
        # ()-Указывает вызов конструктора класса, что приводит к созданию экземпляра

        h_button = QtWidgets.QHBoxLayout()
        # h_button - локальная переменная, ее значение - экземпляр класса QHBoxLayout (кнопки слева направо)
        # QtWidgets-модуль (пространство имен)
        # QHBoxLayout - класс внутри модуля QtWidgets
        # ()-Указывает вызов конструктора класса, что приводит к созданию экземпляра

        h_line.addWidget(self.lineEditInput)  # "закинули в горизонтальную линию lineEditInput"
        # h_line - локальная переменная, ее значение - экземпляр класса QHBoxLayout (кнопки слева направо)
        # addWidget - метод класса QHBoxLayout
        # lineEditInput - атрибут, созданный мной ранее

        h_line.addWidget(self.lineEditMirror)  # закинули в горизонтальную линию lineEditMirror

        h_button.addWidget(self.pushButtonMirror)  # закинули в горизонтальную кнопку pushButtonMirror
        h_button.addWidget(self.pushButtonClear)  # закинули в горизонтальную кнопку pushButtonClear

        self.widget = QtWidgets.QVBoxLayout()

        self.widget.addLayout(h_line)  # добавляем уже не виджет, а слой
        self.widget.addLayout(h_button)  # добавляем уже не виджет, а слой

        self.setLayout(self.widget)



    def __initSignals(self):
        pass

    def __onPushButtonMirrorClicked(self):
        pass

    def __onPushButtonClearClicked(self):
        pass

    def __onLineEditMirrorTextChanged(self, text):
        print(text)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
