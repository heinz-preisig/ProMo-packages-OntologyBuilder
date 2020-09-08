# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_variabletable.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1143, 285)
        Dialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.tableVariable = QtWidgets.QTableWidget(Dialog)
        self.tableVariable.setGeometry(QtCore.QRect(210, 10, 801, 261))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.tableVariable.sizePolicy().hasHeightForWidth())
        self.tableVariable.setSizePolicy(sizePolicy)
        self.tableVariable.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableVariable.setFont(font)
        self.tableVariable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableVariable.setTabKeyNavigation(False)
        self.tableVariable.setProperty("showDropIndicator", False)
        self.tableVariable.setDragDropOverwriteMode(False)
        self.tableVariable.setObjectName("tableVariable")
        self.tableVariable.setColumnCount(8)
        self.tableVariable.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(7, item)
        self.layoutWidget = QtWidgets.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(11, 11, 180, 42))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushFinished = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFinished.sizePolicy().hasHeightForWidth())
        self.pushFinished.setSizePolicy(sizePolicy)
        self.pushFinished.setMinimumSize(QtCore.QSize(40, 40))
        self.pushFinished.setMaximumSize(QtCore.QSize(40, 40))
        self.pushFinished.setText("")
        self.pushFinished.setObjectName("pushFinished")
        self.horizontalLayout.addWidget(self.pushFinished)
        self.pushInfo = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.pushInfo.sizePolicy().hasHeightForWidth())
        self.pushInfo.setSizePolicy(sizePolicy)
        self.pushInfo.setMinimumSize(QtCore.QSize(40, 40))
        self.pushInfo.setMaximumSize(QtCore.QSize(40, 40))
        self.pushInfo.setText("")
        self.pushInfo.setObjectName("pushInfo")
        self.horizontalLayout.addWidget(self.pushInfo)
        self.pushNew = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.pushNew.sizePolicy().hasHeightForWidth())
        self.pushNew.setSizePolicy(sizePolicy)
        self.pushNew.setMinimumSize(QtCore.QSize(40, 40))
        self.pushNew.setMaximumSize(QtCore.QSize(40, 40))
        self.pushNew.setText("")
        self.pushNew.setObjectName("pushNew")
        self.horizontalLayout.addWidget(self.pushNew)
        self.pushPort = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.pushPort.sizePolicy().hasHeightForWidth())
        self.pushPort.setSizePolicy(sizePolicy)
        self.pushPort.setMinimumSize(QtCore.QSize(40, 40))
        self.pushPort.setMaximumSize(QtCore.QSize(40, 40))
        self.pushPort.setText("")
        self.pushPort.setObjectName("pushPort")
        self.horizontalLayout.addWidget(self.pushPort)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        Dialog.setToolTip(_translate("Dialog", "see info button"))
        self.tableVariable.setToolTip(_translate("Dialog", "variable list"))
        self.tableVariable.setSortingEnabled(False)
        item = self.tableVariable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "type"))
        item.setWhatsThis(_translate("Dialog", "click to shift variable type"))
        item = self.tableVariable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "symbol"))
        item.setWhatsThis(_translate("Dialog", "click for rename"))
        item = self.tableVariable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "description"))
        item = self.tableVariable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "units"))
        item = self.tableVariable.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "indices"))
        item = self.tableVariable.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "eqs"))
        item = self.tableVariable.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "del"))
        item = self.tableVariable.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "network"))
