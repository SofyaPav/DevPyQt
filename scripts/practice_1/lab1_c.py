# pyside6-designer
# cd scripts\practice_1\ui
# PySide6-uic lab1_c_form.ui -o lab1_c_form.py


from PySide6 import QtWidgets

from ui.lab1_c_form import Ui_MainWindow


class Window(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)


if __name__ == "__main__":
    app = QtWidgets.QApplication()

    window = Window()
    window.show()

    app.exec()
