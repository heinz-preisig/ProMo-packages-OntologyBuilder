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
        MainWindow.resize(827, 696)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayoutSecondColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutSecondColumn.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayoutSecondColumn.setObjectName("verticalLayoutSecondColumn")
        self.groupBoxControls = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxControls.sizePolicy().hasHeightForWidth())
        self.groupBoxControls.setSizePolicy(sizePolicy)
        self.groupBoxControls.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBoxControls.setObjectName("groupBoxControls")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.groupBoxControls)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 161, 141))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonShowVariant = QtWidgets.QRadioButton(self.verticalLayoutWidget)
        self.radioButtonShowVariant.setObjectName("radioButtonShowVariant")
        self.verticalLayout.addWidget(self.radioButtonShowVariant)
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
        self.verticalLayoutSecondColumn.addWidget(self.groupBoxControls)
        self.pushButtonLeft = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonLeft.setObjectName("pushButtonLeft")
        self.verticalLayoutSecondColumn.addWidget(self.pushButtonLeft)
        self.scrollAreaLeft = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaLeft.setWidgetResizable(True)
        self.scrollAreaLeft.setObjectName("scrollAreaLeft")
        self.scrollAreaWidgetContentsLeft = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsLeft.setGeometry(QtCore.QRect(0, 0, 302, 387))
        self.scrollAreaWidgetContentsLeft.setObjectName("scrollAreaWidgetContentsLeft")
        self.scrollAreaLeft.setWidget(self.scrollAreaWidgetContentsLeft)
        self.verticalLayoutSecondColumn.addWidget(self.scrollAreaLeft)
        self.gridLayout.addLayout(self.verticalLayoutSecondColumn, 0, 1, 1, 1)
        self.verticalLayoutFirstColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutFirstColumn.setObjectName("verticalLayoutFirstColumn")
        self.scrollAreaInterNetworks = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaInterNetworks.setWidgetResizable(True)
        self.scrollAreaInterNetworks.setObjectName("scrollAreaInterNetworks")
        self.scrollAreaWidgetContentsInterNetworks = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsInterNetworks.setGeometry(QtCore.QRect(0, 0, 180, 203))
        self.scrollAreaWidgetContentsInterNetworks.setObjectName("scrollAreaWidgetContentsInterNetworks")
        self.scrollAreaInterNetworks.setWidget(self.scrollAreaWidgetContentsInterNetworks)
        self.verticalLayoutFirstColumn.addWidget(self.scrollAreaInterNetworks)
        self.scrollAreaEntities = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaEntities.setWidgetResizable(True)
        self.scrollAreaEntities.setObjectName("scrollAreaEntities")
        self.scrollAreaWidgetContentsEntities = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsEntities.setGeometry(QtCore.QRect(0, 0, 180, 202))
        self.scrollAreaWidgetContentsEntities.setObjectName("scrollAreaWidgetContentsEntities")
        self.scrollAreaEntities.setWidget(self.scrollAreaWidgetContentsEntities)
        self.verticalLayoutFirstColumn.addWidget(self.scrollAreaEntities)
        self.scrollAreaVariant = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaVariant.setWidgetResizable(True)
        self.scrollAreaVariant.setObjectName("scrollAreaVariant")
        self.scrollAreaWidgetContentsVariants = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsVariants.setGeometry(QtCore.QRect(0, 0, 180, 203))
        self.scrollAreaWidgetContentsVariants.setObjectName("scrollAreaWidgetContentsVariants")
        self.scrollAreaVariant.setWidget(self.scrollAreaWidgetContentsVariants)
        self.verticalLayoutFirstColumn.addWidget(self.scrollAreaVariant)
        self.gridLayout.addLayout(self.verticalLayoutFirstColumn, 0, 0, 1, 1)
        self.verticalLayoutThirdColumn = QtWidgets.QVBoxLayout()
        self.verticalLayoutThirdColumn.setObjectName("verticalLayoutThirdColumn")
        self.groupBoxApplication = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBoxApplication.sizePolicy().hasHeightForWidth())
        self.groupBoxApplication.setSizePolicy(sizePolicy)
        self.groupBoxApplication.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBoxApplication.setObjectName("groupBoxApplication")
        self.gridLayoutWidget = QtWidgets.QWidget(self.groupBoxApplication)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(40, 30, 164, 115))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayoutApplication = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayoutApplication.setContentsMargins(0, 0, 0, 0)
        self.gridLayoutApplication.setObjectName("gridLayoutApplication")
        self.pushButtonInformation = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonInformation.setText("")
        self.pushButtonInformation.setObjectName("pushButtonInformation")
        self.gridLayoutApplication.addWidget(self.pushButtonInformation, 1, 0, 1, 1)
        self.pushButtonCancel = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonCancel.setText("")
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.gridLayoutApplication.addWidget(self.pushButtonCancel, 1, 4, 1, 1)
        self.pushButtonSave = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonSave.setText("")
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayoutApplication.addWidget(self.pushButtonSave, 1, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutApplication.addItem(spacerItem, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayoutApplication.addItem(spacerItem1, 2, 0, 1, 1)
        self.verticalLayoutThirdColumn.addWidget(self.groupBoxApplication)
        self.pushButtonRight = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonRight.setObjectName("pushButtonRight")
        self.verticalLayoutThirdColumn.addWidget(self.pushButtonRight)
        self.scrollAreaRight = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollAreaRight.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.scrollAreaRight.setWidgetResizable(True)
        self.scrollAreaRight.setObjectName("scrollAreaRight")
        self.scrollAreaWidgetContentsRight = QtWidgets.QWidget()
        self.scrollAreaWidgetContentsRight.setGeometry(QtCore.QRect(0, 0, 303, 387))
        self.scrollAreaWidgetContentsRight.setObjectName("scrollAreaWidgetContentsRight")
        self.scrollAreaRight.setWidget(self.scrollAreaWidgetContentsRight)
        self.verticalLayoutThirdColumn.addWidget(self.scrollAreaRight)
        self.gridLayout.addLayout(self.verticalLayoutThirdColumn, 0, 2, 1, 1)
        self.gridLayout.setColumnStretch(0, 30)
        self.gridLayout.setColumnStretch(1, 50)
        self.gridLayout.setColumnStretch(2, 50)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.statusbar.setFont(font)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.groupBoxControls.setTitle(_translate("MainWindow", "controls"))
        self.radioButtonShowVariant.setText(_translate("MainWindow", "show"))
        self.radioButtonDuplicates.setText(_translate("MainWindow", "duplicates"))
        self.radioButtonNewVariant.setText(_translate("MainWindow", "new variant"))
        self.radioButtonEditVariant.setText(_translate("MainWindow", "edit variant"))
        self.radioButtonInstantiateVariant.setText(_translate("MainWindow", "instantiate variant"))
        self.pushButtonLeft.setText(_translate("MainWindow", "PushButton"))
        self.groupBoxApplication.setTitle(_translate("MainWindow", "application"))
        self.pushButtonRight.setText(_translate("MainWindow", "PushButton"))
