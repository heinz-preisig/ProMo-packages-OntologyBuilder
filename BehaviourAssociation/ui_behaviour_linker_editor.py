# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_behaviour_linker_editor.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1477, 876)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutFirstColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutFirstColumn.setObjectName("verticalLayoutFirstColumn")
        self.scrollAreaInterNetworks = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaInterNetworks.setWidgetResizable(True)
        self.scrollAreaInterNetworks.setObjectName("scrollAreaInterNetworks")
        self.scrollAreaWidgetContentsInterNetworks = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsInterNetworks.setGeometry(QtCore.QRect(0, 0, 237, 263))
        self.scrollAreaWidgetContentsInterNetworks.setObjectName("scrollAreaWidgetContentsInterNetworks")
        self.scrollAreaInterNetworks.setWidget(self.scrollAreaWidgetContentsInterNetworks)
        self.verticalLayoutFirstColumn.addWidget(self.scrollAreaInterNetworks)
        self.tabWidgetNodesArcs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidgetNodesArcs.setObjectName("tabWidgetNodesArcs")
        self.nodes = QtWidgets.QWidget()
        self.nodes.setObjectName("nodes")
        self.listNodeObjects = QtWidgets.QListWidget(self.nodes)
        self.listNodeObjects.setGeometry(QtCore.QRect(10, 33, 241, 191))
        self.listNodeObjects.setObjectName("listNodeObjects")
        self.tabWidgetNodesArcs.addTab(self.nodes, "")
        self.arcs = QtWidgets.QWidget()
        self.arcs.setObjectName("arcs")
        self.listArcObjects = QtWidgets.QListWidget(self.arcs)
        self.listArcObjects.setGeometry(QtCore.QRect(10, 20, 241, 191))
        self.listArcObjects.setObjectName("listArcObjects")
        self.tabWidgetNodesArcs.addTab(self.arcs, "")
        self.verticalLayoutFirstColumn.addWidget(self.tabWidgetNodesArcs)
        self.listVariants = QtWidgets.QListWidget(self.centralwidget)
        self.listVariants.setObjectName("listVariants")
        self.verticalLayoutFirstColumn.addWidget(self.listVariants)
        self.gridLayout.addLayout(self.verticalLayoutFirstColumn, 0, 0, 1, 1)
        self.verticalLayoutThirdColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutThirdColumn.setObjectName("verticalLayoutThirdColumn")
        self.groupBoxApplication = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxApplication.sizePolicy().hasHeightForWidth())
        self.groupBoxApplication.setSizePolicy(sizePolicy)
        self.groupBoxApplication.setMinimumSize(QtCore.QSize(0, 220))
        self.groupBoxApplication.setObjectName("groupBoxApplication")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBoxApplication)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 274, 115))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutApplication = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutApplication.setContentsMargins(5, 0, 5, 0)
        self.gridLayoutApplication.setObjectName("gridLayoutApplication")
        self.pushButtonSave = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonSave.sizePolicy().hasHeightForWidth())
        self.pushButtonSave.setSizePolicy(sizePolicy)
        self.pushButtonSave.setText("")
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayoutApplication.addWidget(self.pushButtonSave, 1, 3, 1, 1)
        self.pushButtonInformation = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonInformation.sizePolicy().hasHeightForWidth())
        self.pushButtonInformation.setSizePolicy(sizePolicy)
        self.pushButtonInformation.setText("")
        self.pushButtonInformation.setObjectName("pushButtonInformation")
        self.gridLayoutApplication.addWidget(self.pushButtonInformation, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutApplication.addItem(spacerItem, 0, 0, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonCancel.sizePolicy().hasHeightForWidth())
        self.pushButtonCancel.setSizePolicy(sizePolicy)
        self.pushButtonCancel.setText("")
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayoutApplication.addWidget(self.pushButtonCancel, 1, 4, 1, 1)
        self.pushButtonMakeLatex = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonMakeLatex.sizePolicy().hasHeightForWidth())
        self.pushButtonMakeLatex.setSizePolicy(sizePolicy)
        self.pushButtonMakeLatex.setText("")
        self.pushButtonMakeLatex.setObjectName("pushButtonMakeLatex")
        self.gridLayoutApplication.addWidget(self.pushButtonMakeLatex, 1, 5, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutApplication.addItem(spacerItem1, 2, 0, 1, 1)
        self.pushButtonViewLatex = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButtonViewLatex.sizePolicy().hasHeightForWidth())
        self.pushButtonViewLatex.setSizePolicy(sizePolicy)
        self.pushButtonViewLatex.setText("")
        self.pushButtonViewLatex.setObjectName("pushButtonViewLatex")
        self.gridLayoutApplication.addWidget(self.pushButtonViewLatex, 1, 6, 1, 1)
        self.verticalLayoutThirdColumn.addWidget(self.groupBoxApplication)
        self.pushButtonRight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.verticalLayoutThirdColumn.addWidget(self.pushButtonRight)
        self.scrollAreaRight = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaRight.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaRight.setWidgetResizable(True)
        self.scrollAreaRight.setObjectName("scrollAreaRight")
        self.scrollAreaWidgetContentsRight = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsRight.setGeometry(QtCore.QRect(0, 0, 599, 547))
        self.scrollAreaWidgetContentsRight.setObjectName("scrollAreaWidgetContentsRight")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.scrollAreaWidgetContentsRight)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(10, 10, 581, 531))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.listRight = QtWidgets.QListWidget(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listRight.sizePolicy().hasHeightForWidth())
        self.listRight.setSizePolicy(sizePolicy)
        self.listRight.setObjectName("listRight")
        self.horizontalLayout_2.addWidget(self.listRight)
        self.scrollAreaRight.setWidget(self.scrollAreaWidgetContentsRight)
        self.verticalLayoutThirdColumn.addWidget(self.scrollAreaRight)
        self.gridLayout.addLayout(self.verticalLayoutThirdColumn, 0, 2, 1, 1)
        self.verticalLayoutSecondColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutSecondColumn.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayoutSecondColumn.setObjectName("verticalLayoutSecondColumn")
        self.groupBoxControls = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxControls.sizePolicy().hasHeightForWidth())
        self.groupBoxControls.setSizePolicy(sizePolicy)
        self.groupBoxControls.setMinimumSize(QtCore.QSize(0, 220))
        self.groupBoxControls.setObjectName("groupBoxControls")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBoxControls)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 161, 170))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonShowVariant = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonShowVariant.setObjectName("radioButtonShowVariant")
        self.verticalLayout.addWidget(self.radioButtonShowVariant)
        self.radioButtonMakBase = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonMakBase.setObjectName("radioButtonMakBase")
        self.verticalLayout.addWidget(self.radioButtonMakBase)
        self.radioButtonDuplicates = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonDuplicates.setObjectName("radioButtonDuplicates")
        self.verticalLayout.addWidget(self.radioButtonDuplicates)
        self.radioButtonNewVariant = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonNewVariant.setObjectName("radioButtonNewVariant")
        self.verticalLayout.addWidget(self.radioButtonNewVariant)
        self.radioButtonEditVariant = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonEditVariant.setObjectName("radioButtonEditVariant")
        self.verticalLayout.addWidget(self.radioButtonEditVariant)
        self.radioButtonInstantiateVariant = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonInstantiateVariant.setObjectName("radioButtonInstantiateVariant")
        self.verticalLayout.addWidget(self.radioButtonInstantiateVariant)
        self.pushButtonDelete = QtWidgets.QPushButton(self.groupBoxControls)
        self.pushButtonDelete.setGeometry(QtCore.QRect(190, 30, 51, 41))
        self.pushButtonDelete.setText("")
        self.pushButtonDelete.setObjectName("pushButtonDelete")
        self.pushButtonUpdate = QtWidgets.QPushButton(self.groupBoxControls)
        self.pushButtonUpdate.setGeometry(QtCore.QRect(250, 30, 51, 41))
        self.pushButtonUpdate.setText("")
        self.pushButtonUpdate.setObjectName("pushButtonUpdate")
        self.verticalLayoutSecondColumn.addWidget(self.groupBoxControls)
        self.pushButtonLeft = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.verticalLayoutSecondColumn.addWidget(self.pushButtonLeft)
        self.scrollAreaLeft = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaLeft.setWidgetResizable(True)
        self.scrollAreaLeft.setObjectName("scrollAreaLeft")
        self.scrollAreaWidgetContentsLeft = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsLeft.setGeometry(QtCore.QRect(0, 0, 599, 547))
        self.scrollAreaWidgetContentsLeft.setObjectName("scrollAreaWidgetContentsLeft")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.scrollAreaWidgetContentsLeft)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 9, 581, 531))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listLeft = QtWidgets.QListWidget(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listLeft.sizePolicy().hasHeightForWidth())
        self.listLeft.setSizePolicy(sizePolicy)
        self.listLeft.setObjectName("listLeft")
        self.horizontalLayout.addWidget(self.listLeft)
        self.scrollAreaLeft.setWidget(self.scrollAreaWidgetContentsLeft)
        self.verticalLayoutSecondColumn.addWidget(self.scrollAreaLeft)
        self.gridLayout.addLayout(self.verticalLayoutSecondColumn, 0, 1, 1, 1)
        self.gridLayout.setColumnStretch(0, 2)
        self.gridLayout.setColumnStretch(1, 5)
        self.gridLayout.setColumnStretch(2, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidgetNodesArcs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.tabWidgetNodesArcs.setTabText(self.tabWidgetNodesArcs.indexOf(self.nodes), _translate("MainWindow", "nodes"))
        self.tabWidgetNodesArcs.setTabText(self.tabWidgetNodesArcs.indexOf(self.arcs), _translate("MainWindow", "arcs"))
        self.groupBoxApplication.setTitle(_translate("MainWindow", "application"))
        self.pushButtonRight.setText(_translate("MainWindow", "PushButton"))
        self.groupBoxControls.setTitle(_translate("MainWindow", "controls"))
        self.radioButtonShowVariant.setText(_translate("MainWindow", "show"))
        self.radioButtonMakBase.setText(_translate("MainWindow", "make base"))
        self.radioButtonDuplicates.setText(_translate("MainWindow", "duplicates"))
        self.radioButtonNewVariant.setText(_translate("MainWindow", "new variant"))
        self.radioButtonEditVariant.setText(_translate("MainWindow", "edit variant"))
        self.radioButtonInstantiateVariant.setText(_translate("MainWindow", "instantiate variant"))
        self.pushButtonLeft.setText(_translate("MainWindow", "PushButton"))
