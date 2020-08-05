# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_variabletable.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(883, 282)
        Dialog.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.tableVariable = QtGui.QTableWidget(Dialog)
        self.tableVariable.setGeometry(QtCore.QRect(70, 10, 801, 261))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.tableVariable.sizePolicy().hasHeightForWidth())
        self.tableVariable.setSizePolicy(sizePolicy)
        self.tableVariable.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.tableVariable.setFont(font)
        self.tableVariable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.tableVariable.setTabKeyNavigation(False)
        self.tableVariable.setProperty("showDropIndicator", False)
        self.tableVariable.setDragDropOverwriteMode(False)
        self.tableVariable.setObjectName(_fromUtf8("tableVariable"))
        self.tableVariable.setColumnCount(8)
        self.tableVariable.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tableVariable.setHorizontalHeaderItem(7, item)
        self.layoutWidget = QtGui.QWidget(Dialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 51, 91))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushFinished = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushFinished.sizePolicy().hasHeightForWidth())
        self.pushFinished.setSizePolicy(sizePolicy)
        self.pushFinished.setMinimumSize(QtCore.QSize(40, 40))
        self.pushFinished.setMaximumSize(QtCore.QSize(40, 40))
        self.pushFinished.setText(_fromUtf8(""))
        self.pushFinished.setObjectName(_fromUtf8("pushFinished"))
        self.gridLayout.addWidget(self.pushFinished, 0, 0, 1, 1)
        self.pushInfo = QtGui.QPushButton(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(40)
        sizePolicy.setVerticalStretch(40)
        sizePolicy.setHeightForWidth(self.pushInfo.sizePolicy().hasHeightForWidth())
        self.pushInfo.setSizePolicy(sizePolicy)
        self.pushInfo.setMinimumSize(QtCore.QSize(40, 40))
        self.pushInfo.setMaximumSize(QtCore.QSize(40, 40))
        self.pushInfo.setText(_fromUtf8(""))
        self.pushInfo.setObjectName(_fromUtf8("pushInfo"))
        self.gridLayout.addWidget(self.pushInfo, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 50)
        self.gridLayout.setRowStretch(1, 50)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        Dialog.setToolTip(_translate("Dialog", "see info button", None))
        self.tableVariable.setToolTip(_translate("Dialog", "variable list", None))
        self.tableVariable.setSortingEnabled(False)
        item = self.tableVariable.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "type", None))
        item.setWhatsThis(_translate("Dialog", "click for new variable", None))
        item = self.tableVariable.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "symbol", None))
        item.setWhatsThis(_translate("Dialog", "click for rename", None))
        item = self.tableVariable.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "description", None))
        item = self.tableVariable.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "units", None))
        item = self.tableVariable.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "indices", None))
        item = self.tableVariable.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "eqs", None))
        item = self.tableVariable.horizontalHeaderItem(6)
        item.setText(_translate("Dialog", "del", None))
        item = self.tableVariable.horizontalHeaderItem(7)
        item.setText(_translate("Dialog", "network", None))

