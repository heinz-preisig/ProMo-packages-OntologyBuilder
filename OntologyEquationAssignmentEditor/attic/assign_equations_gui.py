# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assign_equations_gui_v7.ui'
#
# Created by: PyQt5 UI code generator 4.12.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui

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
        MainWindow.resize(1538, 892)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(100, 0))
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtGui.QMainWindow.AllowTabbedDocks|QtGui.QMainWindow.AnimatedDocks|QtGui.QMainWindow.ForceTabbedDocks|QtGui.QMainWindow.VerticalTabs)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 10, 551, 841))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_node = QtGui.QWidget()
        self.tab_node.setObjectName(_fromUtf8("tab_node"))
        self.tableNodes = QtGui.QTableWidget(self.tab_node)
        self.tableNodes.setEnabled(True)
        self.tableNodes.setGeometry(QtCore.QRect(40, 20, 501, 741))
        self.tableNodes.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableNodes.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableNodes.setObjectName(_fromUtf8("tableNodes"))
        self.tableNodes.setColumnCount(5)
        self.tableNodes.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(4, item)
        self.layoutWidget = QtGui.QWidget(self.tab_node)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.comboBoxNodeVariableClasses = QtGui.QComboBox(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxNodeVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxNodeVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxNodeVariableClasses.setObjectName(_fromUtf8("comboBoxNodeVariableClasses"))
        self.horizontalLayout.addWidget(self.comboBoxNodeVariableClasses)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushNodeSave = QtGui.QPushButton(self.layoutWidget)
        self.pushNodeSave.setObjectName(_fromUtf8("pushNodeSave"))
        self.horizontalLayout.addWidget(self.pushNodeSave)
        self.tabWidget.addTab(self.tab_node, _fromUtf8(""))
        self.tab_arc = QtGui.QWidget()
        self.tab_arc.setObjectName(_fromUtf8("tab_arc"))
        self.tableArcs = QtGui.QTableWidget(self.tab_arc)
        self.tableArcs.setGeometry(QtCore.QRect(40, 20, 501, 741))
        self.tableArcs.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableArcs.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableArcs.setObjectName(_fromUtf8("tableArcs"))
        self.tableArcs.setColumnCount(5)
        self.tableArcs.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(4, item)
        self.layoutWidget1 = QtGui.QWidget(self.tab_arc)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setMargin(0)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.comboBoxArcVariableClasses = QtGui.QComboBox(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxArcVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxArcVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxArcVariableClasses.setObjectName(_fromUtf8("comboBoxArcVariableClasses"))
        self.horizontalLayout_2.addWidget(self.comboBoxArcVariableClasses)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushArcSave = QtGui.QPushButton(self.layoutWidget1)
        self.pushArcSave.setObjectName(_fromUtf8("pushArcSave"))
        self.horizontalLayout_2.addWidget(self.pushArcSave)
        self.tabWidget.addTab(self.tab_arc, _fromUtf8(""))
        self.tab_intraface = QtGui.QWidget()
        self.tab_intraface.setObjectName(_fromUtf8("tab_intraface"))
        self.tableIntrafaces = QtGui.QTableWidget(self.tab_intraface)
        self.tableIntrafaces.setEnabled(True)
        self.tableIntrafaces.setGeometry(QtCore.QRect(40, 20, 311, 741))
        self.tableIntrafaces.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableIntrafaces.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableIntrafaces.setObjectName(_fromUtf8("tableIntrafaces"))
        self.tableIntrafaces.setColumnCount(3)
        self.tableIntrafaces.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(2, item)
        self.layoutWidget_2 = QtGui.QWidget(self.tab_intraface)
        self.layoutWidget_2.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.comboBoxIntrafacesVariableClasses = QtGui.QComboBox(self.layoutWidget_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxIntrafacesVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxIntrafacesVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxIntrafacesVariableClasses.setObjectName(_fromUtf8("comboBoxIntrafacesVariableClasses"))
        self.horizontalLayout_3.addWidget(self.comboBoxIntrafacesVariableClasses)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushIntrafaceSave = QtGui.QPushButton(self.layoutWidget_2)
        self.pushIntrafaceSave.setObjectName(_fromUtf8("pushIntrafaceSave"))
        self.horizontalLayout_3.addWidget(self.pushIntrafaceSave)
        self.tabWidget.addTab(self.tab_intraface, _fromUtf8(""))
        self.tab_interface = QtGui.QWidget()
        self.tab_interface.setObjectName(_fromUtf8("tab_interface"))
        self.tableInterfaces = QtGui.QTableWidget(self.tab_interface)
        self.tableInterfaces.setEnabled(True)
        self.tableInterfaces.setGeometry(QtCore.QRect(40, 20, 221, 741))
        self.tableInterfaces.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.tableInterfaces.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tableInterfaces.setObjectName(_fromUtf8("tableInterfaces"))
        self.tableInterfaces.setColumnCount(2)
        self.tableInterfaces.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableInterfaces.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableInterfaces.setHorizontalHeaderItem(1, item)
        self.layoutWidget_3 = QtGui.QWidget(self.tab_interface)
        self.layoutWidget_3.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget_3.setObjectName(_fromUtf8("layoutWidget_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.comboBoxInterfacesVariableClasses = QtGui.QComboBox(self.layoutWidget_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxInterfacesVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxInterfacesVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxInterfacesVariableClasses.setObjectName(_fromUtf8("comboBoxInterfacesVariableClasses"))
        self.horizontalLayout_4.addWidget(self.comboBoxInterfacesVariableClasses)
        spacerItem3 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.pushInterfaceSave = QtGui.QPushButton(self.layoutWidget_3)
        self.pushInterfaceSave.setObjectName(_fromUtf8("pushInterfaceSave"))
        self.horizontalLayout_4.addWidget(self.pushInterfaceSave)
        self.tabWidget.addTab(self.tab_interface, _fromUtf8(""))
        self.groupBoxEquations = QtGui.QGroupBox(self.centralwidget)
        self.groupBoxEquations.setGeometry(QtCore.QRect(600, 10, 911, 841))
        self.groupBoxEquations.setObjectName(_fromUtf8("groupBoxEquations"))
        self.horizontalLayoutWidget_10 = QtGui.QWidget(self.groupBoxEquations)
        self.horizontalLayoutWidget_10.setGeometry(QtCore.QRect(10, 40, 441, 801))
        self.horizontalLayoutWidget_10.setObjectName(_fromUtf8("horizontalLayoutWidget_10"))
        self.horizontalLayoutEquations = QtGui.QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayoutEquations.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.horizontalLayoutEquations.setMargin(0)
        self.horizontalLayoutEquations.setObjectName(_fromUtf8("horizontalLayoutEquations"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Modeller", None))
        item = self.tableNodes.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network", None))
        item = self.tableNodes.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "type", None))
        item = self.tableNodes.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "nature", None))
        item = self.tableNodes.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "token", None))
        item = self.tableNodes.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "edit", None))
        self.pushNodeSave.setText(_translate("MainWindow", "save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_node), _translate("MainWindow", "node", None))
        item = self.tableArcs.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network", None))
        item = self.tableArcs.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "mechanism", None))
        item = self.tableArcs.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "nature", None))
        item = self.tableArcs.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "token", None))
        item = self.tableArcs.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "edit", None))
        self.pushArcSave.setText(_translate("MainWindow", "save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_arc), _translate("MainWindow", "arc", None))
        item = self.tableIntrafaces.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network", None))
        item = self.tableIntrafaces.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "token", None))
        item = self.tableIntrafaces.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "edit", None))
        self.pushIntrafaceSave.setText(_translate("MainWindow", "save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_intraface), _translate("MainWindow", "intraface", None))
        item = self.tableInterfaces.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network", None))
        item = self.tableInterfaces.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "edit", None))
        self.pushInterfaceSave.setText(_translate("MainWindow", "save", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_interface), _translate("MainWindow", "interface", None))
        self.groupBoxEquations.setTitle(_translate("MainWindow", "Equations", None))

