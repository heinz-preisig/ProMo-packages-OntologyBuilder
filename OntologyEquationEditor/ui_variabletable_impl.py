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

__author__ = "Preisig, Heinz A"

MAX_HEIGHT = 800

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from Common.common_resources import CONNECTION_NETWORK_SEPARATOR
from Common.common_resources import roundButton
# from Common.common_resources import globalVariableID
from Common.qt_resources import NO
from Common.qt_resources import YES
from Common.record_definitions import makeCompleteVariableRecord
from Common.ui_radio_selector_w_sroll_impl import UI_RadioSelector
from OntologyBuilder.OntologyEquationEditor.resources import ENABLED_COLUMNS
from OntologyBuilder.OntologyEquationEditor.resources import NEW_VAR
from OntologyBuilder.OntologyEquationEditor.ui_documentation_impl import UI_DocumentationDialog
from OntologyBuilder.OntologyEquationEditor.ui_physunits_impl import UI_PhysUnitsDialog
from OntologyBuilder.OntologyEquationEditor.ui_symbol_impl import UI_SymbolDialog
from OntologyBuilder.OntologyEquationEditor.variable_framework import simulateDeletion
from OntologyBuilder.OntologyEquationEditor.variable_framework import Units
from OntologyBuilder.OntologyEquationEditor.variable_table import VariableTable


