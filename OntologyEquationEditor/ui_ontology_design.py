# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_ontology_design.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_OntologyDesigner(object):
    def setupUi(self, OntologyDesigner):
        OntologyDesigner.setObjectName("OntologyDesigner")
        OntologyDesigner.resize(426, 956)
        self.groupVariables = QtWidgets.QGroupBox(OntologyDesigner)
        self.groupVariables.setGeometry(QtCore.QRect(20, 340, 381, 511))
        self.groupVariables.setObjectName("groupVariables")
        self.tabWidget = QtWidgets.QTabWidget(self.groupVariables)
        self.tabWidget.setGeometry(QtCore.QRect(10, 30, 351, 411))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_networks = QtWidgets.QWidget()
        self.tab_networks.setObjectName("tab_networks")
        self.treeWidget = QtWidgets.QTreeWidget(self.tab_networks)
        self.treeWidget.setGeometry(QtCore.QRect(10, 20, 311, 261))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.groupEdit = QtWidgets.QGroupBox(self.tab_networks)
        self.groupEdit.setGeometry(QtCore.QRect(10, 290, 311, 81))
        self.groupEdit.setObjectName("groupEdit")
        self.groupBoxComponents = QtWidgets.QGroupBox(self.groupEdit)
        self.groupBoxComponents.setGeometry(QtCore.QRect(10, 20, 281, 61))
        self.groupBoxComponents.setObjectName("groupBoxComponents")
        self.radioArc = QtWidgets.QRadioButton(self.groupBoxComponents)
        self.radioArc.setGeometry(QtCore.QRect(210, 30, 61, 22))
        self.radioArc.setObjectName("radioArc")
        self.radioNode = QtWidgets.QRadioButton(self.groupBoxComponents)
        self.radioNode.setGeometry(QtCore.QRect(130, 30, 71, 22))
        self.radioNode.setObjectName("radioNode")
        self.radioGraph = QtWidgets.QRadioButton(self.groupBoxComponents)
        self.radioGraph.setGeometry(QtCore.QRect(30, 30, 71, 22))
        self.radioGraph.setObjectName("radioGraph")
        self.tabWidget.addTab(self.tab_networks, "")
        self.tab_intranets = QtWidgets.QWidget()
        self.tab_intranets.setObjectName("tab_intranets")
        self.combo_IntraConnectionNetwork = QtWidgets.QComboBox(self.tab_intranets)
        self.combo_IntraConnectionNetwork.setGeometry(QtCore.QRect(30, 50, 289, 27))
        self.combo_IntraConnectionNetwork.setObjectName("combo_IntraConnectionNetwork")
        self.tabWidget.addTab(self.tab_intranets, "")
        self.tab_internets = QtWidgets.QWidget()
        self.tab_internets.setObjectName("tab_internets")
        self.combo_InterConnectionNetwork = QtWidgets.QComboBox(self.tab_internets)
        self.combo_InterConnectionNetwork.setGeometry(QtCore.QRect(30, 50, 289, 27))
        self.combo_InterConnectionNetwork.setObjectName("combo_InterConnectionNetwork")
        self.tabWidget.addTab(self.tab_internets, "")
        self.combo_EditVariableTypes = QtWidgets.QComboBox(self.groupVariables)
        self.combo_EditVariableTypes.setGeometry(QtCore.QRect(40, 470, 301, 27))
        self.combo_EditVariableTypes.setObjectName("combo_EditVariableTypes")
        self.groupOntology = QtWidgets.QGroupBox(OntologyDesigner)
        self.groupOntology.setGeometry(QtCore.QRect(20, 10, 381, 191))
        self.groupOntology.setObjectName("groupOntology")
        self.layoutWidget = QtWidgets.QWidget(self.groupOntology)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 348, 171))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioVariables = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioVariables.setObjectName("radioVariables")
        self.verticalLayout.addWidget(self.radioVariables)
        self.radioVariablesAliases = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioVariablesAliases.setObjectName("radioVariablesAliases")
        self.verticalLayout.addWidget(self.radioVariablesAliases)
        self.radioIndicesAliases = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioIndicesAliases.setObjectName("radioIndicesAliases")
        self.verticalLayout.addWidget(self.radioIndicesAliases)
        self.horizontalLayout.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 5, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 0, 2, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem3, 4, 4, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem4, 3, 5, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem5, 2, 4, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem6, 1, 3, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem7, 3, 3, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem8, 4, 2, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem9, 0, 4, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem10, 1, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem11, 2, 2, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem12, 3, 0, 1, 1)
        spacerItem13 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem13, 1, 5, 1, 1)
        self.pushCompile = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushCompile.sizePolicy().hasHeightForWidth())
        self.pushCompile.setSizePolicy(sizePolicy)
        self.pushCompile.setText("")
        self.pushCompile.setObjectName("pushCompile")
        self.gridLayout.addWidget(self.pushCompile, 1, 4, 1, 1)
        self.pushInfo = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushInfo.sizePolicy().hasHeightForWidth())
        self.pushInfo.setSizePolicy(sizePolicy)
        self.pushInfo.setText("")
        self.pushInfo.setObjectName("pushInfo")
        self.gridLayout.addWidget(self.pushInfo, 1, 2, 1, 1)
        self.pushMakeAllVarEqPictures = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushMakeAllVarEqPictures.sizePolicy().hasHeightForWidth())
        self.pushMakeAllVarEqPictures.setSizePolicy(sizePolicy)
        self.pushMakeAllVarEqPictures.setText("")
        self.pushMakeAllVarEqPictures.setAutoDefault(False)
        self.pushMakeAllVarEqPictures.setDefault(True)
        self.pushMakeAllVarEqPictures.setObjectName("pushMakeAllVarEqPictures")
        self.gridLayout.addWidget(self.pushMakeAllVarEqPictures, 3, 4, 1, 1)
        self.pushExit = QtWidgets.QPushButton(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushExit.sizePolicy().hasHeightForWidth())
        self.pushExit.setSizePolicy(sizePolicy)
        self.pushExit.setText("")
        self.pushExit.setAutoDefault(False)
        self.pushExit.setDefault(True)
        self.pushExit.setObjectName("pushExit")
        self.gridLayout.addWidget(self.pushExit, 3, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.groupFiles = QtWidgets.QGroupBox(OntologyDesigner)
        self.groupFiles.setGeometry(QtCore.QRect(20, 210, 301, 111))
        self.groupFiles.setObjectName("groupFiles")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.groupFiles)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 20, 160, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushWrite = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushWrite.setText("")
        self.pushWrite.setAutoDefault(False)
        self.pushWrite.setDefault(True)
        self.pushWrite.setObjectName("pushWrite")
        self.horizontalLayout_2.addWidget(self.pushWrite)
        self.pushShowVariables = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pushShowVariables.setText("")
        self.pushShowVariables.setAutoDefault(False)
        self.pushShowVariables.setDefault(True)
        self.pushShowVariables.setObjectName("pushShowVariables")
        self.horizontalLayout_2.addWidget(self.pushShowVariables)
        self.msgWindow = QtWidgets.QTextBrowser(OntologyDesigner)
        self.msgWindow.setEnabled(False)
        self.msgWindow.setGeometry(QtCore.QRect(20, 860, 381, 81))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(76, 76, 76))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.PlaceholderText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.WindowText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Text, brush)
        brush = QtGui.QBrush(QtGui.QColor(60, 60, 60, 128))
        brush.setStyle(QtCore.Qt.NoBrush)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.PlaceholderText, brush)
        self.msgWindow.setPalette(palette)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.msgWindow.setFont(font)
        self.msgWindow.setAcceptDrops(False)
        self.msgWindow.setObjectName("msgWindow")

        self.retranslateUi(OntologyDesigner)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(OntologyDesigner)

    def retranslateUi(self, OntologyDesigner):
        _translate = QtCore.QCoreApplication.translate
        OntologyDesigner.setWindowTitle(_translate("OntologyDesigner", "ProMo Equation Editor"))
        self.groupVariables.setTitle(_translate("OntologyDesigner", "variables & equations"))
        self.groupEdit.setTitle(_translate("OntologyDesigner", "Edit"))
        self.groupBoxComponents.setTitle(_translate("OntologyDesigner", "components"))
        self.radioArc.setToolTip(_translate("OntologyDesigner", "select to edit variables"))
        self.radioArc.setText(_translate("OntologyDesigner", "arc"))
        self.radioNode.setToolTip(_translate("OntologyDesigner", "select to edit variables"))
        self.radioNode.setText(_translate("OntologyDesigner", "node"))
        self.radioGraph.setToolTip(_translate("OntologyDesigner", "select to edit variables"))
        self.radioGraph.setText(_translate("OntologyDesigner", "graph"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_networks), _translate("OntologyDesigner", "networks"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_intranets), _translate("OntologyDesigner", "intr A nets"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_internets), _translate("OntologyDesigner", "int E rnets"))
        self.groupOntology.setTitle(_translate("OntologyDesigner", "Ontology"))
        self.radioVariables.setToolTip(_translate("OntologyDesigner", "select to edit variables"))
        self.radioVariables.setText(_translate("OntologyDesigner", "variables"))
        self.radioVariablesAliases.setToolTip(_translate("OntologyDesigner", "select to edit variable aliases"))
        self.radioVariablesAliases.setText(_translate("OntologyDesigner", "variable aliases"))
        self.radioIndicesAliases.setToolTip(_translate("OntologyDesigner", "select to edit index aliases"))
        self.radioIndicesAliases.setText(_translate("OntologyDesigner", " index aliases"))
        self.pushCompile.setToolTip(_translate("OntologyDesigner", "press to compile"))
        self.pushInfo.setToolTip(_translate("OntologyDesigner", "press for information"))
        self.pushMakeAllVarEqPictures.setToolTip(_translate("OntologyDesigner", "<html><head/><body><p>- compiles into all available code languages</p><p>- writes equations and variables as well as index file</p><p>- generates latex files with dot graphs</p></body></html>"))
        self.pushExit.setToolTip(_translate("OntologyDesigner", "<html><head/><body><p>- compiles into all available code languages</p><p>- writes equations and variables as well as index file</p><p>- generates latex files with dot graphs</p></body></html>"))
        self.groupFiles.setTitle(_translate("OntologyDesigner", "Files"))
        self.pushWrite.setToolTip(_translate("OntologyDesigner", "<html><head/><body><p>- compiles into all available code languages</p><p>- writes equations and variables as well as index file</p><p>- generates latex files with dot graphs</p></body></html>"))
        self.pushShowVariables.setToolTip(_translate("OntologyDesigner", "<html><head/><body><p>- compiles into all available code languages</p><p>- writes equations and variables as well as index file</p><p>- generates latex files with dot graphs</p></body></html>"))
