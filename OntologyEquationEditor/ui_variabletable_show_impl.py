#!/usr/local/bin/python3
# encoding: utf-8
"""
@summary:      An editor for designing ontologies in my context
@contact:      heinz.preisig@chemeng.ntnu.no
@requires:     Python 3 or higher
@since:        29.08.15
@version:      0.1
@change:       Aug 29, 2015
@author:       Preisig, Heinz A
@copyright:    2014 Preisig, Heinz A  All rights reserved.
"""

__author__ = 'Preisig, Heinz A'

MAX_HEIGHT = 800

import os

from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5 import QtGui

from Common.resources_icons import roundButton
from OntologyBuilder.OntologyEquationEditor.variable_table import VariableTable


class UI_VariableTableShow(VariableTable):
  """
  dialog for a variable
  emits a signal on completion
  """

  completed = QtCore.pyqtSignal(str)
  picked = QtCore.pyqtSignal(str)
  new_variable = QtCore.pyqtSignal(str)
  new_equation = QtCore.pyqtSignal(str, str)
  deleted_symbol = QtCore.pyqtSignal(str)

  def __init__(self,
               title,
               variables,
               indices,
               network,
               ontology_name,
               enabled_types=['ALL'],
               hide_vars=[],
               hide_columns=[],
               info_file=None,
               hidden=[],
               ):
    """
    constructs a dialog window based on QDialog for picking variables
    @param title:     title string: indicates the tree's nature
    @param variables: physical variable.
    @network:      network type
    @my_types:      type of variables being processed

    control is done through the interface and additional functions:
    - enable_pick_contents : true or false
    - enable_seclection : rows and columns

    signals:
    - picked : returns selected item text
    - completed : button finished has been pressed
    -
    """
    self.ontology_name = ontology_name
    VariableTable.__init__(self,
                           title,
                           "variable_picking",
                           variables,
                           indices,
                           network,
                           # variables.index_accessible_variables_on_networks,
                           enabled_types,
                           hide_vars,
                           hide_columns,
                           info_file=info_file
                           )
    buttons = {}
    buttons["back"] = self.ui.pushFinished
    buttons["info"] = self.ui.pushInfo
    buttons["new"] = self.ui.pushNew
    buttons["port"] = self.ui.pushPort

    roundButton(buttons["back"], "back", tooltip="go back")
    roundButton(buttons["info"], "info", tooltip="information")
    roundButton(buttons["new"], "new", tooltip="new variable")
    roundButton(buttons["port"], "port", tooltip="new port variable")
    for b in hidden:
      buttons[b].hide()
    self.variable_list = []
    self.hide_columns = hide_columns

    self.setToolTips("show")
    self.ui.tableVariable.setToolTip("click on row to copy variable to expression")
    self.ui.tableVariable.setSortingEnabled(True)

    # ontology_location = self.ontology_name  #NOTE: did ot work
    # eq_ID = 83
    # eqfile = os.path.join(ontology_location, "LaTeX", "equation_%s.png" % eq_ID)
    #
    # lbl = QtGui.QIcon(QtGui.QPixmap(eqfile))
    # item = QtWidgets.QTableWidgetItem()
    # item.setIcon(lbl)
    # self.ui.tableVariable.setItem(1,2, item)


  def on_tableVariable_itemClicked(self, item):
    r = int(item.row())
    item = self.ui.tableVariable.item
    self.selected_variable_symbol = str(item(r, 1).text())
    print("debugging -- show equations ")
    return


  @staticmethod
  def __addQtTableItem(tab, s, row, col):
    item = QtWidgets.QTableWidgetItem(s)
    tab.setRowCount(row + 1)
    tab.setItem(row, col, item)

  def on_tableVariable_itemDoubleClicked(self, item):
    print("debugging -- double click on item", item.row(), item.column())

  def on_pushFinished_pressed(self):
    self.close()

  def closeEvent(self, event):
    self.close()
