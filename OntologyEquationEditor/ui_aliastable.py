# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_aliastable.ui'
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

class Ui_AliasTable(object):
    def setupUi(self, AliasTable):
        AliasTable.setObjectName(_fromUtf8("AliasTable"))
        AliasTable.resize(650, 885)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AliasTable.sizePolicy().hasHeightForWidth())
        AliasTable.setSizePolicy(sizePolicy)
        self.tableWidget = QtGui.QTableWidget(AliasTable)
        self.tableWidget.setGeometry(QtCore.QRect(70, 10, 571, 861))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget.sizePolicy().hasHeightForWidth())
        self.tableWidget.setSizePolicy(sizePolicy)
        self.tableWidget.setSizeIncrement(QtCore.QSize(1, 1))
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.layoutWidget = QtGui.QWidget(AliasTable)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 51, 91))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
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
        self.gridLayout_3.addWidget(self.pushFinished, 0, 0, 1, 1)
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
        self.gridLayout_3.addWidget(self.pushInfo, 1, 0, 1, 1)
        self.gridLayout_3.setRowStretch(0, 50)
        self.gridLayout_3.setRowStretch(1, 50)

        self.retranslateUi(AliasTable)
        QtCore.QMetaObject.connectSlotsByName(AliasTable)

    def retranslateUi(self, AliasTable):
        AliasTable.setWindowTitle(_translate("AliasTable", "Form", None))

