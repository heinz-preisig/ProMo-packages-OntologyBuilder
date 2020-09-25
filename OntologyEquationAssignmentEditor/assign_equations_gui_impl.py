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

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getOntologyName
from Common.common_resources import M_None, TEMPLATE_NODE_OBJECT
from Common.ontology_container import OntologyContainer
from Common.qt_resources import cleanLayout
from Common.radio_selector_impl import RadioSelector
from Common.record_definitions import EquationAssignment
from Common.record_definitions import Interface
from Common.resource_initialisation import checkAndFixResources
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.ui_radio_selector_w_sroll_impl import UI_RadioSelector
from OntologyBuilder.OntologyEquationAssignmentEditor.assign_equations_gui import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import DotGraphVariableEquations
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeIncidenceDictionaries



class UI_EditorEquationAssignment(QtWidgets.QMainWindow):

  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    self.ontology_name = getOntologyName(task="task_entity_generation")
    self.ontology_dir = DIRECTORIES["ontology_location"] % self.ontology_name
    self.ontology_file = FILES["ontology_file"] % self.ontology_name

    checkAndFixResources(self.ontology_name, stage="ontology_stage_2")

    self.ontology_container = OntologyContainer(self.ontology_name)
    self.incidence_dictionary, self.inv_incidence_dictionary = makeIncidenceDictionaries(self.ontology_container.variables)

    self.equation_dictionary = {}
    self.__makeEquationDictionary()

    self.radio_selectors = {}


    self.current_equation_IDs = {}  # hash: radio button index     value: equation_ID_str
    self.ui.tabWidget.setCurrentIndex(0)
    self.current_tab = 0
    self.tabs = ["node", "arc", "intra", "inter"]

    self.selected_node = None
    self.selected_arc = None
    self.selected_intra = None
    self.selected_inter = None



    # self.current_node_network = None
    # self.previous_node_network = None
    # self.current_node_variable_class = None
    # self.selected_node_key = None
    # self.current_node_equation = None
    #
    # self.current_arc_network = None
    # self.previous_arc_network = None
    # self.current_arc_variable_class = None
    # self.selected_arc_key = None
    # self.current_arc_equation = None
    #
    # self.current_interface_network = None
    # self.previous_interface_network = None
    # self.current_interface_variable_class = None
    # self.selected_interface_key = None
    # self.current_interface_equation = None
    #
    # self.node_indicator_item = None
    # self.last_node_coordinate = None
    # self.arc_indicator_item = None
    # self.last_arc_coordinate = None
    # self.intra_indicator_item = None
    # self.last_interface_coordinate = None
    # self.inter_indicator_item = None
    # self.last_inter_coordinate = None
    #
    # self.node_table_objects = {}
    # self.arc_table_objects = {}
    # self.intra_table_objects = {}
    # self.inter_table_objects = {}

    # icons
    # self.icons = {
    #         "edit": QtGui.QIcon("%s/edit.png" % DIRECTORIES["icon_location"]),
    #         "OK"  : QtGui.QIcon("%s/accept.png" % DIRECTORIES["icon_location"]),
    #         "back": QtGui.QIcon("%s/back.png" % DIRECTORIES["icon_location"]),
    #         "left": QtGui.QIcon("%s/left-icon.png" % DIRECTORIES["icon_location"]),
    #         }

    self.__makeEmptyDataStructures()

  def __makeEquationDictionary(self):
    for var_ID in self.ontology_container.variables:
      for eq_ID in self.ontology_container.variables[var_ID]["equations"]:
        self.equation_dictionary[eq_ID] = (var_ID, self.ontology_container.variables[var_ID]["equations"][eq_ID])

  def __makeEmptyDataStructures(self):

    # empty_equation_assignment = EquationAssignment()

    # object_keys_networks = self.ontology_container.object_key_list_networks
    # object_keys_intra = self.ontology_container.object_key_list_intra
    # object_keys_inter = self.ontology_container.object_key_list_inter
    #
    # # get already defined assignments
    # for object in object_keys_networks + object_keys_intra + object_keys_inter:
    #   empty_equation_assignment[object] = set()
    #   if object in self.equation_assignment:
    #     empty_equation_assignment[object] = self.equation_assignment[object]
    #
    # self.equation_assignment = empty_equation_assignment

    network_node_list = self.ontology_container.list_network_node_objects_with_token
    arc_list = self.ontology_container.list_arc_objects
    intra_node_list = self.ontology_container.list_intra_node_objects_with_token
    inter_node_list = self.ontology_container.list_inter_node_objects

    reduced_network_node_list = []
    for i in network_node_list:
      if "constant" not in i:
        reduced_network_node_list.append(i)

    self.radio_selectors["networks"] = self.__makeAndAddSelector(reduced_network_node_list,
                                                                 self.radioReceiverObject,
                                                                 -1,  # RULE: none selected initially
                                                                 self.ui.frameNodeTop,
                                                                 self.ui.verticalLayoutNodeTop)

    self.radio_selectors["arcs"] = self.__makeAndAddSelector(arc_list,
                                                                 self.radioReceiverArcs,
                                                                 -1,  # RULE: none selected initially
                                                                 self.ui.frameArcTop,
                                                                 self.ui.verticalLayoutArcTop)

    self.radio_selectors["intra"] = self.__makeAndAddSelector(intra_node_list,
                                                                 self.radioReceiverIntra,
                                                                 -1,  # RULE: none selected initially
                                                                 self.ui.frameIntraTop,
                                                                 self.ui.verticalLayoutIntraTop)

    self.radio_selectors["inter"] = self.__makeAndAddSelector(inter_node_list,
                                                                 self.radioReceiverInter,
                                                                 -1,  # RULE: none selected initially
                                                                 self.ui.frameInterTop,
                                                                 self.ui.verticalLayoutInterTop,
                                                                 )


  @staticmethod
  def __makeAndAddSelector(what, receiver, index, frame, layout,  allowed=1):
    list_of_choices = []
    counter = 0
    for item in what:
      list_of_choices.append((str(counter), item, receiver))
      counter += 1

    size = frame.size()
    height = size.height()
    radio_selector = UI_RadioSelector(what,[index],allowed=allowed, maxheight=height)
    radio_selector.newSelection.connect(receiver)
    # radio_selector = RadioSelector()
    # radio_selector.addListOfChoices(group_name, list_of_choices, index, autoexclusive=autoexclusive)

    layout.addWidget(radio_selector)
    return radio_selector

  def on_tabWidget_currentChanged(self, index):
    print("debugging -- new tab", index)
    self.current_tab = index

  def radioReceiverObject(self, checked):
    # if toggle:
      print("debugging -- nodes", checked)
      self.__makeEquationList()
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
    equation_list = {}
    for eq_ID in self.equation_dictionary:
      var_ID, equation = self.equation_dictionary[eq_ID]
      # print(var_ID, eq_ID, equation)
      # if self.current_node_network == equation["network"]:
      var_class = self.ontology_container.variables[var_ID]["type"]
      if var_class == "state":
        equation_list[eq_ID] = (var_ID, var_class, equation["rhs"])

    for eq_ID in equation_list:
      print(eq_ID, " -- ", equation_list[eq_ID])

    if len(equation_list) > 0:
      rendered_expressions = {}
      radio_item_list = []
      self.inverse_dictionary = {}  # hash: label, value: (var_ID, eq_ID)
      for eq_ID in equation_list:
        rendered_expressions[eq_ID] = renderExpressionFromGlobalIDToInternal(equation_list[eq_ID][2], self.ontology_container.variables,
                                                                             self.ontology_container.indices)
        var_ID = equation_list[eq_ID][0]
        rendered_variable = self.ontology_container.variables[equation_list[eq_ID][0]]["aliases"]["internal_code"]
        print("debugging -- rendered equation info", rendered_variable, rendered_expressions[eq_ID])
        s = "%s := %s" % (rendered_variable, rendered_expressions[eq_ID])
        radio_item_list.append(s)
        self.inverse_dictionary[s] = (var_ID, eq_ID)

      self.radio_selectors["nodes"] = self.__makeAndAddSelector(radio_item_list,
                                                                self.radioReceiverEquations,
                                                                -1,  # RULE: none selected initially
                                                                self.ui.frameNodeBottom,
                                                                self.ui.verticalLayoutNodeBottom,
                                                                )
      # self.radio = UI_RadioSelector(radio_item_list, [], allowed=1)
      # self.radio.setWindowTitle("select one")
      # self.radio.rejected.connect(self.__gotState)
      # self.radio.exec_()

  def __gotState(self):
    list = self.radio.getMarked()
    var_ID, eq_ID = self.inverse_dictionary[list[0]]
    print("debugging -- exited", list, var_ID, eq_ID)
    var_equ_tree = DotGraphVariableEquations(self.ontology_container.variables, self.ontology_container.indices, var_ID, self.ontology_name)
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
    node_object = TEMPLATE_NODE_OBJECT %(dynamics, nature)

    self.ontology_container.equation_assignment[node_object] = {
            "tree"   : var_equ_tree.tree.tree,
            "IDs"    : var_equ_tree.tree.IDs,
            "nodes"  : var_equ_tree.tree.nodes,
            "buddies": buddies
            }

    print("debugging -- end of buddies")

