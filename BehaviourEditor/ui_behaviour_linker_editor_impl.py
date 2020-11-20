from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from copy import deepcopy

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.common_resources import indexList
from Common.common_resources import invertDict
from Common.common_resources import putData, TEMPLATE_ENTITY_OBJECT_REMOVED_DUPLICATES
from Common.ontology_container import OntologyContainer
from Common.qt_resources import clearLayout
from Common.record_definitions_equation_linking import EntityBehaviour, VariantRecord
from Common.record_definitions_equation_linking import functionGetObjectsFromObjectStringID
from Common.record_definitions_equation_linking import functionMakeObjectStringID
from Common.resource_initialisation import checkAndFixResources
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.resources_icons import roundButton
from Common.ui_string_dialog_impl import UI_String
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
MAX_NUMBER_OF_VARIANTS = 30  # RULE: there is a maximum total number of variants for all entities

# TODO: could be included into the interface as a choice

pixel_or_text = "text"  # NOTE: variable to set the mode


class Selector(QtCore.QObject):
  """
  Generates a selector for a set of radio buttons.
  The radio buttons are added to a given layout.
  Layouts are handling the buttons in autoexclusive mode.
  The current version is exclusively operating in autoexclusive mode even though there is a variable
    indicating to opposite. It does not work if not every button is set to autoexclusive explicitly. In that case
    the exclusive mode must be handled manually.
    TODO: implement manual handling -- tip: define new button adding group-internal communication
  """
  radio_signal = QtCore.pyqtSignal(str, int)

  def __init__(self, radio_class, receiver, label_list, layout, mode="text", autoexclusive=False):
    super().__init__()
    self.radio_class = radio_class
    self.labels = label_list
    self.layout = layout
    self.mode = mode
    self.autoexclusive = autoexclusive
    self.selected_ID = None
    self.show_list = []

    self.radios = {}
    self.label_indices, \
    self.label_indices_inverse = indexList(self.labels)

    self.makeSelector()
    self.radio_signal.connect(receiver)

  def getStrID(self):
    ID = self.selected_ID
    if ID == None:
      return None
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
    for ID in self.label_indices:
      label = self.labels[ID]
      self.radios[ID] = QtWidgets.QRadioButton(label)
      if self.autoexclusive:
        self.radios[ID].setAutoExclusive(True)
      self.layout.addWidget(self.radios[ID])
      self.radios[ID].toggled.connect(self.selector_toggled)

  def makePixelSelector(self):

    for ID in self.label_indices:
      icon, label, size = self.labels[ID]
      label = QtWidgets.QLabel()
      self.radios[ID] = QtWidgets.QRadioButton(label)
      self.radios[ID].setIcon(icon)
      self.radios[ID].setIconSize(size)
      self.radios[ID].resize(0, 0)  # Note: not sure what I am doing here -- reduces gaps between

      if self.autoexclusive:
        self.radios[ID].setAutoExclusive(False)
      self.layout.addWidget(self.radios[ID])

      self.radios[ID].toggled.connect(self.selector_toggled)

  def showList(self, show):
    self.show_list = show
    self.showIt()
    # self.resetChecked()

  def showIt(self):
    for ID in self.radios:
      # self.radios[ID].setChecked(False)
      if ID not in self.show_list:
        self.radios[ID].hide()
      else:
        self.radios[ID].show()

  def reset(self):
    self.showList([])

  def selector_pressed(self):
    print("debugging -- pressed")

  def selector_toggled(self, toggled):
    # print("debugging -- toggled", toggled)

    if toggled:
      ID = self.getToggled()

      if ID >= 0:
        self.radio_signal.emit(self.radio_class, ID)

  def getToggled(self):

    count = -1
    ID = -1
    for ID_ in self.radios:
      count += 1
      if self.radios[ID_].isChecked():
        # print("goit it :", label)
        ID = count

    self.selected_ID = ID

    return ID

  def resetChecked(self):
    for ID in self.radios:
      self.radios[ID].setDown(False)

  # def selector_released(self):
  #   print("debugging -- released radio button")

