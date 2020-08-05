#!/usr/local/bin/python3
# encoding: utf-8

"""
===============================================================================
 Ontology design facility
===============================================================================

This program is part of the ProcessModelling suite

"""

__project__ = "ProcessModeller  Suite"
__author__ = "PREISIG, Heinz A"
__copyright__ = "Copyright 2015, PREISIG, Heinz A"
__since__ = "03.05.2019"
__license__ = "GPL planned -- until further notice for Bio4Fuel & MarketPlace internal use only"
__version__ = "5.04"
__email__ = "heinz.preisig@chemeng.ntnu.no"
__status__ = "beta"

import os
from PyQt4 import QtCore
from PyQt4 import QtGui

from copy import copy

from Common.common_resources import M_None
from Common.common_resources import getOntologyName
from Common.ontology_container import OntologyContainer
from Common.qt_resources import cleanLayout
from Common.radio_selector_impl import RadioSelector
from Common.record_definitions import EquationAssignment
from Common.record_definitions import Interface
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.resource_initialisation import checkAndFixResources
from Common.ui_radio_selector_w_sroll_impl import UI_RadioSelector
from OntologyBuilder.OntologyEquationAssignmentEditor.assign_equations_gui import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import ID_delimiter
from OntologyBuilder.OntologyEquationEditor.resources import ID_spacer
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeIncidenceDictionaries
from Common.treeid import Tree
from graphviz import Digraph

import subprocess
# from OntologyBuilder.OntologyEquationEditor.variable_framework import simulateDeletion

MAX_HEIGHT = 800

class VariableEquationTree(dict):
  def __init__(self, ID):
    self["ID_tree"] = Tree(0)
    self["variable"] = [ID]
    self["equation"] = []

  def addNode(self, what, parent):
    node_ID = self["ID_tree"].addChild(parent)
    self[what].append(node_ID)
    return node_ID

  def graphMe(self, ontology_name, var_labels, equ_labels):

    self.var_labels = var_labels
    self.equ_labels = equ_labels

    dot_path = os.path.join(DIRECTORIES["ontology_repository"], ontology_name, DIRECTORIES["ontology_graphs_location"],
                            "%s")
    o_template = dot_path  # + ".gv"
    # o = FILES["ontology_file"] % ontology_name
    #
    # the tree of networks
    f = o_template % "vars_equs"
    print(f)
    graph_attr = {}
    graph_attr["nodesep"] = "1"
    graph_attr["ranksep"] = "0.3"
    # graph_attr.edge_attr["color"] = "blue"
    graph_attr["splines"] = "false"  # ""polyline"
    edge_attr = {}
    # edge_attr["tailport"] = "s"
    # edge_attr["headport"] = "n"
    simple_graph = Digraph("T", filename=f)
    simple_graph.graph_attr = graph_attr
    simple_graph.edge_attr = edge_attr

    simple_graph.node(str(0), var_labels, style="filled", collor="blue" )
    self.__walkTree(0,simple_graph)

    simple_graph.view()  # generates pdf
    os.remove(f)

  def __walkTree(self, parent_node_ID, graph):
    children = self["ID_tree"][parent_node_ID]["children"]
    if children:
      for child in children:
        if child in self["equation"]:
          colour = "cyan"
          try:
            node_label = self.equ_labels[child].strip()
          except:
            print (">>>>>>>>>>> no such node")
            node_label = "unknown"
        elif child in self["variable"]:
          colour = "cornsilk"
          try:
            node_label = self.var_labels[child]
          except:
            print(" no such variable ID ", child)
            node_label = "unknown"
        else:
          print (">>>>>>>>>>> no such node")
          node_label = "unknown"

        graph.node(str(child), node_label, style="filled", color=colour)
        graph.edge(str(parent_node_ID),str(child))
        self.__walkTree(child, graph)

    else:
      return

class TreeNode(dict):
  def __init__(self, parents, type, contents):
    self["parents"] = parents
    self["children"] = []
    self["type"] = type
    self["contents"] = contents

  def addChild(self, child):
    self["children"].append(child)

class MakeVariableTree(dict):
  def __init__(self, variables):
    self.variables=variables
    self.tree[ID] = TreeNode()

  def nextEquation(self, ID, parent ):
    children = self.variables[ID]["equations"]

   # for child in children:
   #   self.tree[]



