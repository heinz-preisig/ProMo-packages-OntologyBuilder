# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor_typed_token.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(669, 795)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupToken = QtWidgets.QGroupBox(self.centralwidget)
        self.groupToken.setGeometry(QtCore.QRect(30, 40, 161, 171))
        self.groupToken.setObjectName("groupToken")
        self.comboTokenWithTypedTokens = QtWidgets.QComboBox(self.groupToken)
        self.comboTokenWithTypedTokens.setGeometry(QtCore.QRect(40, 30, 85, 27))
        self.comboTokenWithTypedTokens.setObjectName("comboTokenWithTypedTokens")
        self.pushAddTypedToken = QtWidgets.QPushButton(self.groupToken)
        self.pushAddTypedToken.setGeometry(QtCore.QRect(50, 90, 51, 51))
        self.pushAddTypedToken.setText("")
        self.pushAddTypedToken.setObjectName("pushAddTypedToken")
        self.groupConversion = QtWidgets.QGroupBox(self.centralwidget)
        self.groupConversion.setGeometry(QtCore.QRect(210, 10, 431, 731))
        self.groupConversion.setObjectName("groupConversion")
        self.formLayoutWidget = QtWidgets.QWidget(self.groupConversion)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 120, 191, 551))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formReactants = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formReactants.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formReactants.setFieldGrowthPolicy(QtWidgets.QFormLayout.AllNonFixedFieldsGrow)
        self.formReactants.setContentsMargins(0, 0, 0, 0)
        self.formReactants.setObjectName("formReactants")
        self.formLayoutWidget_2 = QtWidgets.QWidget(self.groupConversion)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(230, 120, 191, 551))
        self.formLayoutWidget_2.setObjectName("formLayoutWidget_2")
        self.formProducts = QtWidgets.QFormLayout(self.formLayoutWidget_2)
        self.formProducts.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.formProducts.setContentsMargins(0, 0, 0, 0)
        self.formProducts.setObjectName("formProducts")
        self.pushNewConversion = QtWidgets.QPushButton(self.groupConversion)
        self.pushNewConversion.setGeometry(QtCore.QRect(20, 690, 99, 27))
        self.pushNewConversion.setObjectName("pushNewConversion")
        self.groupConverstonControl = QtWidgets.QGroupBox(self.groupConversion)
        self.groupConverstonControl.setGeometry(QtCore.QRect(10, 19, 411, 81))
        self.groupConverstonControl.setTitle("")
        self.groupConverstonControl.setObjectName("groupConverstonControl")
        self.spinConversion = QtWidgets.QSpinBox(self.groupConverstonControl)
        self.spinConversion.setGeometry(QtCore.QRect(10, 40, 101, 27))
        self.spinConversion.setObjectName("spinConversion")
        self.pushDelete = QtWidgets.QPushButton(self.groupConverstonControl)
        self.pushDelete.setGeometry(QtCore.QRect(120, 40, 91, 27))
        self.pushDelete.setObjectName("pushDelete")
        self.comboConversion = QtWidgets.QComboBox(self.groupConverstonControl)
        self.comboConversion.setGeometry(QtCore.QRect(220, 40, 191, 27))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboConversion.sizePolicy().hasHeightForWidth())
        self.comboConversion.setSizePolicy(sizePolicy)
        self.comboConversion.setObjectName("comboConversion")
        self.pushSave = QtWidgets.QPushButton(self.centralwidget)
        self.pushSave.setGeometry(QtCore.QRect(80, 240, 51, 51))
        self.pushSave.setText("")
        self.pushSave.setObjectName("pushSave")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 669, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.spinConversion.valueChanged['int'].connect(self.comboConversion.setCurrentIndex)
        self.comboConversion.currentIndexChanged['int'].connect(self.spinConversion.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupToken.setTitle(_translate("MainWindow", "token"))
        self.groupConversion.setTitle(_translate("MainWindow", "conversion"))
        self.pushNewConversion.setText(_translate("MainWindow", "new"))
        self.pushDelete.setText(_translate("MainWindow", "delete"))
