# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'editor_foundation_ontology_gui.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(856, 817)
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
        self.groupBoxNetwork = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxNetwork.setGeometry(QtCore.QRect(320, 30, 120, 221))
        self.groupBoxNetwork.setObjectName("groupBoxNetwork")
        self.layoutWidget = QtWidgets.QWidget(self.groupBoxNetwork)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 69, 66))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.radioButtonIntra = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButtonIntra.setObjectName("radioButtonIntra")
        self.verticalLayout_3.addWidget(self.radioButtonIntra)
        self.radioButtonInter = QtWidgets.QRadioButton(self.layoutWidget)
        self.radioButtonInter.setObjectName("radioButtonInter")
        self.verticalLayout_3.addWidget(self.radioButtonInter)
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBoxNetwork)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 90, 106, 66))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.pushAddChild = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushAddChild.setObjectName("pushAddChild")
        self.verticalLayout_4.addWidget(self.pushAddChild)
        self.pushRemoveChild = QtWidgets.QPushButton(self.layoutWidget1)
        self.pushRemoveChild.setObjectName("pushRemoveChild")
        self.verticalLayout_4.addWidget(self.pushRemoveChild)
        self.groupBoxFile = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxFile.setGeometry(QtCore.QRect(480, 30, 261, 221))
        self.groupBoxFile.setObjectName("groupBoxFile")
        self.widget = QtWidgets.QWidget(self.groupBoxFile)
        self.widget.setGeometry(QtCore.QRect(10, 30, 241, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetNoConstraint)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushSave = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushSave.sizePolicy().hasHeightForWidth())
        self.pushSave.setSizePolicy(sizePolicy)
        self.pushSave.setText("")
        self.pushSave.setObjectName("pushSave")
        self.horizontalLayout_4.addWidget(self.pushSave)
        self.pushInfo = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushInfo.sizePolicy().hasHeightForWidth())
        self.pushInfo.setSizePolicy(sizePolicy)
        self.pushInfo.setText("")
        self.pushInfo.setObjectName("pushInfo")
        self.horizontalLayout_4.addWidget(self.pushInfo)
        self.pushGraph = QtWidgets.QPushButton(self.widget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushGraph.sizePolicy().hasHeightForWidth())
        self.pushGraph.setSizePolicy(sizePolicy)
        self.pushGraph.setText("")
        self.pushGraph.setObjectName("pushGraph")
        self.horizontalLayout_4.addWidget(self.pushGraph)
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 290, 781, 361))
        self.tabWidget.setObjectName("tabWidget")
        self.tab_structure = QtWidgets.QWidget()
        self.tab_structure.setObjectName("tab_structure")
        self.groupBoxStructureComponents = QtWidgets.QGroupBox(self.tab_structure)
        self.groupBoxStructureComponents.setGeometry(QtCore.QRect(20, 30, 91, 211))
        self.groupBoxStructureComponents.setObjectName("groupBoxStructureComponents")
        self.layoutWidget2 = QtWidgets.QWidget(self.groupBoxStructureComponents)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 20, 74, 101))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonStructureNode = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButtonStructureNode.setObjectName("radioButtonStructureNode")
        self.verticalLayout.addWidget(self.radioButtonStructureNode)
        self.radioButtonStructureArc = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButtonStructureArc.setObjectName("radioButtonStructureArc")
        self.verticalLayout.addWidget(self.radioButtonStructureArc)
        self.radioButtonStructureToken = QtWidgets.QRadioButton(self.layoutWidget2)
        self.radioButtonStructureToken.setObjectName("radioButtonStructureToken")
        self.verticalLayout.addWidget(self.radioButtonStructureToken)
        self.widgetToken = QtWidgets.QWidget(self.tab_structure)
        self.widgetToken.setGeometry(QtCore.QRect(120, 10, 251, 301))
        self.widgetToken.setObjectName("widgetToken")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.widgetToken)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 50, 231, 191))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutToken = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayoutToken.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayoutToken.setObjectName("horizontalLayoutToken")
        self.listViewStructure = QtWidgets.QListWidget(self.tab_structure)
        self.listViewStructure.setGeometry(QtCore.QRect(380, 60, 191, 192))
        self.listViewStructure.setObjectName("listViewStructure")
        self.listViewStructureExtension = QtWidgets.QListWidget(self.tab_structure)
        self.listViewStructureExtension.setGeometry(QtCore.QRect(580, 60, 191, 192))
        self.listViewStructureExtension.setObjectName("listViewStructureExtension")
        self.layoutWidget3 = QtWidgets.QWidget(self.tab_structure)
        self.layoutWidget3.setGeometry(QtCore.QRect(380, 260, 120, 41))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushNewStructureElement = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushNewStructureElement.setText("")
        self.pushNewStructureElement.setObjectName("pushNewStructureElement")
        self.horizontalLayout.addWidget(self.pushNewStructureElement)
        self.pushDeleteStructureElement = QtWidgets.QPushButton(self.layoutWidget3)
        self.pushDeleteStructureElement.setText("")
        self.pushDeleteStructureElement.setObjectName("pushDeleteStructureElement")
        self.horizontalLayout.addWidget(self.pushDeleteStructureElement)
        self.layoutWidget4 = QtWidgets.QWidget(self.tab_structure)
        self.layoutWidget4.setGeometry(QtCore.QRect(580, 260, 120, 41))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_2.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushNewStructureElementExtension = QtWidgets.QPushButton(self.layoutWidget4)
        self.pushNewStructureElementExtension.setText("")
        self.pushNewStructureElementExtension.setObjectName("pushNewStructureElementExtension")
        self.horizontalLayout_2.addWidget(self.pushNewStructureElementExtension)
        self.pushDeleteStructureElementExtension = QtWidgets.QPushButton(self.layoutWidget4)
        self.pushDeleteStructureElementExtension.setText("")
        self.pushDeleteStructureElementExtension.setObjectName("pushDeleteStructureElementExtension")
        self.horizontalLayout_2.addWidget(self.pushDeleteStructureElementExtension)
        self.labelStructure = QtWidgets.QLabel(self.tab_structure)
        self.labelStructure.setGeometry(QtCore.QRect(380, 30, 161, 17))
        self.labelStructure.setObjectName("labelStructure")
        self.labelStructureExtension = QtWidgets.QLabel(self.tab_structure)
        self.labelStructureExtension.setGeometry(QtCore.QRect(580, 30, 181, 17))
        self.labelStructureExtension.setObjectName("labelStructureExtension")
        self.tabWidget.addTab(self.tab_structure, "")
        self.tab_behaviour = QtWidgets.QWidget()
        self.tab_behaviour.setObjectName("tab_behaviour")
        self.layoutWidget5 = QtWidgets.QWidget(self.tab_behaviour)
        self.layoutWidget5.setGeometry(QtCore.QRect(150, 260, 120, 41))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_3.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushNewBehaviourElement = QtWidgets.QPushButton(self.layoutWidget5)
        self.pushNewBehaviourElement.setText("")
        self.pushNewBehaviourElement.setObjectName("pushNewBehaviourElement")
        self.horizontalLayout_3.addWidget(self.pushNewBehaviourElement)
        self.pushDeleteBehaviourElement = QtWidgets.QPushButton(self.layoutWidget5)
        self.pushDeleteBehaviourElement.setText("")
        self.pushDeleteBehaviourElement.setObjectName("pushDeleteBehaviourElement")
        self.horizontalLayout_3.addWidget(self.pushDeleteBehaviourElement)
        self.groupBoxBehaviourComponents = QtWidgets.QGroupBox(self.tab_behaviour)
        self.groupBoxBehaviourComponents.setGeometry(QtCore.QRect(40, 40, 91, 211))
        self.groupBoxBehaviourComponents.setObjectName("groupBoxBehaviourComponents")
        self.layoutWidget6 = QtWidgets.QWidget(self.groupBoxBehaviourComponents)
        self.layoutWidget6.setGeometry(QtCore.QRect(10, 20, 75, 101))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget6)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.radioButtonBehaviourGraph = QtWidgets.QRadioButton(self.layoutWidget6)
        self.radioButtonBehaviourGraph.setObjectName("radioButtonBehaviourGraph")
        self.verticalLayout_2.addWidget(self.radioButtonBehaviourGraph)
        self.radioButtonBehaviourNode = QtWidgets.QRadioButton(self.layoutWidget6)
        self.radioButtonBehaviourNode.setObjectName("radioButtonBehaviourNode")
        self.verticalLayout_2.addWidget(self.radioButtonBehaviourNode)
        self.radioButtonBehaviourArc = QtWidgets.QRadioButton(self.layoutWidget6)
        self.radioButtonBehaviourArc.setObjectName("radioButtonBehaviourArc")
        self.verticalLayout_2.addWidget(self.radioButtonBehaviourArc)
        self.listViewBehaviour = QtWidgets.QListWidget(self.tab_behaviour)
        self.listViewBehaviour.setGeometry(QtCore.QRect(150, 60, 191, 192))
        self.listViewBehaviour.setObjectName("listViewBehaviour")
        self.groupBoxRules = QtWidgets.QGroupBox(self.tab_behaviour)
        self.groupBoxRules.setGeometry(QtCore.QRect(420, 40, 171, 80))
        self.groupBoxRules.setObjectName("groupBoxRules")
        self.radioButtonHasPortVariables = QtWidgets.QRadioButton(self.groupBoxRules)
        self.radioButtonHasPortVariables.setGeometry(QtCore.QRect(0, 20, 151, 22))
        self.radioButtonHasPortVariables.setObjectName("radioButtonHasPortVariables")
        self.tabWidget.addTab(self.tab_behaviour, "")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 30, 301, 221))
        self.groupBox.setObjectName("groupBox")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget.setGeometry(QtCore.QRect(20, 30, 256, 192))
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        self.treeWidget.header().setVisible(False)
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 670, 801, 111))
        self.groupBox_2.setObjectName("groupBox_2")
        self.msgWindow = QtWidgets.QTextBrowser(self.groupBox_2)
        self.msgWindow.setEnabled(False)
        self.msgWindow.setGeometry(QtCore.QRect(10, 30, 781, 81))
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
        self.groupBoxNetwork.setTitle(_translate("MainWindow", "network"))
        self.radioButtonIntra.setText(_translate("MainWindow", "intra"))
        self.radioButtonInter.setText(_translate("MainWindow", "inter"))
        self.pushAddChild.setText(_translate("MainWindow", "add child"))
        self.pushRemoveChild.setText(_translate("MainWindow", "remove child"))
        self.groupBoxFile.setTitle(_translate("MainWindow", "control"))
        self.pushSave.setToolTip(_translate("MainWindow", "save ProMo base ontology"))
        self.pushInfo.setToolTip(_translate("MainWindow", "information"))
        self.pushGraph.setToolTip(_translate("MainWindow", "make ProMo ontology graph"))
        self.tabWidget.setToolTip(_translate("MainWindow", "<html><head/><body><p>defines <span style=\" font-weight:600;\">structure</span> --&gt; bookkeeping </p><p><span style=\" font-weight:600;\">behaviour</span> --&gt; taxonometry of variabless</p></body></html>"))
        self.groupBoxStructureComponents.setTitle(_translate("MainWindow", "components"))
        self.radioButtonStructureNode.setText(_translate("MainWindow", "node"))
        self.radioButtonStructureArc.setText(_translate("MainWindow", "arc"))
        self.radioButtonStructureToken.setText(_translate("MainWindow", "token"))
        self.listViewStructure.setToolTip(_translate("MainWindow", "<html><head/><body><p>click once to select</p><p>twice to jump to definition location</p></body></html>"))
        self.listViewStructureExtension.setToolTip(_translate("MainWindow", "<html><head/><body><p>click once to select</p><p>twice to jump to definition location</p></body></html>"))
        self.pushNewStructureElement.setToolTip(_translate("MainWindow", "add"))
        self.pushDeleteStructureElement.setToolTip(_translate("MainWindow", "remove"))
        self.pushNewStructureElementExtension.setToolTip(_translate("MainWindow", "add"))
        self.pushDeleteStructureElementExtension.setToolTip(_translate("MainWindow", "remove"))
        self.labelStructure.setText(_translate("MainWindow", "stucture"))
        self.labelStructureExtension.setText(_translate("MainWindow", "extension"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_structure), _translate("MainWindow", "structure"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_structure), _translate("MainWindow", "<html><head/><body><p>structure the section that servest the bookkeeping. </p><p>Contains all items that appear in the models</p><p><span style=\" font-weight:600;\">nodes</span>: dynamics and distribution nature, </p><p><span style=\" font-weight:600;\">arcs</span> for each type of token the transport nature and the distribution nature, </p><p><span style=\" font-weight:600;\">tokens</span>: token item and refinement </p></body></html>"))
        self.groupBoxBehaviourComponents.setTitle(_translate("MainWindow", "components"))
        self.radioButtonBehaviourGraph.setText(_translate("MainWindow", "graph"))
        self.radioButtonBehaviourNode.setText(_translate("MainWindow", "node"))
        self.radioButtonBehaviourArc.setText(_translate("MainWindow", "arc"))
        self.listViewBehaviour.setToolTip(_translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">single</span> click   --&gt; select</p><p><span style=\" font-weight:600;\">double</span> click --&gt; jump to where item has been defined</p></body></html>"))
        self.groupBoxRules.setTitle(_translate("MainWindow", "rules"))
        self.radioButtonHasPortVariables.setText(_translate("MainWindow", "has port variables"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_behaviour), _translate("MainWindow", "behaviour"))
        self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab_behaviour), _translate("MainWindow", "<html><head/><body><p><span style=\" font-weight:600;\">behaviour</span>: </p><p><span style=\" font-weight:600;\">graph</span> --&gt; network,</p><p><span style=\" font-weight:600;\">node</span> : constant, frame and state, </p><p><span style=\" font-weight:600;\">arc</span>: transport</p></body></html>"))
        self.groupBox.setTitle(_translate("MainWindow", "domain tree"))
        self.treeWidget.setToolTip(_translate("MainWindow", "ProMo ontology domain tree"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Messages"))
