from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.common_resources import indexList
from Common.common_resources import putData
from Common.ui_string_dialog_impl import UI_String
from Common.ontology_container import OntologyContainer
from Common.qt_resources import clearLayout
from Common.record_definitions import EntityBehaviour
from Common.record_definitions import functionGetObjectsFromObjectStringID
from Common.record_definitions import functionMakeObjectStringID
from Common.resource_initialisation import checkAndFixResources
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.resources_icons import roundButton
from OntologyBuilder.BehaviourEditor.ui_behaviour_linker_editor import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import AnalyseBiPartiteGraph
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal

# RULE : what variable class in what network for nodes and arcs
# TODO: integrate into base ontology editor

rules = {
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

base_variant = "base"  # RULE: nomenclature for base case

# TODO: could be included into the interface as a choice

pixel_or_text = "text"  # NOTE: variable to set the mode


class Selector(QtCore.QObject):
  radio_signal = QtCore.pyqtSignal(str, int)

  def __init__(self, receiver, label_list, layout, mode="text", autoexclusive=False):
    super().__init__()
    self.labels = label_list
    self.layout = layout
    self.mode = mode
    self.autoexclusive = autoexclusive

    self.radios = {}
    # label_indices -- hash:enumeration:int - value:label:string
    # label_indices_inverse -- hash:label:string - value:enumeration:int
    self.label_indices, \
    self.label_indices_inverse = indexList(self.labels)

    self.makeSelector()
    self.radio_signal.connect(receiver)

  def getStrID(self, ID):
    return self.label_indices[ID]

  def getID(self, str_ID):
    return self.label_indices_inverse[str_ID]

  def makeSelector(self):
    if self.mode == "text":
      self.makeTextSelector()
    elif self.mode == "pixelled":
      self.makePixelSelector()
    else:
      raise

  def makeTextSelector(self):
    for label_ID in self.label_indices:
      label = self.labels[label_ID]
      self.radios[label_ID] = QtWidgets.QRadioButton(label)
      if self.autoexclusive:
        self.radios[label_ID].setAutoExclusive(False)
      self.layout.addWidget(self.radios[label_ID])
      self.radios[label_ID].toggled.connect(self.selector_toggled)
      # self.radios[label_ID].released.connect(self.selector_released)

  def makePixelSelector(self):

    for label_ID in self.label_indices:
      icon, label, size = self.labels[label_ID]
      # for (icon, label, size) in self.labels:
      label = QtWidgets.QLabel()
      self.radios[label_ID] = QtWidgets.QRadioButton(label)
      self.radios[label_ID].setIcon(icon)
      self.radios[label_ID].setIconSize(size)
      self.radios[label_ID].resize(0, 0)  # Note: not sure what I am doing here -- reduces gaps between

      if self.autoexclusive:
        self.radios[label_ID].setAutoExclusive(False)
      self.layout.addWidget(self.radios[label_ID])

      self.radios[label_ID].toggled.connect(self.selector_toggled)

  def showList(self, show):
    self.show_list = show
    self.showIt()

  def showIt(self):
    for ID in self.radios:
      self.radios[ID].setChecked(False)
      if ID not in self.show_list:
        self.radios[ID].hide()
      else:
        self.radios[ID].show()

  def reset(self):
    self.showList([])

  def selector_toggled(self, toggled):
    print("debugging -- toggled", toggled)
    if toggled:
      label, ID = self.getToggled()

      if ID >= 0:
        self.radio_signal.emit(label, ID)

  def getToggled(self):

    count = -1
    ID = -1
    str_label = None
    for label in self.radios:
      count += 1
      if self.radios[label].isChecked():
        # print("goit it :", label)
        str_label = str(label)
        ID = count

    return str_label, ID

  # def selector_released(self):
  #   print("debugging -- released radio button")


# class EntityBehaviour(dict):
#   def __init__(self, networks, entities):
#     for nw in networks:
#       self[nw] = {}
#       for entity in entities[nw]:
#         self[nw][entity] = {}
#         self[nw][entity]["base"] = None
#
#   def addVariant(self, network, entity, variant, data):
#     self[network][entity][variant] = data
#
#   def removeEntity(self, network, entity):
#     del self[network][entity]
#
#   def removeVariant(self, network, entity, variant):
#     del self[network][entity][variant]
#
#   def getRootVariableID(self):
#     pass
#
#
# class EntityBehaviourGraphs(EntityBehaviour):
#
#   def __init__(self, networks, entities):
#     super().__init__(networks, entities)


class MainWindowImpl(QtWidgets.QMainWindow):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.move(QtCore.QPoint(0, 0))

    roundButton(self.ui.pushButtonInformation, "info", tooltip="information")
    roundButton(self.ui.pushButtonSave, "save", tooltip="save entity behaviour")
    roundButton(self.ui.pushButtonCancel, "exit", tooltip="cancel and exit")

    self.ui.groupBoxControls.hide()
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()

    # first get ontology
    self.ontology_name = getOntologyName(task=icon_f, left_icon=None)

    # check for infrastructure
    checkAndFixResources(self.ontology_name, stage="ontology_stage_2")

    # attach ontology
    self.ontology_container = OntologyContainer(self.ontology_name)
    self.location = DIRECTORIES["latex_doc_location"] % self.ontology_name

    self.reduced_network_node_list = self.ontology_container.list_reduced_network_node_objects
    self.reduced_arc_list = self.ontology_container.list_reduced_network_arc_objects

    # instantiate entity behaviours
    networks = self.ontology_container.list_inter_branches
    entities_list = self.reduced_network_node_list
    self.entity_behaviours = EntityBehaviour(networks, entities_list)
    # self.entity_behaviour_graphs = EntityBehaviourGraphs(networks, entities_list)

    # get existing data
    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    loaded_entity_behaviours = getData(f)
    if loaded_entity_behaviours:
      for entity_str_ID in loaded_entity_behaviours:  # careful there may not be all entities at least during
        # developments
        if not (loaded_entity_behaviours[entity_str_ID] == None):
          self.entity_behaviours[entity_str_ID] = loaded_entity_behaviours[entity_str_ID]

    # interface components
    self.layout_InterNetworks = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsInterNetworks.setLayout(self.layout_InterNetworks)

    self.layout_Entities = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsEntities.setLayout(self.layout_Entities)

    self.layout_Variants = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsVariants.setLayout(self.layout_Variants)

    self.layout_Left = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsLeft.setLayout(self.layout_Left)

    self.layout_Right = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsRight.setLayout(self.layout_Right)

    # initialisations
    # network selector
    self.radio_InterNetworks = Selector(self.radioReceiverInterNetworks,
                                        networks,
                                        self.layout_InterNetworks)

    # entity selector
    entity_set = set()
    for nw in networks:
      for entity in self.reduced_network_node_list[nw]:
        entity_set.add(entity)

    entity_list = sorted(entity_set)

    self.radio_Entities = Selector(self.radioReceiverEntities,
                                   entity_list,
                                   self.layout_Entities)
    self.radio_Entities.showList([])

    variant_set = set()
    for obje_str_ID in self.entity_behaviours:
      network, entity, variant = functionGetObjectsFromObjectStringID(obje_str_ID)
      variant_set.add(variant)
    variant_list = sorted(variant_set)

    self.radio_Variants = Selector(self.radioReceiverVariants, variant_list, self.layout_Variants)
    self.radio_Variants.showList([])

    equations_label_list, self.equation_index = self.__makeEquationAndIndexLists()
    self.radio_Left = Selector(self.radioReceiverLeftEquations, equations_label_list, self.layout_Left)
    self.radio_Left.showList([])
    self.radio_Right = Selector(self.radioReceiverRightEquations, equations_label_list, self.layout_Right)
    self.radio_Right.showList([])

    self.selected_InterNetwork_ID = None
    self.selected_Entity_ID = None
    self.selected_variant_ID = None
    self.selected_variant_str_ID = "base"
    self.radio_index = None
    self.selected_base_variable = None
    self.blocked = []
    self.blocked_radio_ID = []
    # self.current_left_index = None
    # self.current_right_index = None
    self.left_show_list = self.radio_Left.show_list
    self.right_show_list = self.radio_Right.show_list

    # controls
    self.actions = ["duplicates", "new_variant", "edit_variant", "instantiate_variant"]

    # prepare lists
    self.current_base_var_ID = None

    # start process

    self.status_report = self.statusBar().showMessage
    self.status_report("getting started")
    self.entity_layout_clean = True
    self.variant_layout_clean = True
    self.equation_left_clean = True
    self.equation_right_clean = True

  def radioReceiverInterNetworks(self, text, ID):
    print("debugging -- receiver InterNetworks", text, ID)
    self.selected_InterNetwork_ID = ID
    nw_label_current = self.radio_InterNetworks.label_indices[ID]

    current_entities = self.reduced_network_node_list[nw_label_current]
    show_list = []
    for i in current_entities:
      show_list.append(self.radio_Entities.label_indices_inverse[i])
    self.radio_Entities.showList(show_list)

    #
    # updating interface
    self.radio_Variants.reset()
    self.radio_Left.reset()
    self.radio_Right.reset()
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()

  def radioReceiverEntities(self, text, ID):
    # print("debugging -- receiver Entities", text, ID)

    self.selected_Entity_ID = ID

    nw_str_ID = self.radio_InterNetworks.getStrID(self.selected_InterNetwork_ID)
    entity_label_ID = self.radio_Entities.getStrID(self.selected_Entity_ID)
    base_variant_str_ID = functionMakeObjectStringID(nw_str_ID, entity_label_ID, "base")

    if not self.entity_behaviours[base_variant_str_ID]:
      self.__makeBase()

    else:
      variant_IDs, variant_list = self.__makeVariantList()
      self.radio_Variants.showList(variant_IDs)

      #
      # updating interface
      self.radio_Left.reset()
      self.radio_Right.reset()
      self.ui.pushButtonLeft.hide()
      self.ui.pushButtonRight.hide()

    # print("debugging -- end of receiver Entities")

  def radioReceiverVariants(self, text, ID):
    print("debugging -- ReceiverVariants")
    self.ui.groupBoxControls.show()
    self.selected_variant_ID = ID

    self.status_report("editing entity-behaviour for entity  > %s <  variant  > %s < "
                       % (self.selected_Entity_ID, self.selected_variant_ID))
    pass

  def radioReceiverLeftEquations(self, text, eq_radio_ID):

    if self.state == "make_base":
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_index[eq_radio_ID]
      self.current_base_var_ID = var_ID
      if pixel_or_text == "pixelled":
        self.__makeEquationPixelButton(equation_label, self.ui.pushButtonLeft, "click to accept")
      elif pixel_or_text == "text":
        self.__makeEquationTextButton(equation_label, self.ui.pushButtonLeft, "click to accept")
      self.current_base_var_ID = var_ID

    elif self.state == "duplicates":
      print("debugging -- duplicates to be processed")
      self.__makeEquationTextButton("accept", self.ui.pushButtonLeft, "click to accept")
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_index[eq_radio_ID]
      self.blocked.append(eq_ID)
      self.blocked_radio_ID.append(eq_radio_ID)
      self.radio_Left.show_list.remove(eq_radio_ID)
      self.radio_Right.show_list.append(eq_radio_ID)
      self.radio_Left.showIt()
      entity_object_str = self.__makeEntityObjectStrID()
      nw, entity, variant = entity_object_str.split(".")
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity, var_ID)
      graph_file = var_equ_tree_graph.render()
      self.status_report("generated graph for %s " % (self.selected_Entity_ID))
      self.entity_behaviours.addVariant(nw, entity, variant, entity_assignments)

      self.radio_Left.showIt()
      self.radio_Right.showIt()

  def radioReceiverRightEquations(self, text, eq_radio_ID):

    if self.state == "make_base":
      return

    elif self.state == "duplicates":
      print("debugging -- duplicates to be processed")
      self.__makeEquationTextButton("accept", self.ui.pushButtonLeft, "click to accept")
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_index[eq_radio_ID]
      self.blocked.remove(eq_ID)
      self.blocked_radio_ID.remove(eq_radio_ID)
      self.radio_Left.show_list.append(eq_radio_ID)
      self.radio_Right.show_list.remove(eq_radio_ID)
      self.radio_Left.showIt()

      self.radio_Left.showIt()
      self.radio_Right.showIt()

  def on_pushButtonLeft_pressed(self):
    # print("debugging -- push left button state:",self.state)

    nw_str_ID = self.radio_InterNetworks.getStrID(self.selected_InterNetwork_ID)
    entity_label_ID = self.radio_Entities.getStrID(self.selected_Entity_ID)
    # nw, entity = entity_label_ID.split(ENTITY_OBJECT_SEPARATOR)
    entity_label_ID = self.radio_Entities.getStrID(self.selected_Entity_ID)

    if self.state == "make_base":
      variant = "base"
      var_ID = self.current_base_var_ID
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity_label_ID, var_ID)
      self.status_report("generated graph for %s" % (entity_label_ID))
      self.entity_behaviours.addVariant(nw_str_ID, entity_label_ID, variant, entity_assignments)

      graph_file = var_equ_tree_graph.render()
      # self.entity_behaviour_graphs.addVariant(nw, entity, variant, var_equ_tree_graph)
      self.selected_variant_str_ID = variant
      self.ui.pushButtonLeft.hide()

      variant_IDs, variant_list = self.__makeVariantList()
      self.radio_Variants.showList(variant_IDs)
      self.radio_Left.showList([])

    elif self.state == "duplicates":  # accepting
      print("debugging -- accepting duplicate reduced entity object")
      var_ID = self.selected_base_variable
      entity_object_str = self.__makeEntityObjectStrID()
      nw, entity, variant = entity_object_str.split(".")
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity, var_ID)
      graph_file = var_equ_tree_graph.render()
      self.status_report("generated graph for %s " % (self.selected_Entity_ID))
      self.entity_behaviours.addVariant(nw, entity, variant, entity_assignments)

      self.radio_Left.reset()
      self.radio_Right.reset()
      self.radio_Variants.reset()

  # push buttons
  def on_pushButtonRight_pressed(self):
    # print("debugging -- push right button")
    pass

  def on_pushButtonSave_pressed(self):
    # print("debugging -- save file")
    # self.ontology_container.writeVariables()

    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    putData(self.entity_behaviours, f)

  def on_pushButtonInformation_pressed(self):
    print("todo: not yet implemented")

  def on_radioButtonDuplicates_pressed(self):
    print("debugging -- duplicates")
    self.state = "duplicates"
    entity_object_str = self.__makeEntityObjectStrID()

    self.selected_base_variable = self.entity_behaviours[entity_object_str]["root_variable"]  # var_ID : int

    radio_show_list = self.__makeLeftSelector()
    self.radio_Left.showList(radio_show_list)

  def on_radioButtonNewVariant_pressed(self):
    variant_IDs, limiting_list = self.__makeVariantList()

    self.dialoge = UI_String("Provide a new variant name", placeholdertext="variant", limiting_list=limiting_list)
    self.dialoge.exec_()
    print("debugging -- new variant")

  def on_radioButtonEditVariant_pressed(self):
    print("debugging -- edit variant")

  def on_radioButtonInstantiateVariant_pressed(self):
    print("debugging -- instantiate variant")

  # =============================

  def analyseBiPartiteGraph(self, object, var_ID):
    obj = object.replace("|", "_")
    blocked = self.blocked
    var_equ_tree_graph, assignments = AnalyseBiPartiteGraph(var_ID,
                                                            self.ontology_container,
                                                            self.ontology_name,
                                                            blocked,
                                                            obj)
    return var_equ_tree_graph, assignments

  def __makeEntityObjectStrID(self):
    nw_str_ID = self.radio_InterNetworks.label_indices[self.selected_InterNetwork_ID]
    entity_label_ID = self.radio_Entities.label_indices[self.selected_Entity_ID]
    variant = self.radio_Variants.label_indices[self.selected_variant_ID]
    entity_object_str = functionMakeObjectStringID(nw_str_ID, entity_label_ID, variant)
    return entity_object_str

  def __makeLeftSelector(self):
    show = self.__makeShows()
    radio_show_list = []
    print("debugging -- halting point")
    for i in self.equation_index:
      eq_ID, var_ID, var_type, nw_eq, equation_labe = self.equation_index[i]
      if eq_ID in show:
        radio_show_list.append(i)

    return radio_show_list

  def __makeRightSelector(self):
    show = self.blocked
    equation_list, index = self.__makeRadioSelectorLists(show)
    self.radio_Right.makeSelector(pixel_or_text, equation_list, self.layout_Right)
    self.equation_right_clean = False
    self.current_right_index = index

  # def __makeAfterChangedBlockedList(self):
  #
  #   entity_object_str = self.__makeEntityObjectStrID()
  #   nw, entity, variant = entity_object_str.split(".")
  #   self.selected_base_variable = self.entity_behaviours[entity_object_str]["root_variable"]  # var_ID : int
  #
  #
  #   var_ID = self.entity_behaviours[entity_object_str]["root_variable"]  # self.current_base_var_ID
  #   var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity, var_ID)
  #   graph_file = var_equ_tree_graph.render()
  #   self.status_report("generated graph for %s " % (self.selected_Entity_ID))
  #   self.entity_behaviours.addVariant(nw, entity, variant, entity_assignments)
  #   # self.entity_behaviour_graphs.addVariant(nw, entity, variant, var_equ_tree_graph)

  def __makeShows(self):
    nw = self.selected_InterNetwork_ID
    entity = self.selected_Entity_ID
    variant = self.selected_variant_ID
    entity_object_str = self.__makeEntityObjectStrID()

    nodes = self.entity_behaviours[entity_object_str]["nodes"]
    show = []
    # select duplicates:
    for node in nodes:
      label, str_ID = nodes[node].split("_")
      ID = int(str_ID)
      if label == "variable":
        equation_IDs = sorted(self.ontology_container.variables[ID]["equations"])
        if len(equation_IDs) > 1:
          # print("debugging -- found variable %s"%equation_IDs)
          show.extend(equation_IDs)
    for eq_ID in self.blocked:
      if eq_ID in show:
        show.remove(eq_ID)
    return show

  def __makeEquationTextButton(self, text, button, tooltip):
    button.setText(text)
    button.setToolTip(tooltip)
    button.show()

  def __makeEquationPixelButton(self, equation_label, button, tooltip):
    button.setText("")
    icon, label, size = equation_label
    button.setIcon(icon)
    button.setIconSize(size)
    button.setToolTip(tooltip)
    button.show()
    return

  def __clearEntityInfrastructure(self):
    if not self.entity_layout_clean:
      clearLayout(self.layout_Entities)
    self.selected_Entity_ID = None
    self.__clearVariantInfrastructure()
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()
    # print("debugging -- clearing entity infrastructure")
    self.entity_layout_clean = True

  def __clearVariantInfrastructure(self):
    if not self.variant_layout_clean:
      clearLayout(self.layout_Variants)
    self.selected_variant_ID = None
    self.__clearEquationInfrastructure()
    # print("debugging -- clearing variant infrastructure")
    self.variant_layout_clean = True

  def __clearEquationInfrastructure(self):
    if not self.equation_left_clean:
      clearLayout(self.layout_Left)
      self.equation_left_clean = True
      # print("debugging -- clearing left ")
    if not self.equation_right_clean:
      clearLayout(self.layout_Right)
      self.equation_left_clean = True
      # print("debugging -- clearing right ")
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()
    # print("debugging -- clearing equation infrastructure")

  def __makeBase(self):
    self.ui.groupBoxControls.hide()
    # print("debugging -- define base")
    self.state = "make_base"
    selected_state_equation_list, selected_state_radio_entries = self.__makeStateEquationSelector()

    self.radio_Left.showList(selected_state_radio_entries)
    self.status_report("making base for %s" % self.selected_Entity_ID)

  def __makeStateEquationSelector(self):

    nw = self.selected_InterNetwork_ID
    nw_str_ID = self.radio_InterNetworks.getStrID(nw)

    selected_state_equation_list = []
    selected_state_radio_entries = []
    selected_var_type = None

    label_index = self.radio_Left.label_indices

    for eq_radio_ID in label_index:

      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_index[eq_radio_ID]

      # (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation) = self.equations[eq_ID]

      if nw_str_ID in self.ontology_container.networks:
        nws = list(self.ontology_container.ontology_tree[nw_str_ID]["parents"])
        nws.append(nw_str_ID)
        for p_nw in nws:
          if p_nw in rules["nodes"]:
            selected_var_type = rules["nodes"][p_nw]
        for p_nw in nws:
          if p_nw == nw_eq:  # in self.rendered_equation_dictionary:
            if var_type == selected_var_type:
              selected_state_equation_list.append(eq_ID)
              selected_state_radio_entries.append(eq_radio_ID)

    return selected_state_equation_list, selected_state_radio_entries

  def __makeVariantList(self):

    nw_str_ID = self.radio_InterNetworks.getStrID(self.selected_InterNetwork_ID)

    entity_str_IDs = sorted(self.entity_behaviours)
    variants_IDs = set()
    variants = set()
    for o in entity_str_IDs:
      network, entity, variant = functionGetObjectsFromObjectStringID(o)
      if network == nw_str_ID:
        variant_ID = self.radio_Variants.label_indices_inverse[variant]
        variants_IDs.add(variant_ID)
        variants.add(variant)

    return list(variants_IDs), list(variants)

  def __makeRadioSelectorLists(self, selector_list):

    radio_selectors = {
            "rendered": [],
            "pixelled": []
            }

    index = {"variable": [], "equation": []}
    indices = []

    for equ_ID in selector_list:
      var_ID, var_type, nw_eq, rendered_equation, pixelled_equation = self.equations[equ_ID]
      radio_selectors["rendered"].append(rendered_equation)
      radio_selectors["pixelled"].append(pixelled_equation)
      indices.append(equ_ID)

    return radio_selectors, indices

  def __makeEquationAndIndexLists(self):

    equations = []
    equation_index = {}
    equation_variable_dictionary = self.ontology_container.equation_variable_dictionary
    count = -1
    for eq_ID in equation_variable_dictionary:
      count += 1
      var_ID, equation = equation_variable_dictionary[eq_ID]
      var_type = self.ontology_container.variables[var_ID]["type"]
      nw_eq = self.ontology_container.variables[var_ID]["network"]

      if pixel_or_text == "text":

        rendered_expressions = renderExpressionFromGlobalIDToInternal(
                equation["rhs"],
                self.ontology_container.variables,
                self.ontology_container.indices)

        rendered_variable = self.ontology_container.variables[var_ID]["aliases"]["internal_code"]
        equation_label = "%s := %s" % (rendered_variable, rendered_expressions)
      elif pixel_or_text == "pixelled":
        equation_label = self.__make_icon(eq_ID)

      # equations[eq_ID] = (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation)
      equations.append(equation_label)
      equation_index[count] = (eq_ID, var_ID, var_type, nw_eq, equation_label)
    return equations, equation_index

  def __makeEquationList_keep_not_used(self):

    equations = {}  # tuple
    equation_variable_dictionary = self.ontology_container.equation_variable_dictionary
    for eq_ID in equation_variable_dictionary:
      var_ID, equation = equation_variable_dictionary[eq_ID]
      var_type = self.ontology_container.variables[var_ID]["type"]
      nw_eq = self.ontology_container.variables[var_ID]["network"]

      rendered_expressions = renderExpressionFromGlobalIDToInternal(
              equation["rhs"],
              self.ontology_container.variables,
              self.ontology_container.indices)

      rendered_variable = self.ontology_container.variables[var_ID]["aliases"]["internal_code"]
      rendered_equation = "%s := %s" % (rendered_variable, rendered_expressions)
      pixelled_equation = self.__make_icon(eq_ID)

      equations[eq_ID] = (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation)

    return equations

  def __make_icon(self, eq_ID):

    template = join(self.location, "equation_%s.png")
    f = template % eq_ID
    label = QtWidgets.QLabel()
    pix = QtGui.QPixmap(f)
    icon = QtGui.QIcon(pix)
    size = pix.size()
    return icon, label, size
