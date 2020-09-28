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
__since__ = "24.09.2020"
__license__ = "GPL planned -- until further notice for Bio4Fuel & MarketPlace internal use only"
__version__ = "8.01"
__email__ = "heinz.preisig@chemeng.ntnu.no"
__status__ = "beta"

from PyQt5 import QtWidgets

from Common.common_resources import getOntologyName
from Common.common_resources import TEMPLATE_NODE_OBJECT
from Common.ontology_container import OntologyContainer
from Common.qt_resources import cleanLayout
from Common.resource_initialisation import checkAndFixResources
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.ui_radio_selector_w_sroll_impl import UI_RadioSelector
from OntologyBuilder.OntologyEquationAssignmentEditor.assign_equations_gui import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import DotGraphVariableEquations
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeIncidenceDictionaries


class UI_EditorEquationAssignment(QtWidgets.QMainWindow):
  rules = {  #RULE : what variable class in what network for nodes and arcs
          "nodes": {
                  "physical": "state",
                  "control" : "state",
                  "intra"   : "state",
                  "inter"   : "transform",
                  },
          "arcs" : {
                  "physical": "transport",
                  "control" : "dataflow",
                  "inter"   : "transform"
                  }
          }


  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ontology_name = getOntologyName(task="task_entity_generation")
    self.ontology_dir = DIRECTORIES["ontology_location"] % self.ontology_name
    self.ontology_file = FILES["ontology_file"] % self.ontology_name

    checkAndFixResources(self.ontology_name, stage="ontology_stage_2")

    self.ontology_container = OntologyContainer(self.ontology_name)
    self.incidence_dictionary, self.inv_incidence_dictionary = makeIncidenceDictionaries(
            self.ontology_container.variables)

    self.equation_dictionary = {}
    self.__makeEquationDictionary()

    self.radio_selectors = {}
    self.__makeCombosNetworks()

    self.current_equation_IDs = {}  # hash: radio button index     value: equation_ID_str
    self.ui.tabWidget.setCurrentIndex(0)
    self.current_tab = 0
    self.tabs = ["node", "arc", "intra", "inter"]

    self.selected_node = None
    self.selected_arc = None
    self.selected_intra = None
    self.selected_inter = None
    self.selected_arc_network = None
    self.selected_node_network = None

    self.__makeEquationList()

  def __makeCombosNetworks(self):
    networks = self.ontology_container.list_leave_networks
    list_inter_branches = self.ontology_container.list_inter_branches
    self.ui.comboNodeNetworks.addItems(list_inter_branches)
    self.ui.comboArcNetworks.addItems(list_inter_branches)
    pass

  def on_comboNodeNetworks_currentTextChanged(self, network):
    print("debugging -- node network", network)
    self.selected_node_network = network
    self.__makeNodeSelector()

  def on_comboArcNetworks_currentTextChanged(self, network):
    print("debugging -- arc network", network)
    self.selected_arc_network = network
    self.__makeArcSelector()

  def __makeNodeSelector(self):
    network_node_list = self.ontology_container.list_node_objects_on_networks_with_tokens[self.selected_node_network]

    reduced_network_node_list = []
    for i in network_node_list:
      if "constant" not in i:   #RULE: reservoirs (time-scale constant) have no state
        reduced_network_node_list.append(i)
    self.radio_selectors["networks"] = self.__makeSelector(reduced_network_node_list,
                                                           self.radioReceiverNodes,
                                                           -1,  # RULE: none selected initially
                                                           self.ui.verticalLayoutNodeTop)

  def __makeArcSelector(self):
    network_arc_list = self.ontology_container.list_arc_objects_on_networks[self.selected_arc_network]

    self.radio_selectors["arcs"] = self.__makeSelector(network_arc_list,
                                                        self.radioReceiverArcs,
                                                        -1,
                                                        self.ui.verticalLayoutArcTop)


  def __makeEquationDictionary(self):
    for var_ID in self.ontology_container.variables:
      for eq_ID in self.ontology_container.variables[var_ID]["equations"]:
        self.equation_dictionary[eq_ID] = (var_ID, self.ontology_container.variables[var_ID]["equations"][eq_ID])

  # def __makeEmptyDataStructures(self):
  #
  #   network_node_list = self.ontology_container.list_network_node_objects_with_token
  #   arc_list = self.ontology_container.list_arc_objects
  #   intra_node_list = self.ontology_container.list_intra_node_objects_with_token
  #   inter_node_list = self.ontology_container.list_inter_node_objects
  #
  #   reduced_network_node_list = []
  #   for i in network_node_list:
  #     if "constant" not in i:
  #       reduced_network_node_list.append(i)
  #
  #   self.radio_selectors["networks"] = self.__makeSelector(reduced_network_node_list,
  #                                                          self.radioReceiverObject,
  #                                                          -1,  # RULE: none selected initially
  #                                                          # self.ui.frameNodeTop,
  #                                                          self.ui.verticalLayoutNodeTop)
  #
  #   self.radio_selectors["arcs"] = self.__makeSelector(arc_list,
  #                                                      self.radioReceiverObject,
  #                                                      -1,  # RULE: none selected initially
  #                                                      # self.ui.frameArcTop,
  #                                                      self.ui.verticalLayoutArcTop)
  #
  #   self.radio_selectors["intra"] = self.__makeSelector(intra_node_list,
  #                                                       self.radioReceiverObject,
  #                                                       -1,  # RULE: none selected initially
  #                                                       # self.ui.frameIntraTop,
  #                                                       self.ui.verticalLayoutIntraTop)

  @staticmethod
  def __makeSelector(what, receiver, index, layout, allowed=1):

    height = layout.parent().size().height()
    radio_selector = UI_RadioSelector(what, [index], allowed=allowed, maxheight=height)
    radio_selector.newSelection.connect(receiver)
    cleanLayout(layout)
    layout.addWidget(radio_selector)

    return radio_selector

  def on_tabWidget_currentChanged(self, index):
    print("debugging -- new tab", index)
    self.current_tab = index

  def radioReceiverNodes(self, checked):
    if checked:
      print("debugging -- nodes", checked)
      self.selected_node_network = checked
      self.__makeNodeEquationSelector()
      pass

  def __makeNodeEquationSelector(self):
    # item_list = self.rendered_equation[self.selected_node_network][]
    pass

  def radioReceiverArcs(self, token_class, token, token_string, toggle):

    if toggle:
      print("debugging -- arcs")
      pass

  def radioReceiverIntra(self, token_class, token, token_string, toggle):

    if toggle:
      print("debugging -- intra")
      pass

  def radioReceiverInter(self, token_class, token, token_string, toggle):

    if toggle:
      print("debugging -- inter")
      pass

  def radioReceiverEquations(self, checked):
    print("debugging -- node equations checked", checked)
    pass

  def __makeEquationList(self):

    # variable_classes=set()
    # [variable_classes.add(i) for nw in self.ontology_container.variable_types_on_networks
    #  for i in self.ontology_container.variable_types_on_networks[nw]]
    # [variable_classes.add(i) for nw in self.ontology_container.variable_types_on_intrafaces
    #  for i in self.ontology_container.variable_types_on_networks[nw]]
    # [variable_classes.add(i) for nw in self.ontology_container.variable_types_on_interfaces
    #  for i in self.ontology_container.variable_types_on_networks[nw]]

    # variable_classes = self.rules
    self.inverse_dictionary = {}  # hash: label, value: (var_ID, eq_ID)

    equation_list = {}
    for component in self.rules:
      for nw in self.rules[component]:
        equation_list[nw] = {}
        for var_class in self.rules[component][nw]:
          equation_list[nw][var_class] = {}
          self.inverse_dictionary[var_class] = {}

        for eq_ID in self.equation_dictionary:
          var_ID, equation = self.equation_dictionary[eq_ID]
          for var_class in self.rules[component][nw]:
            equation_list[nw][var_class][eq_ID] = (var_ID, var_class, equation["rhs"], equation["network"])

        # for eq_ID in equation_list[nw]:
        #   print(eq_ID, " -- ", equation_list[nw][eq_ID])

        if len(equation_list[nw]) > 0:
          rendered_equation = {}  # hash :: variable ID
          rendered_expressions = {}
          radio_item_list = []
          for var_class in self.rules[component][nw]:
            rendered_expressions[var_class] = {}
            for eq_ID in equation_list[nw][var_class]:
              rendered_expressions[var_class][eq_ID] = renderExpressionFromGlobalIDToInternal(
                      equation_list[nw][var_class][eq_ID][2],
                      self.ontology_container.variables,
                      self.ontology_container.indices)

              var_ID = equation_list[nw][var_class][eq_ID][0]
              network = equation_list[nw][var_class][eq_ID][3]
              if network not in rendered_equation:
                rendered_equation[network] = {}
              if var_class not in rendered_equation[network]:
                rendered_equation[network][var_class] = {}
              rendered_variable = self.ontology_container.variables[equation_list[nw][var_class][eq_ID][0]]["aliases"][
                "internal_code"]

              # print("debugging -- rendered equation info", rendered_variable, rendered_expressions[var_class][eq_ID])
              s = "%s := %s" % (rendered_variable, rendered_expressions[var_class][eq_ID])
              # radio_item_list.append(s)

              if var_ID not in rendered_equation[network][var_class]:
                rendered_equation[network][var_class][var_ID] = []
              rendered_equation[network][var_class][var_ID].append(s)

              self.inverse_dictionary[s] = (var_ID, eq_ID)
      self.rendered_equation = rendered_equation
      #
      # self.radio_selectors["nodes"] = self.__makeSelector(radio_item_list,
      #                                                     self.radioReceiverEquations,
      #                                                     -1,  # RULE: none selected initially
      #                                                     self.ui.verticalLayoutNodeBottom,
      #                                                     )
      print("debugging -- end of make equation list")

  def __gotState(self):
    list = self.radio.getMarked()
    var_ID, eq_ID = self.inverse_dictionary[list[0]]
    print("debugging -- exited", list, var_ID, eq_ID)
    var_equ_tree = DotGraphVariableEquations(self.ontology_container.variables, self.ontology_container.indices, var_ID,
                                             self.ontology_name)
    print("debugging -- dotgrap done")
    buddies = set()
    for var_ID in var_equ_tree.tree.IDs:
      o, str_ID = var_ID.split("_")
      ID = int(str_ID)
      if o == "variable":
        network = self.ontology_container.variables[ID]['network']
        if network in self.ontology_container.list_leave_networks:
          buddies.add((ID, network))

        # print("debugging --", network)
      # print("debugging -- buddies", self.buddies)

    nw, component, dynamics, nature, token = self.selected_node_key
    node_object = TEMPLATE_NODE_OBJECT % (dynamics, nature)

    self.ontology_container.equation_assignment[node_object] = {
            "tree"   : var_equ_tree.tree.tree,
            "IDs"    : var_equ_tree.tree.IDs,
            "nodes"  : var_equ_tree.tree.nodes,
            "buddies": buddies
            }

    print("debugging -- end of buddies")