class UI_VariableTableDialog(VariableTable):
  """
  dialog for a variable
  emits a signal on completion
  """

  completed = QtCore.pyqtSignal(str)
  picked = QtCore.pyqtSignal(str)
  new_variable = QtCore.pyqtSignal(str)
  new_equation = QtCore.pyqtSignal(int)
  deleted_symbol = QtCore.pyqtSignal(str)

  def __init__(self,
               title,
               variables,
               indices,
               network,
               network_expression,
               choice,
               has_port_variables,
               disabled_variables=[],
               hide_vars=[],
               hide_columns=[],
               info_file=None):
    """
    constructs a dialog window based on QDialog
    @param title:     title string: indicates the tree's nature
    @param variables: physical variable.
    @network:      network type
    @my_types:      type of variables being processed

    control is done through the interface and additional functions:
    - enable_pick_contents : true or false
    - enable_selection : rows and columns

    signals:
    - picked : returns selected item text
    - completed : button finished has been pressed
    -
    """

    enabled_variable_types = [choice]

    VariableTable.__init__(self,
                           title,
                           "variables_definition",
                           variables,
                           indices,
                           network,
                           # variables.index_networks_for_variable,       # defines variable space
                           enabled_variable_types,
                           hide_vars,
                           hide_columns,
                           info_file=info_file
                           )

    roundButton(self.ui.pushFinished, "back", tooltip="go back")
    roundButton(self.ui.pushInfo, "info", tooltip="information")

    self.network_expression = network_expression
    self.variable_list = []
    self.disabled_variables = disabled_variables
    self.has_port_variables = has_port_variables
    self.variables_in_table = []
    self.label_ID_dict = {}  # for changing / choosing index set
    self.reset_table()

    self.ui_symbol = UI_SymbolDialog()
    self.ui_symbol.finished.connect(self.reset_table)
    self.ui_units = UI_PhysUnitsDialog("new physical units")
    self.ui_units.finished.connect(self.reset_table)

    # self.setToolTips("edit")  # FIXME: this does not work. appears to be a pyqt issue.

  def show(self):
    self.reset_table()
    QtWidgets.QDialog.show(self)
    self.setToolTips("edit")
    self.raise_()

  def hideColumn(self, c):
    self.ui.tableVariable.hideColumn(c)

  def enable_column_selection(self, columns):
    self.enabled_columns = columns

  def protect_variable_type(self, variable_types):  # TODO may be useful
    self.protected_variable_types = variable_types

  def __showDeleteDialog(self, selected_ID):
    var_symbol = self.variables[selected_ID].label
    msg = "deleting variable : %s" % var_symbol
    d_vars, d_equs, d_vars_text, d_equs_text = simulateDeletion(self.variables, selected_ID, self.indices)
    v = d_vars_text[1:-1].replace("\n", ",  ")
    e = d_equs_text.replace("\n", "\n   ")
    msg += "\n\nand consequently \n...variables:%s \n\n...equations %s" % (v, e)

    reply = QtWidgets.QMessageBox.question(self, "choose", msg, YES, NO)
    # print("reply :", reply)
    if reply == YES:
      print("yes")
      self.__deleteVariable(d_vars, d_equs)
      self.reset_table()

  def __deleteVariable(self, d_vars, d_equs):
    print("going to delete: \n...variables:%s \n...equations %s" % (d_vars, d_equs))
    for id in d_equs:
      self.variables.removeEquation(id)
    for s in d_vars:
      self.variables.removeVariable(s)
    self.variables.indexVariables()  # indexEquationsInNetworks()
    self.reset_table()
    # self.makeTable()

  def __showNewVariableDialog(self):
    msg = "new port variable ?"
    if self.has_port_variables:
      reply = QtWidgets.QMessageBox.question(self, "choose", msg, YES, NO)
    else:
      reply = NO

    if reply == YES:
      print("yes")
      self.defineGivenVariable()
    elif reply == NO:
      print("no")
      self.__defineNewVarWithEquation()
    else:
      print("none")
    self.reset_table()

  def __defineNewVarWithEquation(self):
    self.new_variable.emit(self.selected_variable_type)

  ### table handling
  def on_tableVariable_itemClicked(self, item):

    c = int(item.column())
    r = int(item.row())
    # print("debugg row chosen is: %s" % r)
    # print("debugg column chosen is: %s" % c)
    item = self.ui.tableVariable.item
    self.selected_variable_type = str(item(r, 0).text())  # DOC: here I know if a new dimension must be generated

    if c == 0:
      if self.selected_variable_type[0] == "*":
        self.__defineNewVarWithEquation()  # RULE: first character in variable class name is * --> gen index
      self.__showNewVariableDialog()
      return

    # picking only
    self.selected_variable_symbol = str(item(r, 1).text())

    # get out if variable is disabled
    if self.selected_variable_symbol in self.disabled_variables:
      return

    # do not allow changing of units and index sets once in use or is defined via equation

    selected_ID = self.variables_in_table[r]
    v = self.variables[selected_ID]
    l = len(v.equations)
    not_yet_used = (self.variables.inv_incidence_dictionary[selected_ID] == []) and \
                   (len(self.variables[selected_ID].equations.keys()) == 0)
    if l != 0:
      if 3 in self.enabled_columns:
        self.enabled_columns.remove(3)
      if 4 in self.enabled_columns:
        self.enabled_columns.remove(4)
    else:
      if 3 not in self.enabled_columns:
        self.enabled_columns += [3]
      if 4 not in self.enabled_columns:
        self.enabled_columns += [4]

    if c not in self.enabled_columns:
      return

    # execute requested command
    if c == 1:
      # print("clicked 1 - symbol ", self.selected_variable_symbol)
      forbidden_symbols = []
      for ID in self.variables_in_table:
        forbidden_symbols.append(self.variables[ID].label)
      self.__changeSymbol(v, forbidden_symbols)
    elif c == 2:
      # print("clicked 2 - description ", v.doc)
      self.__changeDocumentation(v)
    elif c == 3:
      # print("clicked 3 - units ", v.units)
      if not_yet_used:
        self.__changeUnits(v)
    elif c == 4:
      # print("clicked 4 - indexing ", v.index_structures)
      if not_yet_used:
        self.__changeIndexing(v)
    elif c == 5:
      # print("clicked 5 - equations ", selected_number_of_equations)
      self.new_equation.emit(selected_ID)
    elif c == 6:
      # print("clicked 6 - delete ")
      self.__showDeleteDialog(selected_ID)
    return

  def defineGivenVariable(self):
    var_ID = self.variables.newProMoVariableIRI()  # globalVariableID(update=True)
    #
    # NOTE: there is something fundamentally wrong as when using the default things go utterly wrong.. python ???
    variable_record = makeCompleteVariableRecord(var_ID,
                                                 label=NEW_VAR,
                                                 type=self.selected_variable_type,
                                                 network=self.network,
                                                 doc=NEW_VAR,
                                                 index_structures=[],
                                                 units=Units(),
                                                 equations={},
                                                 aliases={},
                                                 )

    self.variables.addNewVariable(ID=var_ID, **variable_record)
    self.reset_table()
    enabled_columns = ENABLED_COLUMNS["edit"]["constant"]
    self.enable_column_selection(enabled_columns)

  def __changeSymbol(self, variable, forbidden_symbols):
    self.ui_symbol.setUp(variable, forbidden_symbols)
    self.ui_symbol.show()

  def __changeUnits(self, phys_var):
    self.ui_units.setUp(phys_var)  # = UI_PhysUnitsDialog("new physical units", phys_var)
    # self.ui_units.finished.connect(self.reset_table)
    self.ui_units.show()

  def __changeDocumentation(self, phys_var):
    self.ui_documentation = UI_DocumentationDialog(phys_var)
    self.ui_documentation.finished.connect(self.reset_table)
    self.ui_documentation.show()

  def __changeIndexing(self, phys_var):  # TODO: when does this make sense ?
    self.phys_var = phys_var
    if CONNECTION_NETWORK_SEPARATOR in phys_var.network:
      index_structures_labels = ["node", "arc"]  # RULE: connection networks have nodes and arcs
      self.label_ID_dict = {self.indices[ind_ID]["label"] for ind_ID in self.indices if
                            self.indices[ind_ID]["label"] in index_structures_labels}
    else:
      self.label_ID_dict = self.__getIndexListPerNetwork(self.network)
      index_structures_labels = [self.indices[ind_ID]["label"] for ind_ID in self.label_ID_dict.keys()]
    self.ui_selector = UI_RadioSelector(index_structures_labels,
                                        phys_var.index_structures,
                                        allowed=5)  # RULE: number of allowed indices is currently 5
    self.ui_selector.newSelection.connect(self.__gotNewIndexStrucList)
    self.ui_selector.show()

  def __getIndexListPerNetwork(self, nw):
    label_ID_dict = {}
    for ind_ID in self.indices:
      for layer in self.indices[ind_ID]["network"]:
        if layer == nw:
          label_ID_dict[ind_ID] = self.indices[ind_ID]["label"]
    return label_ID_dict

  def __gotNewIndexStrucList(self, strucs_list):
    indexing_sets = [ind_ID for ind_ID in self.indices if self.indices[ind_ID][
      "label"] in strucs_list]
    self.phys_var.index_structures = indexing_sets
    self.reset_table()

  def on_pushFinished_pressed(self):
    self.closeEvent(None)

  def closeEvent(self, event):
    for ID in self.variables:
      if self.variables[ID].label == NEW_VAR:
        self.variables.removeVariable(ID)

    try:
      self.ui_symbol.close()
    except:
      pass

    try:
      self.ui_selector.close()
    except:
      pass

    try:
      self.ui_units.close()
    except:
      pass
    try:
      self.ui_documentation.close()
    except:
      pass
    self.completed.emit("close")

    self.close()
