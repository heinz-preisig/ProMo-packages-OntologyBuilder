from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.common_resources import putData
from Common.ontology_container import OntologyContainer
from Common.qt_resources import cleanLayout
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


class Selector(QtCore.QObject):
  radio_signal = QtCore.pyqtSignal(str, int)

  def __init__(self, receiver):
    super().__init__()
    self.radio_signal.connect(receiver)
    self.radios = {}

  def makeSelector(self, which_one, label_list, layout):
    if which_one == "text":
      self.makeTextSelector(label_list["rendered"], layout)
    elif which_one == "pixelled":
      self.makePixelSelector(label_list["pixelled"], layout)
    else:
      raise

  def makeTextSelector(self, label_list, layout):
    cleanLayout(layout)
    for label in label_list:
      self.radios[label] = QtWidgets.QRadioButton(label)
      layout.addWidget(self.radios[label])

      self.radios[label].toggled.connect(self.selector_toggled)

  def makePixelSelector(self, pixel_dictionary, layout):

    cleanLayout(layout)

    ID = 0
    for (icon, label, size) in pixel_dictionary:
      label = QtWidgets.QLabel()
      self.radios[ID] = QtWidgets.QRadioButton(label)
      self.radios[ID].setIcon(icon)
      self.radios[ID].setIconSize(size)
      self.radios[ID].resize(0, 0)  # Note: not sure what I am doing here -- reduces gaps between
      layout.addWidget(self.radios[ID])

      self.radios[ID].toggled.connect(self.selector_toggled)

      ID += 1
    return self.radios

  def selector_toggled(self, toggled):
    # print("debugging -- toggled", toggled)
    count = -1
    if toggled:
      for label in self.radios:
        count += 1
        if self.radios[label].isChecked():
          # print("goit it :", label)
          self.radio_signal.emit(str(label), count)


class EntityBehaviour(dict):
  def __init__(self, entity):
    self.addEntity(entity)

  def addEntity(self, entity):
    self[entity] = {"base": None}

  def addVariant(self, entity, variant, data):
    if entity not in self:
      self.addEntity(entity)
    self[entity][variant] = data

  def removeEntity(self, entity):
    del self[entity]

  def removeVariant(self, entity, variant):
    del self[entity][variant]