class VariantSelector(Selector):
  def __init__(self, radio_class, receiver, label_list_initial, layout, mode="text", autoexclusive=False):
    label_list, self.variant_map, self.variant_indices_map = self.variantMapping(label_list_initial)

    super().__init__(radio_class, receiver, label_list, layout, mode=mode, autoexclusive=autoexclusive)


  def updateVariants(self, label_list_initial):
    self.labels, self.variant_map, self.variant_indices_map = self.variantMapping(label_list_initial)
    self.label_indices, \
    self.label_indices_inverse = indexList(self.labels)

  def variantMapping(self, variant_list):
    """
    maps the variants to the fixed IDs defined for the selector
    """

    variant_map = {}
    extended_variant_list = []
    self.show_list = []

    variant_indices = ["variant_%s" % i for i in range(0, MAX_NUMBER_OF_VARIANTS)]


    for i in range(len(variant_indices)):
      variant_map[i] = variant_indices[i]
      extended_variant_list.append(variant_indices[i])

    for i in range(len(variant_list)):
      variant_map[i] = variant_list[i]
      extended_variant_list[i] = variant_list[i]
      try:
        self.radios[i].setText(variant_list[i])
      except:
        pass
      self.show_list.append(i)

    variant_inverse_map = invertDict(variant_map)

    return extended_variant_list, variant_map, variant_inverse_map


