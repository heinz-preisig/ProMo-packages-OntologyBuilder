# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor_typed_token.ui'
#
# Created by: PyQt4 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1015, 537)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.groupToken = QtGui.QGroupBox(self.centralwidget)
        self.groupToken.setGeometry(QtCore.QRect(380, 30, 161, 131))
        self.groupToken.setObjectName(_fromUtf8("groupToken"))
        self.spinNumberOfTypedTokens = QtGui.QSpinBox(self.groupToken)
        self.spinNumberOfTypedTokens.setGeometry(QtCore.QRect(40, 80, 61, 27))
        self.spinNumberOfTypedTokens.setMinimum(1)
        self.spinNumberOfTypedTokens.setObjectName(_fromUtf8("spinNumberOfTypedTokens"))
        self.comboTokenWithTypedTokens = QtGui.QComboBox(self.groupToken)
        self.comboTokenWithTypedTokens.setGeometry(QtCore.QRect(40, 30, 85, 27))
        self.comboTokenWithTypedTokens.setObjectName(_fromUtf8("comboTokenWithTypedTokens"))
        self.groupConversion = QtGui.QGroupBox(self.centralwidget)
        self.groupConversion.setGeometry(QtCore.QRect(560, 20, 431, 481))
        self.groupConversion.setObjectName(_fromUtf8("groupConversion"))
        self.comboConversion = QtGui.QComboBox(self.groupConversion)
        self.comboConversion.setGeometry(QtCore.QRect(230, 60, 191, 27))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboConversion.sizePolicy().hasHeightForWidth())
        self.comboConversion.setSizePolicy(sizePolicy)
        self.comboConversion.setObjectName(_fromUtf8("comboConversion"))
        self.formLayoutWidget = QtGui.QWidget(self.groupConversion)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 110, 191, 281))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formReactants = QtGui.QFormLayout(self.formLayoutWidget)
        self.formReactants.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.formReactants.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formReactants.setMargin(0)
        self.formReactants.setObjectName(_fromUtf8("formReactants"))
        self.formLayoutWidget_2 = QtGui.QWidget(self.groupConversion)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(230, 110, 191, 281))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.formProducts = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.formProducts.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.formProducts.setMargin(0)
        self.formProducts.setObjectName(_fromUtf8("formProducts"))
        self.pushNewConversion = QtGui.QPushButton(self.groupConversion)
        self.pushNewConversion.setGeometry(QtCore.QRect(20, 420, 99, 27))
        self.pushNewConversion.setObjectName(_fromUtf8("pushNewConversion"))
        self.pushDelete = QtGui.QPushButton(self.groupConversion)
        self.pushDelete.setGeometry(QtCore.QRect(160, 420, 99, 27))
        self.pushDelete.setObjectName(_fromUtf8("pushDelete"))
        self.spinConverstion = QtGui.QSpinBox(self.groupConversion)
        self.spinConverstion.setGeometry(QtCore.QRect(20, 60, 101, 27))
        self.spinConverstion.setObjectName(_fromUtf8("spinConverstion"))
        self.groupStart = QtGui.QGroupBox(self.centralwidget)
        self.groupStart.setGeometry(QtCore.QRect(50, 40, 251, 111))
        self.groupStart.setTitle(_fromUtf8(""))
        self.groupStart.setObjectName(_fromUtf8("groupStart"))
        self.pushNewSystem = QtGui.QPushButton(self.groupStart)
        self.pushNewSystem.setGeometry(QtCore.QRect(20, 50, 99, 27))
        self.pushNewSystem.setObjectName(_fromUtf8("pushNewSystem"))
        self.pushLoad = QtGui.QPushButton(self.groupStart)
        self.pushLoad.setGeometry(QtCore.QRect(130, 50, 99, 27))
        self.pushLoad.setObjectName(_fromUtf8("pushLoad"))
        self.groupSaving = QtGui.QGroupBox(self.centralwidget)
        self.groupSaving.setGeometry(QtCore.QRect(60, 190, 251, 71))
        self.groupSaving.setTitle(_fromUtf8(""))
        self.groupSaving.setObjectName(_fromUtf8("groupSaving"))
        self.pushSaveAs = QtGui.QPushButton(self.groupSaving)
        self.pushSaveAs.setGeometry(QtCore.QRect(120, 20, 99, 27))
        self.pushSaveAs.setObjectName(_fromUtf8("pushSaveAs"))
        self.pushSave = QtGui.QPushButton(self.groupSaving)
        self.pushSave.setGeometry(QtCore.QRect(10, 20, 101, 27))
        self.pushSave.setObjectName(_fromUtf8("pushSave"))
        self.message_box = QtGui.QTextBrowser(self.centralwidget)
        self.message_box.setGeometry(QtCore.QRect(50, 310, 491, 161))
        self.message_box.setObjectName(_fromUtf8("message_box"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupToken.setTitle(_translate("MainWindow", "token", None))
        self.groupConversion.setTitle(_translate("MainWindow", "conversion", None))
        self.pushNewConversion.setText(_translate("MainWindow", "new", None))
        self.pushDelete.setText(_translate("MainWindow", "delete", None))
        self.pushNewSystem.setText(_translate("MainWindow", "new", None))
        self.pushLoad.setText(_translate("MainWindow", "load", None))
        self.pushSaveAs.setText(_translate("MainWindow", "save as", None))
        self.pushSave.setText(_translate("MainWindow", "save", None))

