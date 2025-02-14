from PySide6 import QtWidgets, QtCore, QtGui
# QtWidgets: Модуль, содержащий виджеты (например, кнопки, слайдеры, окна) и компоненты интерфейса.
# QtCore: Модуль, предоставляющий основные классы, такие как сигналы/слоты, обработка событий, таймеры.
# QtGui: Модуль для управления графическими элементами, такими как шрифты, цвета, события клавиш.

from ui.d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget):
# class Window: Объявляем класс Window, который представляет главное окно приложения.
# QtWidgets.QWidget: Window наследуется от QWidget, базового класса для всех виджетов в PySide6. Он обеспечивает базовый функционал окна




    def __init__(self, parent=None):
        # def __init__: Конструктор класса Window, вызывается при создании экземпляра.
        # self: Ссылка на текущий экземпляр класса.
        # parent=None: Позволяет передать родительский объект (например, другое окно), если нужно.
        super().__init__(parent)
        # super().__init__(parent): Вызывает конструктор родительского класса (QWidget), чтобы инициализировать базовый функционал окна.

        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # Инициализация QSettings для сохранения значений
        self.settings = QtCore.QSettings("MyApp", "EventFilter")

        # Связываем виджеты для взаимодействия
        self.initConnections()
        self.loadSettings()

        # Устанавливаем политику фокуса для dials, чтобы он мог получать клавиши
        self.ui.dial.setFocusPolicy(QtCore.Qt.FocusPolicy.StrongFocus)

    def initConnections(self):
        # Связываем изменение значений между QDial, QSlider и QLCDNumber
        self.ui.dial.valueChanged.connect(self.syncWidgets)
        self.ui.horizontalSlider.valueChanged.connect(self.syncWidgets)

        # Обработчики для клавиш + и - для QDial
        self.ui.dial.installEventFilter(self)

        # Обработчик изменения значения в ComboBox
        self.ui.comboBox.currentIndexChanged.connect(self.updateDisplayFormat)

        # Заполняем ComboBox
        self.ui.comboBox.addItems(["Decimal", "Hexadecimal", "Binary", "Octal"])

    def eventFilter(self, watched: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """
        Реализация обработки нажатий клавиш для изменения значения QDial (+ и -).
        """
        if watched == self.ui.dial and event.type() == QtCore.QEvent.KeyPress:
            if isinstance(event, QtGui.QKeyEvent):
                if event.key() == QtCore.Qt.Key_Plus:  # Клавиша "+"
                    self.ui.dial.setValue(self.ui.dial.value() + 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                elif event.key() == QtCore.Qt.Key_Minus:  # Клавиша "-"
                    self.ui.dial.setValue(self.ui.dial.value() - 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                return True
        return super(Window, self).eventFilter(watched, event)

    def syncWidgets(self):
        """
        Обновляем отображение на LCD, Slider и Dial при изменении значения в одном из виджетов.
        """
        value = self.ui.dial.value()
        self.ui.horizontalSlider.setValue(value)
        self.updateLCDNumber(value)

    def updateLCDNumber(self, value):
        """
        Обновляем отображение на LCDNumber в зависимости от текущего формата.
        """
        selected_format = self.ui.comboBox.currentText()

        if selected_format == "Decimal":
            self.ui.lcdNumber.display(value)
        elif selected_format == "Hexadecimal":
            self.ui.lcdNumber.display(hex(value)[2:].upper())
        elif selected_format == "Binary":
            self.ui.lcdNumber.display(bin(value)[2:])
        elif selected_format == "Octal":
            self.ui.lcdNumber.display(oct(value)[2:])

    def updateDisplayFormat(self):
        """
        Применяем выбранный формат отображения.
        """
        value = self.ui.dial.value()
        self.updateLCDNumber(value)

    def loadSettings(self):
        """
        Загружаем сохраненные настройки из QSettings при запуске приложения.
        """
        display_format = self.settings.value("displayFormat", "Decimal")
        lcd_value = int(self.settings.value("lcdValue", 0))

        # Устанавливаем сохраненные значения
        self.ui.comboBox.setCurrentText(display_format)
        self.ui.dial.setValue(lcd_value)
        self.ui.horizontalSlider.setValue(lcd_value)

        # Применяем формат отображения
        self.updateLCDNumber(lcd_value)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Сохраняем настройки перед закрытием приложения.
        """
        self.settings.setValue("displayFormat", self.ui.comboBox.currentText())
        self.settings.setValue("lcdValue", self.ui.dial.value())


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