class MainWindowImpl(QtWidgets.QMainWindow):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

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
          data = loaded_entity_behaviours[entity_str_ID]
          self.entity_behaviours[entity_str_ID] = VariantRecord(tree=data["tree"],
                                                                nodes=data["nodes"],
                                                                IDs=data["IDs"],
                                                                root_variable=data["root_variable"],
                                                                blocked_list= data["blocked"],
                                                                buddies_list=data["buddies"])

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
    self.radio_InterNetworks = Selector("InterNetworks",
                                        self.radioReceiverState,
                                        networks,
                                        self.layout_InterNetworks)

    # entity selector
    entity_set = set()
    for nw in networks:
      for entity in self.reduced_network_node_list[nw]:
        entity_set.add(entity)
    entity_list = sorted(entity_set)

    self.radio_Entities = Selector("Entities",
                                   self.radioReceiverState,
                                   entity_list,
                                   self.layout_Entities)
    self.radio_Entities.showList([])

    variant_list = self.entity_behaviours.getVariantList()
    self.radio_Variants = VariantSelector("Variants",
                                   self.radioReceiverState,
                                   variant_list,
                                   self.layout_Variants)
    self.radio_Variants.showIt()

    equations_label_list, \
    self.equation_information, \
    self.equation_inverse_index = self.__makeEquationAndIndexLists()

    self.radio_Left = Selector("Left",
                               self.radioReceiverLeftEquations,
                               equations_label_list,
                               self.layout_Left)
    self.radio_Left.showList([])

    self.radio_Right = Selector("Right",
                                self.radioReceiverRightEquations,
                                equations_label_list,
                                self.layout_Right)
    self.radio_Right.showList([])

    self.selected_InterNetwork_ID = None
    self.selected_Entity_ID = None
    self.selected_variant_ID = None
    self.selected_variant_str_ID = "base"
    self.radio_index = None
    self.selected_base_variable = None
    self.blocked = []
    self.blocked_radio_ID = []
    self.left_show_list = self.radio_Left.show_list
    self.right_show_list = self.radio_Right.show_list

    # controls
    self.actions = ["show", "duplicates", "new_variant", "edit_variant", "instantiate_variant"]

    # prepare lists
    self.current_base_var_ID = None

    # start process

    self.status_report = self.statusBar().showMessage
    self.status_report("getting started")
    self.entity_layout_clean = True
    self.variant_layout_clean = True
    self.equation_left_clean = True
    self.equation_right_clean = True
    self.state = "start"

  def isCompleteState(self):
    state = -1
    if self.radio_InterNetworks.selected_ID != None:
      state += 1
      if self.radio_Entities.selected_ID != None:
        state += 1
        if self.radio_Variants.selected_ID != None:
          state += 1
    return state

  def radioReceiverState(self, radio_class, ID):
    print("debugging -- receiver state %s" % radio_class, ID)
    if radio_class == "InterNetworks":
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

    elif radio_class == "Entities":
      # print("debugging -- receiver Entities", radio_class, ID)
      # print("debugging -- state %s"%self.state)
      # print("debugging -- is state %s"%self.isCompleteState())

      self.selected_Entity_ID = ID

      nw_str_ID = self.radio_InterNetworks.getStrID()
      entity_label_ID = self.radio_Entities.getStrID()
      base_variant_str_ID = functionMakeObjectStringID(nw_str_ID, entity_label_ID, "base")

      if not self.entity_behaviours[base_variant_str_ID]:
        self.radio_Variants.showList([])
        self.__makeBase()

      else:
        # print("debugging -- getting variant ")
        if self.radio_Variants.getStrID() != None:  # handle first pass
          self.__makeAndDisplayEquationListLeftAndRight()
          self.ui.groupBoxControls.show()
        else:
          self.radio_Variants.reset()
          self.radio_Left.reset()
          self.radio_Right.reset()
          self.ui.pushButtonLeft.hide()
          self.ui.pushButtonRight.hide()
        variant_IDs = self.__makeVariantRadioIDList()
        self.radio_Variants.showList(variant_IDs)


    elif radio_class == "Variants":
      print("debugging -- ReceiverVariants")
      self.ui.radioButtonShowVariant.setChecked(True)
      self.ui.groupBoxControls.show()
      variant = self.radio_Variants.getStrID()
      self.__makeAndDisplayEquationListLeftAndRight()

    else:
      print("error in state %s does not fit any case" % radio_class)

  def radioReceiverLeftEquations(self, text, eq_radio_ID):

    if self.state == "make_base":
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[eq_radio_ID]
      self.current_base_var_ID = var_ID
      if pixel_or_text == "pixelled":
        self.__makeEquationPixelButton(equation_label, self.ui.pushButtonLeft, "click to accept")
      elif pixel_or_text == "text":
        self.__makeEquationTextButton(equation_label, self.ui.pushButtonLeft, "click to accept")
      self.current_base_var_ID = var_ID

    elif self.state in ["duplicates", "new_variant"]:
      print("debugging -- duplicates to be processed")
      self.__makeEquationTextButton("accept", self.ui.pushButtonLeft, "click to accept")
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[eq_radio_ID]
      self.blocked.append(eq_ID)
      self.blocked_radio_ID.append(eq_radio_ID)
      self.radio_Left.show_list.remove(eq_radio_ID)
      self.radio_Right.show_list.append(eq_radio_ID)
      self.radio_Left.showIt()
      entity_object_str = self.__makeEntityObjectStrID()
      nw, entity, variant = entity_object_str.split(".")
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity, var_ID, self.blocked)
      graph_file = var_equ_tree_graph.render()
      self.status_report("generated graph for %s " % (self.selected_Entity_ID))
      #
      if self.state == "duplicates":
        duplicate_variant = TEMPLATE_ENTITY_OBJECT_REMOVED_DUPLICATES%variant
        self.entity_behaviours.addVariant(nw, entity, duplicate_variant, entity_assignments)

      self.radio_Left.showIt()
      self.radio_Right.showIt()


  def radioReceiverRightEquations(self, text, eq_radio_ID):

    if self.state == "make_base":
      return

    elif self.state in ["duplicates", "new_variant"]:
      print("debugging -- duplicates to be processed")
      self.__makeEquationTextButton("accept", self.ui.pushButtonLeft, "click to accept")
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[eq_radio_ID]
      self.blocked.remove(eq_ID)
      self.blocked_radio_ID.remove(eq_radio_ID)
      self.radio_Left.show_list.append(eq_radio_ID)
      self.radio_Right.show_list.remove(eq_radio_ID)
      self.radio_Left.showIt()

      self.radio_Left.showIt()
      self.radio_Right.showIt()

  def on_pushButtonLeft_pressed(self):
    print("debugging -- push left button state:",self.state)

    nw_str_ID = self.radio_InterNetworks.getStrID()
    entity_label_ID = self.radio_Entities.getStrID()
    entity_label_ID = self.radio_Entities.getStrID()

    if self.state == "make_base":
      variant = "base"
      var_ID = self.current_base_var_ID
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(entity_label_ID, var_ID, [])
      self.status_report("generated graph for %s" % (entity_label_ID))
      self.entity_behaviours.addVariant(nw_str_ID, entity_label_ID, variant, entity_assignments)

      graph_file = var_equ_tree_graph.render()
      # self.entity_behaviour_graphs.addVariant(nw, entity, variant, var_equ_tree_graph)
      self.selected_variant_str_ID = variant
      self.ui.pushButtonLeft.hide()

      variant_IDs = self.__makeVariantRadioIDList()
      self.radio_Variants.showList(variant_IDs)
      self.radio_Left.showList([])

    elif self.state in ["duplicates", "new_variant"]:  # accepting
      print("debugging -- accepting >>> %s <<< reduced entity object"%self.state)
      var_ID = self.selected_base_variable
      entity_object_str = self.__makeEntityObjectStrID()
      nw, entity, variant = entity_object_str.split(".")
      var_equ_tree_graph, _entity_assignments = self.analyseBiPartiteGraph(entity, var_ID, self.blocked)
      graph_file = var_equ_tree_graph.render()

      if self.state in ["duplicates"]:
        duplicate_variant = TEMPLATE_ENTITY_OBJECT_REMOVED_DUPLICATES%variant
        entity_assignments = _entity_assignments
      else:
        limiting_list = self.__makeVariantStringList()
        duplicate_variant = self.__askForNewVariantName(limiting_list)
        print("debugging -- new variant", duplicate_variant)
        entity_assignments = deepcopy(_entity_assignments)
      self.entity_behaviours.addVariant(nw, entity, duplicate_variant, entity_assignments)
      variants = self.entity_behaviours.getVariantList()
      self.radio_Variants.updateVariants(variants)

      self.status_report("generated graph for %s " % (duplicate_variant))

      self.radio_Left.reset()
      self.radio_Right.reset()
      self.radio_Variants.showIt()


    elif self.state == "show":
      print("debugging -- show don't do anything")

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

  def on_radioButtonShowVariant_pressed(self):
    # print("debugging -- show variant")
    self.state = "show"
    self.__makeAndDisplayEquationListLeftAndRight()



  def on_radioButtonDuplicates_pressed(self):
    print("debugging -- duplicates")
    self.state = "duplicates"
    self.blocked = []

    entity_object_str = self.__makeEntityObjectStrID()
    self.selected_base_variable = self.entity_behaviours[entity_object_str]["root_variable"]  # var_ID : int
    show = self.__makeDuplicateShows()
    radio_show_list = self.__makeRadioShowList(show)
    self.radio_Left.showList(radio_show_list)

  def on_radioButtonNewVariant_pressed(self):
    self.state = "new_variant"
    self.__makeAndDisplayEquationListLeftAndRight() #self.selected_variant_str_ID)

  def __askForNewVariantName(self, limiting_list):
    dialoge = UI_String("Provide a new variant name", placeholdertext="variant", limiting_list=limiting_list)
    dialoge.exec_()
    variant = dialoge.getText()
    del dialoge
    return variant

  def on_radioButtonEditVariant_pressed(self):
    print("debugging -- edit variant")
    self.state= "edit_variant"
    self.__makeAndDisplayEquationListLeftAndRight()

  def on_radioButtonInstantiateVariant_pressed(self):
    print("debugging -- instantiate variant")

  # =============================

  def analyseBiPartiteGraph(self, entity, var_ID, blocked):
    obj = entity.replace("|", "_")
    var_equ_tree_graph, assignments = AnalyseBiPartiteGraph(var_ID,
                                                            self.ontology_container,
                                                            self.ontology_name,
                                                            blocked,
                                                            obj)
    return var_equ_tree_graph, assignments

  def __makeAndDisplayEquationListLeftAndRight(self):
    # print("debugging -- making and displaying left list")
    network = self.radio_InterNetworks.getStrID()
    entity = self.radio_Entities.getStrID()
    variant = self.radio_Variants.getStrID()
    entity_str_ID = functionMakeObjectStringID(network, entity, variant)

    if self.state == "new_variant":
      print("debugging -- new variant, entity string", entity_str_ID)
      if "base" in entity_str_ID:
        print("debugging -- found D-D", entity_str_ID)

    self.selected_base_variable = self.entity_behaviours.getRootVariableID(entity_str_ID)
    equation_ID_list = self.entity_behaviours.getEquationIDList(entity_str_ID)
    blocked_ = self.entity_behaviours.getBlocked(entity_str_ID)  # ok that is a copy
    blocked= deepcopy(blocked_)
    root_equation = equation_ID_list.pop(0)

    eq_radio_ID = self.equation_inverse_index[root_equation]
    eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[eq_radio_ID]

    self.__makeEquationTextButton(equation_label, self.ui.pushButtonLeft, "click to accept")

    # print("debugging -- left list showing ", equation_ID_list[0:5])
    show_left = self.__makeRadioShowList(equation_ID_list)
    show_right = self.__makeRadioShowList((blocked))
    self.blocked = deepcopy(blocked)

    # print("debugging -- left list showing ", show_left[0:5])
    self.radio_Left.showList(show_left)
    self.radio_Right.showList(show_right)


  def __makeEntityObjectStrID(self):
    nw_str_ID = self.radio_InterNetworks.label_indices[self.selected_InterNetwork_ID]
    entity_label_ID = self.radio_Entities.label_indices[self.selected_Entity_ID]
    variant = self.radio_Variants.getStrID() #label_indices[self.radio_Variants.getStrID()] #selected_variant_ID]
    entity_object_str = functionMakeObjectStringID(nw_str_ID, entity_label_ID, variant)
    return entity_object_str

  def __makeRadioShowList(self, show):
    radio_show_list = []
    # print("debugging -- halting point")
    for i in self.equation_information:
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[i]
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

  def __makeDuplicateShows(self):
    # nw = self.selected_InterNetwork_ID
    # entity = self.selected_Entity_ID
    # variant = self.selected_variant_ID
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

  # def __clearEntityInfrastructure(self):
  #   if not self.entity_layout_clean:
  #     clearLayout(self.layout_Entities)
  #   self.selected_Entity_ID = None
  #   self.__clearVariantInfrastructure()
  #   self.ui.pushButtonLeft.hide()
  #   self.ui.pushButtonRight.hide()
  #   # print("debugging -- clearing entity infrastructure")
  #   self.entity_layout_clean = True
  #
  # def __clearVariantInfrastructure(self):
  #   if not self.variant_layout_clean:
  #     clearLayout(self.layout_Variants)
  #   self.selected_variant_ID = None
  #   self.__clearEquationInfrastructure()
  #   # print("debugging -- clearing variant infrastructure")
  #   self.variant_layout_clean = True
  #
  # def __clearEquationInfrastructure(self):
  #   if not self.equation_left_clean:
  #     clearLayout(self.layout_Left)
  #     self.equation_left_clean = True
  #     # print("debugging -- clearing left ")
  #   if not self.equation_right_clean:
  #     clearLayout(self.layout_Right)
  #     self.equation_left_clean = True
  #     # print("debugging -- clearing right ")
  #   self.ui.pushButtonLeft.hide()
  #   self.ui.pushButtonRight.hide()
  #   # print("debugging -- clearing equation infrastructure")

  def __makeBase(self):
    self.ui.groupBoxControls.hide()
    # print("debugging -- define base")
    self.state = "make_base"
    selected_state_equation_list, selected_state_radio_entries = self.__makeStateEquationSelector()

    self.radio_Left.showList(selected_state_radio_entries)
    self.status_report("making base for %s" % self.selected_Entity_ID)

  def __makeStateEquationSelector(self):

    nw = self.selected_InterNetwork_ID
    nw_str_ID = self.radio_InterNetworks.getStrID()

    selected_state_equation_list = []
    selected_state_radio_entries = []
    selected_var_type = None

    label_index = self.radio_Left.label_indices

    for eq_radio_ID in label_index:

      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[eq_radio_ID]

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

  def __makeVariantStringList(self):

    nw_str_ID = self.radio_InterNetworks.getStrID()

    entity_str_IDs = sorted(self.entity_behaviours)
    variants_radio_IDs = set()
    variants = set()
    for o in entity_str_IDs:
      network, entity, variant = functionGetObjectsFromObjectStringID(o)
      if network == nw_str_ID:
        variant_radio_ID = self.radio_Variants.label_indices_inverse[variant]
        variants_radio_IDs.add(variant_radio_ID)
        variants.add(variant)

    return list(variants_radio_IDs), list(variants)


  def __makeVariantRadioIDList(self):

    nw_str_ID = self.radio_InterNetworks.getStrID()

    entity_str_IDs = sorted(self.entity_behaviours)
    variants_radio_IDs = set()
    for o in entity_str_IDs:
      network, entity, variant = functionGetObjectsFromObjectStringID(o)
      if network == nw_str_ID:
        variant_radio_ID = self.radio_Variants.label_indices_inverse[variant]
        variants_radio_IDs.add(variant_radio_ID)

    return list(variants_radio_IDs)

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
    equation_information = {}
    equation_inverse_index = {}
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
      equation_inverse_index[eq_ID] = count
      equation_information[count] = (eq_ID, var_ID, var_type, nw_eq, equation_label)
    return equations, equation_information, equation_inverse_index

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