class UI_EditorEquationAssignment(QtGui.QMainWindow):

  # potential_issues : TODO : is the order important. Adding a network does leave us unordered compared to the old
  #  approach....???

  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ontology_name = getOntologyName(task="task_entity_generation")
    self.ontology_dir = DIRECTORIES["ontology_location"] % self.ontology_name
    self.ontology_file = FILES["ontology_file"] % self.ontology_name

    checkAndFixResources(self.ontology_name, stage="ontology_stage_2")

    self.ontology_container = OntologyContainer(self.ontology_name)
    self.ontology_tree = self.ontology_container.ontology_tree
    self.interfaces = self.ontology_container.interfaces
    self.variables = self.ontology_container.vars  # readVariables()
    self.indices = self.ontology_container.indices
    self.incidence_dictionary, self.inv_incidence_dictionary = makeIncidenceDictionaries(self.variables)

    self.equation_dictionary = {}
    self.__makeEquationDictionary()
    self.equation_assignment = self.ontology_container.equation_assignment

    self.radio_selectors = {}

    self.current_component = None  # node or arc

    self.current_equation_IDs = {}  # hash: radio button index     value: equation_ID_str

    self.current_node_network = None
    self.previous_node_network = None
    self.current_node_variable_class = None
    self.selected_node_key = None
    self.current_node_equation = None

    self.current_arc_network = None
    self.previous_arc_network = None
    self.current_arc_variable_class = None
    self.selected_arc_key = None
    self.current_arc_equation = None

    self.current_interface_network = None
    self.previous_interface_network = None
    self.current_interface_variable_class = None
    self.selected_interface_key = None
    self.current_interface_equation = None

    self.node_indicator_item = None
    self.last_node_coordinate = None
    self.arc_indicator_item = None
    self.last_arc_coordinate = None
    self.intra_indicator_item = None
    self.last_interface_coordinat = None
    self.inter_indicator_item = None
    self.last_inter_coordinate = None

    self.node_table_objects = {}
    self.arc_table_objects = {}
    self.intra_table_objects = {}
    self.inter_table_objects = {}

    # icons
    self.icons = {"edit": QtGui.QIcon("%s/edit.png" % DIRECTORIES["icon_location"]),
                  "OK"  : QtGui.QIcon("%s/accept.png" % DIRECTORIES["icon_location"]),
                  "back": QtGui.QIcon("%s/back.png" % DIRECTORIES["icon_location"]),
                  "left": QtGui.QIcon("%s/left-icon.png" % DIRECTORIES["icon_location"]),
                  }
    self.ui.groupBoxEquations.hide()
    self.__makeEmptyDataStructures()

  def __makeEquationDictionary(self):
    for var_ID in self.variables:
      for eq_ID in self.variables[var_ID]["equations"]:
        self.equation_dictionary[eq_ID] = (var_ID, self.variables[var_ID]["equations"][eq_ID])

  def __makeEmptyDataStructures(self):

    empty_equation_assignment = EquationAssignment()

    object_keys_networks = self.ontology_container.object_key_list_networks
    object_keys_intra = self.ontology_container.object_key_list_intra
    object_keys_inter = self.ontology_container.object_key_list_inter

    # get already defined assignments
    for object in object_keys_networks + object_keys_intra + object_keys_inter:
      empty_equation_assignment[object] = set()
      if object in self.equation_assignment:
        empty_equation_assignment[object] = self.equation_assignment[object]

    self.equation_assignment = empty_equation_assignment

    self.node_table_objects = self.__makeTable("node", self.ui.tableNodes,
                                               self.ontology_container.object_key_list_networks)
    self.arc_table_objects = self.__makeTable("arc", self.ui.tableArcs,
                                              self.ontology_container.object_key_list_networks)
    self.intra_table_objects = self.__makeTable("intra", self.ui.tableIntrafaces,
                                                self.ontology_container.object_key_list_intra)
    self.inter_table_objects = self.__makeTable("inter", self.ui.tableInterfaces,
                                                self.ontology_container.object_key_list_inter)

  def __makeTable(self, what, ui_table, object_list):
    """
    generate tables
    """
    t = ui_table
    row = t.rowCount()
    selector = {}
    # RULE: the object key is a tuple with the second element indicating what it is (node, arce, intra, inter)
    for object in object_list:
      if what == object[1]:
        t.setRowCount(row + 1)
        column = 0
        for item in object:
          if item != what:
            self.__setItem(t, row, column, item)
            column += 1
        selector[row] = object
        item = self.__setItem(t, row, column, "edit", icon=self.icons["edit"])
        row += 1
    self.__resize(t)
    return selector

  def __resize(self, tab):
    tab.resizeColumnsToContents()
    t = self.__tabSizeHint(tab)
    x = t.width()
    s = QtCore.QSize()
    s.setWidth(x)
    s.setHeight(tab.height())
    tab.resize(s)

  def __tabSizeHint(self, tab):
    width = 0
    for i in range(tab.columnCount()):
      width += tab.columnWidth(i)

    width += tab.verticalHeader().sizeHint().width()

    width += tab.verticalScrollBar().sizeHint().width()
    width += tab.frameWidth() * 2

    height = 0
    for i in range(tab.rowCount()):
      height += tab.rowHeight(i)
    height += tab.horizontalHeader().sizeHint().height()
    height += tab.horizontalScrollBar().sizeHint().width()
    height += tab.frameWidth() * 2

    return QtCore.QSize(width, min(height, MAX_HEIGHT))

  def __setItem(self, table_widget, row, col, text, icon=None):
    item = QtGui.QTableWidgetItem()

    if icon:
      item.setIcon(icon)
      item.setTextAlignment(QtCore.Qt.AlignHCenter)
    else:
      item.setText(text)
    table_widget.setItem(row, col, item)
    item.setFlags(QtCore.Qt.ItemIsEnabled)
    return item

  def __hideRadioSelectors(self, selector_list):
    for s in selector_list:
      if s in self.radio_selectors:
        self.radio_selectors[s].hide()

  def __showRadioSelectors(self, selector_list):
    for s in selector_list:
      if s in self.radio_selectors:
        self.radio_selectors[s].show()

  def __makeAndAddRadioSelector(self, group_name, what, receiver, index, layout, autoexclusive=True):
    radio_selector = RadioSelector()
    list_of_choices = []
    counter = 0
    cleanLayout(layout)
    layout.addWidget(radio_selector)
    for item in what:
      list_of_choices.append((str(counter), item, receiver))  # token is the string of the counter
      counter += 1
    radio_selector.addListOfChoices(group_name, list_of_choices, index, autoexclusive=autoexclusive)
    return radio_selector

  def __makeNodeVariableClassList(self):
    # RULE: only those that apply to the current network
    var_class_list = sorted(self.ontology_tree[self.current_node_network]["behaviour"]["node"])

    # RULE: first variables must be port variable
    if self.equation_assignment[self.selected_node_key] == set():
      var_class_list_with_port_variables = self.ontology_container.rules["variable_classes_having_port_variables"]
      var_classes = sorted(set(var_class_list).intersection(set(var_class_list_with_port_variables)))
    else:
      var_classes = var_class_list

    self.ui.comboBoxNodeVariableClasses.clear()
    self.ui.comboBoxNodeVariableClasses.addItems(var_classes)

  def __makeArcVariableClassList(self):
    var_class_list = self.ontology_tree[self.current_arc_network]["behaviour"]["arc"]
    self.ui.comboBoxArcVariableClasses.clear()
    self.ui.comboBoxArcVariableClasses.addItems(var_class_list)

  def __makeInterfaceVariableClassList(self):
    interface_record_def = Interface(None, None, None, self.current_interface_variable_class)
    var_class_list = interface_record_def["internal_variable_classes"]
    self.ui.comboBoxInterfacesVariableClasses.clear()
    self.ui.comboBoxInterfacesVariableClasses.addItems(var_class_list)

  def __makeEquationList(self):
    equation_list = {}
    for eq_ID in self.equation_dictionary:
      var_ID, equation = self.equation_dictionary[eq_ID]
      # print(var_ID, eq_ID, equation)
      if self.current_node_network == equation["network"]:
        var_class = self.variables[var_ID]["type"]
        if var_class == "state":
          equation_list[eq_ID] = (var_ID, var_class, equation["rhs"])

    for eq_ID in equation_list:
      print(eq_ID, " -- ", equation_list[eq_ID])

    if len(equation_list) > 0:
      rendered_expressions = {}
      radio_item_list = []
      self.inverse_dictionary = {}  # hash: label, value: (var_ID, eq_ID)
      for eq_ID in equation_list:
        rendered_expressions[eq_ID] = renderExpressionFromGlobalIDToInternal(equation_list[eq_ID][2], self.variables,
                                                                             self.indices)
        var_ID = equation_list[eq_ID][0]
        rendered_variable = self.variables[equation_list[eq_ID][0]]["aliases"]["internal_code"]
        print(rendered_variable, rendered_expressions[eq_ID])
        s = "%s := %s" % (rendered_variable, rendered_expressions[eq_ID])
        radio_item_list.append(s)
        self.inverse_dictionary[s] = (var_ID, eq_ID)
      self.radio = UI_RadioSelector(radio_item_list, [], allowed=1)
      self.radio.setWindowTitle("select one")
      self.radio.rejected.connect(self.__gotState)
      self.radio.exec_()

  def __gotState(self):
    list = self.radio.getMarked()
    var_ID, eq_ID = self.inverse_dictionary[list[0]]
    print("debugging -- exited", list, var_ID, eq_ID)
    # rel_vars, rel_equs, rel_vars_text, rel_equs_text = simulateDeletion(self.variables, var_ID, self.indices)
    # rel_equs, rel_equs_text = self.workTree(var_ID)
    # print("debugging equs", rel_equs )
    # print("debugging equs", rel_equs_text )

    var_equ_tree = VariableEquationTree(var_ID)
    sel_equs = []
    self.makeTree(var_equ_tree,0,sel_equs,var_ID)
    print("debugging tree", var_equ_tree["ID_tree"])
    print("debugging tree variables", var_equ_tree["variable"])
    print("debugging tree equations", var_equ_tree["equation"])

    var_labels = {}
    equ_labels = {}
    for var_ID in self.variables:
      var_labels[var_ID] = self.variables[var_ID]["aliases"]["internal_code"]
      for eq_ID in self.variables[var_ID]["equations"]:
        lhs, incidence_list = self.incidence_dictionary[eq_ID]
        rhs = self.variables[lhs]["equations"][eq_ID]["rhs"]
        equ_labels[eq_ID] = renderExpressionFromGlobalIDToInternal(rhs, variables=self.variables, indices=self.indices)


    var_equ_tree.graphMe(self.ontology_name, var_labels, equ_labels)

  def makeTree(self, var_eq_tree, parent_var_ID, d_equs, var_ID):
    """
    interate to find all equations and variables
    :tree: bipartite var/eq tree
    :param d_equs: set of equations to be deleted - list of IDs (integers)
    :param var_ID: variable ID (integer)
    :return: None
    """

    for eq_id in self.inv_incidence_dictionary[var_ID]:
      if eq_id not in d_equs:
        d_equs.append(eq_id)
        equ_node_ID = var_eq_tree.addNode("equation", parent_var_ID)
        var_node_ID = var_eq_tree.addNode("variable", equ_node_ID)
        lhs, incidence_list = self.incidence_dictionary[eq_id]
        self.makeTree(var_eq_tree, var_node_ID, d_equs, lhs)


  def workTree(self, var_ID):
    d_equs = [] #set()

    # - key: equation_ID(integer)
    # - value: (lhs - variable_ID, rhs - incidence list (integers) )

    self.incidence_dictionary, self.inv_incidence_dictionary = self.makeIncidenceDictionaries()
    self.reduceVars(d_equs, var_ID)

    d_equs_text = ""
    for eq_ID in d_equs:
      lhs, incidence_list = self.incidence_dictionary[eq_ID]
      rhs = self.variables[lhs]["equations"][eq_ID]["rhs"]
      rhs_rendered = renderExpressionFromGlobalIDToInternal(rhs, variables=self.variables, indices=self.indices)
      lhs_rendered = self.variables[lhs]["aliases"]["internal_code"]
      d_equs_text += "\n%s :: %s :=  %s" %(eq_ID, lhs_rendered, rhs_rendered)
    return d_equs, d_equs_text


  def reduceVars(self, d_equs, var_ID):
    """
    interate to find all equations and variables to be deleted
    in most of the cases everything is deleted except the state variables
      because the equations are all dependent on each other.
    :param inv_incidence_dictionary:  "inverse" incidence dictionary
    :param variables: variables (dictionary)
    :param incidence_dictionary: incidence dictionary (var, incidence list)
    :param d_vars: set of variables to be deleted - list of IDs (integers)
    :param d_equs: set of equations to be deleted - list of IDs (integers)
    :param var_ID: variable ID (integer)
    :return: None
    """

    for eq_id in self.inv_incidence_dictionary[var_ID]:
      if eq_id not in d_equs:
        d_equs.append(eq_id)
        lhs, incidence_list = self.incidence_dictionary[eq_id]
        self.reduceVars(d_equs, lhs)

  def makeIncidenceDictionaries(self):
    """
    variables may be defined by several equations

    :param variables: variable dictionary with integrated equation dictionary
    :param expression_network: network on which the expression is defined
    :return: incidence_dictionary
              - key: equation_ID (integer)
              - value: (lhs-variable_ID, rhs-incidence list (integers) )
             inverse incidence matrix as dictionary
              - key : variable ID (integer)
              - value: list of equations (integer)
    """
    incidence_dictionary = {}
    # inv_incidence_dictionary_ = {v: set() for v in self.variables.keys()}
    inv_incidence_dictionary = {v: [] for v in self.variables.keys()}
    for v in self.variables:
      try:
        equations = self.variables[v].equations  # variables as class Variables
      except:
        equations = self.variables[v]["equations"]  # variables from variable dict, the variable file format
      for e in equations:
        if e in [97,63]:
          print("debugging", e)
        inc_list = equations[e]["incidence_list"] #self.makeIncidentList(equations[e]["rhs"])
        # c_ = copy(inc_list)
        # c__ = copy(inc_list)
        incidence_dictionary[e] = (v, inc_list)
        inv_incidence_dictionary[v].append(inc_list)


        # for i in inc_list:
        #   inv_incidence_dictionary_[int(i)].add(e)
        # equations[e]["incidence_list"] = c__

    # inv_incidence_dictionary = {}
    # for v in inv_incidence_dictionary
    #   inv_incidence_dictionary[v] = sorted(list(inv_incidence_dictionary_[var_ID]))

    return incidence_dictionary, inv_incidence_dictionary

  def makeIncidentList(self, equation_ID_coded_string):
    """
    make incidence list for a ID-coded expression
    extracts all variables into a list
    :param equation_ID_coded_string:
    :return: sorted incidence list of variable IDs [integers
    """
    incidence_list = []
    splited = equation_ID_coded_string.split(ID_spacer)
    for i in splited:
      test_string = ID_spacer + i
      # print("debugging", test_string, ID_delimiter["variable"])
      if test_string[0:2] == ID_delimiter["variable"][0:2]:
        inc = i.strip(ID_delimiter["variable"])
        incidence_list.append(inc)
    return sorted(set(incidence_list))

  def __resetEquation(self):
    self.radio_selectors["equations"].uncheckGroup("equations")

  def __makeEquations(self, variable_class, selection, autoexclusive=True):

    self.current_equation_IDs = {}
    index = 1

    equations = [M_None]
    self.current_equation_IDs[0] = None

    indices = self.ontology_container.indices

    equation_ID_list = []
    for var_ID in self.variables:
      var = self.variables[var_ID]
      if var["network"] == self.current_node_network:
        if var["type"] == variable_class:
          lhs = var["label"]
          for eq_ID in var["equations"]:
            equ = var["equations"][eq_ID]
            if equ["network"] == self.current_node_network:
              expression = equ["rhs"]
              rhs = renderExpressionFromGlobalIDToInternal(expression, self.variables, indices)
              entry = "%s        %s = %s" % (eq_ID, lhs, rhs)
              equations.append(entry)
              self.current_equation_IDs[index] = eq_ID
              index += 1

        # eqs = self.variables[var_ID]["equations"] #["equation_list"]
        # equation_ID_list.extend(eqs)

    # for ID in equation_ID_list:
    #   lhs = self.equations[ID]["lhs"]
    #   rhs = self.equations[ID]["rhs"]
    #   entry = "%s        %s = %s" % (ID, lhs, rhs)
    #   equations.append(entry)
    #   self.current_equation_IDs[index] = ID
    #   index += 1

    self.radio_selectors["equations"] = self.__makeAndAddRadioSelector("equations",
                                                                       equations,
                                                                       self.radioReceiverEquations,
                                                                       selection,
                                                                       self.ui.horizontalLayoutEquations,
                                                                       autoexclusive=autoexclusive)

    self.radio_selectors["equations"].show()
    self.ui.groupBoxEquations.show()

  def on_tableNodes_cellPressed(self, row, column):

    column = self.ui.tableNodes.columnCount() - 1
    self.node_indicator_item = self.__setItem(self.ui.tableNodes, row, column, "", icon=self.icons["left"])

    if self.last_node_coordinate:
      last_row, last_column = self.last_node_coordinate
      self.__setItem(self.ui.tableNodes, last_row, last_column, "", icon=self.icons["edit"])
    self.last_node_coordinate = row, column

    self.current_component = "node"
    self.previous_node_network = self.current_node_network
    self.selected_node_key = self.node_table_objects[row]
    self.current_node_network = self.selected_node_key[0]

    self.__makeEquationList()
    # self.__makeNodeVariableClassList()
    #
    # self.current_node_variable_class = self.ui.comboBoxNodeVariableClasses.currentText()

  def on_tableArcs_cellPressed(self, row, column):

    column = self.ui.tableArcs.columnCount() - 1
    self.arc_indicator_item = self.__setItem(self.ui.tableArcs, row, column, "", icon=self.icons["left"])

    if self.last_arc_coordinate:
      last_row, last_column = self.last_arc_coordinate
      self.__setItem(self.ui.tableArcs, last_row, last_column, "", icon=self.icons["edit"])
    self.last_arc_coordinate = row, column

    self.current_component = "arc"
    self.previous_arc_network = self.current_arc_network
    self.selected_arc_key = self.arc_table_objects[row]
    self.current_arc_network = self.selected_arc_key[0]

    self.__makeArcVariableClassList()

    self.current_arc_variable_class = self.ui.comboBoxArcVariableClasses.currentText()

  def on_tableInterfaces_cellPressed(self, row, column):

    column = self.ui.tableInterfaces.columnCount() - 1
    self.inter_indicator_item = self.__setItem(self.ui.tableInterfaces, row, column, "", icon=self.icons["left"])

    if self.last_inter_coordinate:
      last_row, last_column = self.last_inter_coordinate
      self.__setItem(self.ui.tableInterfaces, last_row, last_column, "", icon=self.icons["edit"])
    self.last_inter_coordinate = row, column

    self.current_component = "inter"
    self.previous_interface_network = self.current_interface_network
    self.selected_interface_key = self.inter_table_objects[row]
    self.current_interface_network = self.selected_interface_key[0]

    self.__makeInterfaceVariableClassList()

    self.current_inface_variable_class = self.ui.comboBoxinterfaceVariableClasses.currentText()

  @QtCore.pyqtSignature("int")
  def on_tabWidget_currentChanged(self, index):
    # print("index: ", index)
    if index == 0:
      self.current_component = "node"
      self.ui.groupBoxEquations.hide()
    elif index == 1:
      self.current_component = "arc"
      self.ui.groupBoxEquations.hide()
    elif index == 2:
      self.current_component = "interface"
      self.ui.groupBoxEquations.hide()
    else:
      print(">>>>> tab change -- something went wrong")

  def on_pushNodeSave_pressed(self):
    print("write file")
    self.ontology_container.writeMe()

  def on_pushArcSave_pressed(self):
    print("write file")
    self.ontology_container.writeMe()

  def on_pushInterfaceSave_pressed(self):
    print("write file")
    self.ontology_container.writeMe()

  @QtCore.pyqtSignature('QString')
  def on_comboBoxNodeVariableClasses_currentIndexChanged(self, entry):
    # print("debugging got node class entry :", entry)
    self.current_node_variable_class = entry
    self.__makeEquations(entry, -1)

  @QtCore.pyqtSignature('QString')
  def on_comboBoxArcVariableClasses_currentIndexChanged(self, entry):
    print(" got arc class entry :", entry)
    self.current_arc_variable_class = entry
    self.__makeEquations(entry, -1)

  @QtCore.pyqtSignature('QString')
  def on_comboBoxInterfaceVariableClasses_currentIndexChanged(self, entry):
    print(" got interface class entry :", entry)
    self.current_interface_variable_class = entry
    self.__makeEquations(entry, -1, autoexclusive=False)

  def radioReceiverEquations(self, group_name, index_str, equation_index, logical_value):
    index = int(index_str)
    # print("radioReceiverEquations :", group_name, index, equation_index, logical_value)
    self.current_equation = self.current_equation_IDs[index]  # equation_index
    if self.current_component == "node":
      key = self.selected_node_key
      if index == 0:
        variable_class = M_None
        equation = -1
      else:
        variable_class = self.current_node_variable_class
        equation = self.current_equation

      self.equation_assignment[key].add(equation)
      print("debugging")


    elif self.current_component == "arc":
      key = self.selected_arc_key
      if index == 0:
        variable_class = M_None
        equation = -1
      else:
        variable_class = self.current_arc_variable_class
        equation = self.current_equation
      self.equation_assignment["arc"][key] = self.current_arc_network, equation
      # print("arc :", self.equation_assignment["arc"])
      self.arc_items[self.last_arc_item[0], 5].setText(str(equation))
      self.arc_items[self.last_arc_item[0], 3].setText(variable_class)
      self.__resize(self.ui.tableArcs)
    elif self.current_component == "interface":
      key = self.selected_interface_key
    else:
      print(" no such component:", self.current_component)
