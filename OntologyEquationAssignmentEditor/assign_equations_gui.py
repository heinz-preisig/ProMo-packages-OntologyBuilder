# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'assign_equations_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore
from PyQt5 import QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1538, 892)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(100, 0))
        MainWindow.setDockNestingEnabled(False)
        MainWindow.setDockOptions(QtWidgets.QMainWindow.AllowTabbedDocks|QtWidgets.QMainWindow.AnimatedDocks|QtWidgets.QMainWindow.ForceTabbedDocks|QtWidgets.QMainWindow.VerticalTabs)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 10, 551, 841))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_node = QtWidgets.QWidget()
        self.tab_node.setObjectName("tab_node")
        self.tableNodes = QtWidgets.QTableWidget(self.tab_node)
        self.tableNodes.setEnabled(True)
        self.tableNodes.setGeometry(QtCore.QRect(40, 20, 501, 741))
        self.tableNodes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableNodes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableNodes.setObjectName("tableNodes")
        self.tableNodes.setColumnCount(5)
        self.tableNodes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableNodes.setHorizontalHeaderItem(4, item)
        self.layoutWidget = QtWidgets.QWidget(self.tab_node)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxNodeVariableClasses = QtWidgets.QComboBox(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxNodeVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxNodeVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxNodeVariableClasses.setObjectName("comboBoxNodeVariableClasses")
        self.horizontalLayout.addWidget(self.comboBoxNodeVariableClasses)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushNodeSave = QtWidgets.QPushButton(self.layoutWidget)
        self.pushNodeSave.setObjectName("pushNodeSave")
        self.horizontalLayout.addWidget(self.pushNodeSave)
        self.tabWidget.addTab(self.tab_node, "")
        self.tab_arc = QtWidgets.QWidget()
        self.tab_arc.setObjectName("tab_arc")
        self.tableArcs = QtWidgets.QTableWidget(self.tab_arc)
        self.tableArcs.setGeometry(QtCore.QRect(40, 20, 501, 741))
        self.tableArcs.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableArcs.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableArcs.setObjectName("tableArcs")
        self.tableArcs.setColumnCount(5)
        self.tableArcs.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableArcs.setHorizontalHeaderItem(4, item)
        self.layoutWidget1 = QtWidgets.QWidget(self.tab_arc)
        self.layoutWidget1.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.comboBoxArcVariableClasses = QtWidgets.QComboBox(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxArcVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxArcVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxArcVariableClasses.setObjectName("comboBoxArcVariableClasses")
        self.horizontalLayout_2.addWidget(self.comboBoxArcVariableClasses)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushArcSave = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushArcSave.setObjectName("pushArcSave")
        self.horizontalLayout_2.addWidget(self.pushArcSave)
        self.tabWidget.addTab(self.tab_arc, "")
        self.tab_intraface = QtWidgets.QWidget()
        self.tab_intraface.setObjectName("tab_intraface")
        self.tableIntrafaces = QtWidgets.QTableWidget(self.tab_intraface)
        self.tableIntrafaces.setEnabled(True)
        self.tableIntrafaces.setGeometry(QtCore.QRect(40, 20, 311, 741))
        self.tableIntrafaces.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableIntrafaces.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableIntrafaces.setObjectName("tableIntrafaces")
        self.tableIntrafaces.setColumnCount(3)
        self.tableIntrafaces.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableIntrafaces.setHorizontalHeaderItem(2, item)
        self.layoutWidget_2 = QtWidgets.QWidget(self.tab_intraface)
        self.layoutWidget_2.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.comboBoxIntrafacesVariableClasses = QtWidgets.QComboBox(self.layoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxIntrafacesVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxIntrafacesVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxIntrafacesVariableClasses.setObjectName("comboBoxIntrafacesVariableClasses")
        self.horizontalLayout_3.addWidget(self.comboBoxIntrafacesVariableClasses)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.pushIntrafaceSave = QtWidgets.QPushButton(self.layoutWidget_2)
        self.pushIntrafaceSave.setObjectName("pushIntrafaceSave")
        self.horizontalLayout_3.addWidget(self.pushIntrafaceSave)
        self.tabWidget.addTab(self.tab_intraface, "")
        self.tab_interface = QtWidgets.QWidget()
        self.tab_interface.setObjectName("tab_interface")
        self.tableInterfaces = QtWidgets.QTableWidget(self.tab_interface)
        self.tableInterfaces.setEnabled(True)
        self.tableInterfaces.setGeometry(QtCore.QRect(40, 20, 221, 741))
        self.tableInterfaces.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableInterfaces.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableInterfaces.setObjectName("tableInterfaces")
        self.tableInterfaces.setColumnCount(2)
        self.tableInterfaces.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableInterfaces.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.tableInterfaces.setHorizontalHeaderItem(1, item)
        self.layoutWidget_3 = QtWidgets.QWidget(self.tab_interface)
        self.layoutWidget_3.setGeometry(QtCore.QRect(40, 770, 501, 29))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget_3)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.comboBoxInterfacesVariableClasses = QtWidgets.QComboBox(self.layoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBoxInterfacesVariableClasses.sizePolicy().hasHeightForWidth())
        self.comboBoxInterfacesVariableClasses.setSizePolicy(sizePolicy)
        self.comboBoxInterfacesVariableClasses.setObjectName("comboBoxInterfacesVariableClasses")
        self.horizontalLayout_4.addWidget(self.comboBoxInterfacesVariableClasses)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.pushInterfaceSave = QtWidgets.QPushButton(self.layoutWidget_3)
        self.pushInterfaceSave.setObjectName("pushInterfaceSave")
        self.horizontalLayout_4.addWidget(self.pushInterfaceSave)
        self.tabWidget.addTab(self.tab_interface, "")
        self.groupBoxEquations = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxEquations.setGeometry(QtCore.QRect(600, 10, 911, 841))
        self.groupBoxEquations.setObjectName("groupBoxEquations")
        self.horizontalLayoutWidget_10 = QtWidgets.QWidget(self.groupBoxEquations)
        self.horizontalLayoutWidget_10.setGeometry(QtCore.QRect(10, 40, 441, 801))
        self.horizontalLayoutWidget_10.setObjectName("horizontalLayoutWidget_10")
        self.horizontalLayoutEquations = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_10)
        self.horizontalLayoutEquations.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayoutEquations.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutEquations.setObjectName("horizontalLayoutEquations")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setOrientation(QtCore.Qt.Vertical)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Process Modeller"))
        item = self.tableNodes.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network"))
        item = self.tableNodes.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "type"))
        item = self.tableNodes.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "nature"))
        item = self.tableNodes.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "token"))
        item = self.tableNodes.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "edit"))
        self.pushNodeSave.setText(_translate("MainWindow", "save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_node), _translate("MainWindow", "node"))
        item = self.tableArcs.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network"))
        item = self.tableArcs.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "mechanism"))
        item = self.tableArcs.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "nature"))
        item = self.tableArcs.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "token"))
        item = self.tableArcs.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "edit"))
        self.pushArcSave.setText(_translate("MainWindow", "save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_arc), _translate("MainWindow", "arc"))
        item = self.tableIntrafaces.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network"))
        item = self.tableIntrafaces.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "token"))
        item = self.tableIntrafaces.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "edit"))
        self.pushIntrafaceSave.setText(_translate("MainWindow", "save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_intraface), _translate("MainWindow", "intraface"))
        item = self.tableInterfaces.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "network"))
        item = self.tableInterfaces.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "edit"))
        self.pushInterfaceSave.setText(_translate("MainWindow", "save"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_interface), _translate("MainWindow", "interface"))
        self.groupBoxEquations.setTitle(_translate("MainWindow", "Equations"))