class EntityBehaviourGraphs(EntityBehaviour):

  def __init__(self, entity):
    super().__init__(entity)


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

    self.radio_InterNetworks = {}
    self.radio_Entities = {}
    self.radio_Variants = {}
    self.radio_Entities = {}
    self.radio_Left = {}
    self.radio_Right = {}

    self.selected_InterNetwork = None
    self.selected_Entity = None
    self.selected_variant = "base"
    self.radio_index = None
    self.text_or_pixel = "pixelled"

    # controls
    self.actions = ["duplicates", "new_variant", "edit_variant", "instantiate_variant"]

    # get existing data
    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    self.entity_behaviours = getData(f)
    if not self.entity_behaviours:
      # print("debugging -- no data")
      self.entity_behaviours = {}
    self.entity_behaviour_graphs = {}

    # prepare lists
    self.equations = self.__makeEquationList()
    self.current_base_var_ID = None

    # start process
    inter_networks = self.ontology_container.list_inter_branches
    self.radio_InterNetworks = Selector(self.radioReceiverInterNetworks)
    self.radio_InterNetworks.makeTextSelector(inter_networks, self.layout_InterNetworks)

    self.status = self.statusBar().showMessage
    self.status("getting started")
    self.entity_layout_clean = True
    self.variant_layout_clean = True
    self.equation_left_clean = True
    self.equation_right_clean = True

  def radioReceiverInterNetworks(self, text, ID):
    # print("debugging -- receiver InterNetworks", text, ID)
    self.selected_InterNetwork = text

    entities_list = self.reduced_network_node_list[self.selected_InterNetwork]

    self.__clearEntityInfrastructure()
    self.radio_Entities = Selector(self.radioReceiverEntities)
    self.radio_Entities.makeTextSelector(entities_list, self.layout_Entities)
    self.entity_layour_clean = False

  def radioReceiverEntities(self, text, ID):
    # print("debugging -- receiver Entities", text, ID)
    self.selected_Entity = text
    self.__clearVariantInfrastructure()


    if self.selected_InterNetwork not in self.entity_behaviours:  # for the very first time
      self.entity_behaviours[self.selected_InterNetwork] = {}
      self.entity_behaviours[self.selected_InterNetwork] = EntityBehaviour(self.selected_Entity)
      # print("debugging -- new base behaviour ")

      if self.selected_InterNetwork not in self.entity_behaviour_graphs:  # for the very first time
        self.entity_behaviour_graphs[self.selected_InterNetwork] = {}
        self.entity_behaviour_graphs[self.selected_InterNetwork] = EntityBehaviourGraphs(self.selected_Entity)

      self.equation_left_clean = False
      self.__makeBase()
      return

    # print("halting")
    if self.selected_InterNetwork not in self.entity_behaviour_graphs:  # for the very first time
      self.entity_behaviour_graphs[self.selected_InterNetwork] = {}
      self.entity_behaviour_graphs[self.selected_InterNetwork] = EntityBehaviourGraphs(self.selected_Entity)

    if self.selected_Entity not in self.entity_behaviours[self.selected_InterNetwork]:
      self.equation_left_clean = False
      self.__makeBase()

    elif not self.entity_behaviours[self.selected_InterNetwork][self.selected_Entity]["base"]:
      self.equation_left_clean = False
      self.__makeBase()

    else:
      variant_list = self.__makeVariantList()
      self.radio_Variants = Selector(self.radioReceiverVariants)
      self.radio_Variants.makeTextSelector(variant_list, self.layout_Variants)
      self.variant_layout_clean = False

    # print("debugging -- end of receiver Entities")

  def radioReceiverVariants(self):
    # print("debugging -- ReceiverVariants")
    self.ui.groupBoxControls.show()
    pass

  def radioReceiverEquations(self, text, ID):

    if self.state == "make_base":
      eq_ID = self.equation_selection[ID]
      (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation) = self.equations[eq_ID]

      # print("debugging -- make base", ID, eq_ID, var_ID, rendered_equation)
      self.ui.pushButtonLeft.setText("")
      icon, label, size = pixelled_equation
      self.ui.pushButtonLeft.setIcon(icon)
      self.ui.pushButtonLeft.setIconSize(size)
      self.ui.pushButtonLeft.setToolTip("click to accept")
      self.ui.pushButtonLeft.show()

    self.current_base_var_ID = var_ID

  def on_pushButtonLeft_pressed(self):
    # print("deugging -- push left button state:",self.state)

    if self.state == "make_base":
      var_ID = self.current_base_var_ID
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(self.selected_Entity, var_ID)

      self.entity_behaviours[self.selected_InterNetwork].addVariant(self.selected_Entity,
                                                                    "base",
                                                                    entity_assignments)
      self.entity_behaviour_graphs[self.selected_InterNetwork].addVariant(self.selected_Entity,
                                                                          "base",
                                                                          var_equ_tree_graph)

      self.__clearEquationInfrastructure()

      variant_list = self.__makeVariantList()
      if not variant_list:
        return
      self.radio_Variants = Selector(self.radioReceiverVariants)
      self.radio_Variants.makeTextSelector(variant_list, self.layout_Variants)
      self.variant_layout_clean = False

  def __makeVariantList(self):
    variants = sorted(self.entity_behaviours[self.selected_InterNetwork][self.selected_Entity])
    for variant in variants:
      if not self.entity_behaviours[self.selected_InterNetwork][self.selected_Entity][variant]:
        if (variant == "base") or ("base" not in variants):
          del self.entity_behaviours[self.selected_InterNetwork]
          variants = None
        else:
          del self.entity_behaviours[self.selected_InterNetwork][self.selected_Entity][variant]
          variants = sorted(self.entity_behaviours[self.selected_InterNetwork][self.selected_Entity])

    return variants

  def on_pushButtonRight_pressed(self):
    # print("debugging -- push right button")
    pass

  def on_pushButtonSave_pressed(self):
    # print("debugging -- save file")
    # self.ontology_container.writeVariables()

    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    putData(self.entity_behaviours, f)

  def analyseBiPartiteGraph(self, object, var_ID):
    obj = object.replace("|", "_")
    blocked = []
    var_equ_tree_graph, assignments = AnalyseBiPartiteGraph(var_ID,
                                                            self.ontology_container,
                                                            self.ontology_name,
                                                            blocked,
                                                            obj)
    return var_equ_tree_graph, assignments

  def __clearEntityInfrastructure(self):
    if not self.entity_layout_clean:
      cleanLayout(self.layout_Entities)
    self.selected_Entity = None
    self.__clearVariantInfrastructure()
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()
    # print("debugging -- clearing entity infrastructure")
    self.entity_layout_clean = True

  def __clearVariantInfrastructure(self):
    if not self.variant_layout_clean:
      cleanLayout(self.layout_Variants)
    self.selected_variant = None
    self.__clearEquationInfrastructure()
    # print("debugging -- clearing variant infrastructure")
    self.variant_layout_clean = True

  def __clearEquationInfrastructure(self):
    if not self.equation_left_clean:
      cleanLayout(self.layout_Left)
      self.equation_left_clean = True
      # print("debugging -- clearing left ")
    if not self.equation_right_clean:
      cleanLayout(self.layout_Right)
      self.equation_left_clean = True
      # print("debugging -- clearing right ")
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()
    # print("debugging -- clearing equation infrastructure")

  def __makeBase(self):
    self.ui.groupBoxControls.hide()
    # print("debugging -- define base")
    self.state = "make_base"
    self.radio_Left = Selector(self.radioReceiverEquations)
    selected_state_equation_list = self.__makeStateEquationSelector()
    self.equation_left_clean = False
    radio_selected_state_equation_list, self.radio_index = self.__makeRadioSelectorLists(selected_state_equation_list)
    self.radio_Left.makeSelector(self.text_or_pixel, radio_selected_state_equation_list, self.layout_Left)
    self.equation_selection = selected_state_equation_list

  def __makeStateEquationSelector(self):

    nw = self.selected_InterNetwork

    selected_state_equation_list = []
    selected_var_type = None

    for eq_ID in self.equations:
      (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation) = self.equations[eq_ID]

      if nw in self.ontology_container.networks:
        nws = list(self.ontology_container.ontology_tree[nw]["parents"])
        nws.append(nw)
        for p_nw in nws:
          if p_nw in rules["nodes"]:
            selected_var_type = rules["nodes"][p_nw]
        for p_nw in nws:
          if p_nw == nw_eq:  # in self.rendered_equation_dictionary:
            if var_type == selected_var_type:
              selected_state_equation_list.append(eq_ID)

    return selected_state_equation_list

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

  def __makeEquationList(self):

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
