# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'd_eventfilter_settings_form.ui'
##
## Created by: Qt User Interface Compiler version 6.7.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QDial, QHBoxLayout,
    QLCDNumber, QSizePolicy, QSlider, QVBoxLayout,
    QWidget)

class Ui_Form(object):
# class Ui_Form -мой класс
# object-сущ класс


    def setupUi(self, Form):
    # def setupUi - мой метод
    # self — ссылка на текущий экземпляр моего класса Ui_Form.
    # Form — мой аргумент (аргумент-переменная, которая получает значение в момент вызова метода)
    # Описание: Настраивает виджеты и их компоновку в пользовательском интерфейсе.

        if not Form.objectName():
            # Form — мой аргумент
            # objectName() - сущ метод сущ класса QWidget (или наслед) который возвращает имя объекта Form.
            # if not Form.objectName() проверка задано ли имя для объекта Form. Если имя пустое (не задано), выполняется следующий блок кода:

            Form.setObjectName(u"Form")
            # Form — мой аргумент
            # setObjectName - сущ метод сущ класса QWidget(или наслед), он задает имя объекту Form. В данном случае имя объекта устанавливается как "Form"

        Form.resize(241, 179)
        # Form — мой аргумент
        # resize() - сущ метод сущ класса QWidget (или наслед), изменяет размер виджета
        # 241 - ширина
        # 179 - высота

        self.verticalLayout_2 = QVBoxLayout(Form)
        # self — ссылка на текущий экземпляр моего класса Ui_Form
        # verticalLayout_2 - мой атрибут моего класса Ui_Form
        # QVBoxLayout - сущ класс (класс для компоновки элементов в вертикальную колонку, один под другим)
        # Form - мой аргумент

        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        # verticalLayout_2 - мой атрибут моего класса Ui_Form - будущий экземпляр сущ класса QVBoxLayout
        # setObjectName — это сущ метод сущ класса QObject, который используется для задания уникального имени объекта.


        self.horizontalLayout = QHBoxLayout()
        # self — ссылка на текущий экземпляр моего класса Ui_Form
        # horizontalLayout - мой атрибут
        # QHBoxLayout - существующий класс

        self.horizontalLayout.setObjectName(u"horizontalLayout")

        self.dial = QDial(Form)
        self.dial.setObjectName(u"dial")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dial.sizePolicy().hasHeightForWidth())
        self.dial.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.dial)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")

        self.comboBox = QComboBox(Form)
        self.comboBox.setObjectName(u"comboBox")

        self.verticalLayout.addWidget(self.comboBox)

        self.lcdNumber = QLCDNumber(Form)
        self.lcdNumber.setObjectName(u"lcdNumber")

        self.verticalLayout.addWidget(self.lcdNumber)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.horizontalSlider = QSlider(Form)
        self.horizontalSlider.setObjectName(u"horizontalSlider")
        self.horizontalSlider.setOrientation(Qt.Horizontal)

        self.verticalLayout_2.addWidget(self.horizontalSlider)


        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"Form", None))
    # retranslateUi

