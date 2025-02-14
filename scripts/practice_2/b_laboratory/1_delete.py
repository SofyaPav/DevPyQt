from PySide6 import QtWidgets, QtCore, QtGui
from ui.d_eventfilter_settings_form import Ui_Form


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
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
        self.ui.dial.valueChanged.connect(self.updateLCDNumber)
        self.ui.horizontalSlider.valueChanged.connect(self.updateLCDNumber)
        self.ui.lcdNumber.display(0)  # Устанавливаем начальное значение LCDNumber

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
            # Проверяем, является ли событие событием от клавиши
            if isinstance(event, QtGui.QKeyEvent):
                # Получаем код клавиши
                if event.key() == QtCore.Qt.Key_Plus:  # Клавиша "+"
                    self.ui.dial.setValue(self.ui.dial.value() + 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                elif event.key() == QtCore.Qt.Key_Minus:  # Клавиша "-"
                    self.ui.dial.setValue(self.ui.dial.value() - 1)
                    print(f"Dial value: {self.ui.dial.value()}")
                return True  # Событие обработано
        return super(Window, self).eventFilter(watched, event)

    def updateLCDNumber(self):
        """
        Обновляем отображение на LCD и Slider при изменении значения в одном из виджетов.
        """
        value = self.ui.dial.value()  # Получаем значение из QDial
        self.ui.lcdNumber.display(value)  # Обновляем LCDNumber
        self.ui.horizontalSlider.setValue(value)  # Обновляем значение у Slider

    def updateSliderAndDial(self):
        """
        Обновляем значения Slider и Dial, когда меняется значение LCDNumber.
        """
        value = self.ui.lcdNumber.intValue()  # Используем intValue для получения значения
        self.ui.dial.setValue(value)
        self.ui.horizontalSlider.setValue(value)

    def updateDisplayFormat(self):
        """
        Обновляем формат отображения в зависимости от выбранного значения в ComboBox.
        """
        selected_format = self.ui.comboBox.currentText()

        value = self.ui.lcdNumber.intValue()  # Используем intValue для получения значения

        if selected_format == "Decimal":
            self.ui.lcdNumber.display(value)  # Отображаем как десятичное
        elif selected_format == "Hexadecimal":
            # Преобразуем в строку и убираем префикс '0x'
            self.ui.lcdNumber.display(hex(value)[2:])
        elif selected_format == "Binary":
            # Преобразуем в строку и убираем префикс '0b'
            self.ui.lcdNumber.display(bin(value)[2:])
        elif selected_format == "Octal":
            # Преобразуем в строку и убираем префикс '0o'
            self.ui.lcdNumber.display(oct(value)[2:])

    def loadSettings(self):
        """
        Загружаем сохраненные настройки из QSettings при запуске приложения.
        """
        display_format = self.settings.value("displayFormat", "Decimal")
        lcd_value = self.settings.value("lcdValue", 0)

        # Устанавливаем сохраненные значения
        self.ui.comboBox.setCurrentText(display_format)
        self.ui.lcdNumber.display(lcd_value)

        # Применяем формат отображения
        self.updateDisplayFormat()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        """
        Сохраняем настройки перед закрытием приложения.
        """
        self.settings.setValue("displayFormat", self.ui.comboBox.currentText())
        self.settings.setValue("lcdValue", self.ui.lcdNumber.intValue())  # Используем intValue()

if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
