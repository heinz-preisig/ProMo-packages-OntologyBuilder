from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.ontology_container import OntologyContainer
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.resource_initialisation import checkAndFixResources
from Common.qt_resources import cleanLayout
from Common.resources_icons import roundButton
from OntologyBuilder.BehaviourEditor.ui_behaviour_linker_editor import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal

from OntologyBuilder.OntologyEquationEditor.resources import AnalyseBiPartiteGraph

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
      self.radios[ID].resize(0,0)    # Note: not sure what I am doing here -- reduces gaps between
      layout.addWidget(self.radios[ID])

      self.radios[ID].toggled.connect(self.selector_toggled)

      ID += 1
    return self.radios

  def selector_toggled(self, toggled):
    print("debugging -- toggled", toggled)
    if toggled:
      count = -1
      for label in self.radios:
        count += 1
        if self.radios[label].isChecked():
          print("goit it :", label)
          self.radio_signal.emit(str(label), count)


class MainWindowImpl(QtWidgets.QMainWindow):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.move(QtCore.QPoint(0, 0))

    roundButton(self.ui.pushButtonInformation, "info", tooltip="information")
    roundButton(self.ui.pushButtonSave, "save", tooltip="save entity behaviour")
    roundButton(self.ui.pushButtonCancle, "exit", tooltip="cancel and exit")

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
    self.vbox_InterNetworks = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsInterNetworks.setLayout(self.vbox_InterNetworks)

    self.vbox_Entities = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsEntities.setLayout(self.vbox_Entities)

    self.vbox_Variants = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsVariants.setLayout(self.vbox_Variants)

    self.vbox_Left = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsLeft.setLayout(self.vbox_Left)

    self.vbox_Right = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsRight.setLayout(self.vbox_Right)

    self.radio_InterNetworks = {}
    self.radio_Entities = {}
    self.radio_Variants = {}
    self.radio_Entities = {}
    self.radio_Left = {}
    self.radio_Right = {}

    self.selected_InterNetwork = None
    self.selected_Entity = None
    self.sected_variant = "base"
    self.radio_index = None

    # controls
    self.actions = ["duplicates", "new_variant", "edit_variant", "instantiate_variant"]

    # get existing data
    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    self.equation_assignment = getData(f)
    if not self.equation_assignment:
      print("debugging -- no data")

    # prepare lists
    self.equations = self.__makeEquationList()

    # start process
    inter_networks = self.ontology_container.list_inter_branches
    self.radio_InterNetworks = Selector(self.radioReceiverInterNetworks)
    self.radio_InterNetworks.makeTextSelector(inter_networks, self.vbox_InterNetworks)

  def radioReceiverInterNetworks(self, ID, index):
    print("debugging -- receiver InterNetworks", ID)
    self.selected_InterNetwork = ID

    entities_list = self.reduced_network_node_list[self.selected_InterNetwork]
    self.radio_Entities = Selector(self.radioReceiverEntities)
    self.radio_Entities.makeTextSelector(entities_list, self.vbox_Entities)

  def radioReceiverEntities(self, ID, index):
    print("debugging -- receiver Entities", ID)
    self.selected_Entity = ID
    define_base = True
    if self.selected_InterNetwork in self.equation_assignment:
      if self.selected_Entity in self.equation_assignment[self.selected_InterNetwork]:
        if "base" in self.equation_assignment[self.selected_InterNetwork][self.selected_Entity]:
          print("debugging -- base is defined")
          define_base = False
        else:
          self.equation_assignment[self.selected_InterNetwork][self.selected_Entity]["base"] = {}
      else:
        self.equation_assignment[self.selected_InterNetwork][self.selected_Entity] = {}
        self.equation_assignment[self.selected_InterNetwork][self.selected_Entity]["base"] = {}
    else:
      self.equation_assignment[self.selected_InterNetwork] = {}
      self.equation_assignment[self.selected_InterNetwork][self.selected_Entity] = {}
      self.equation_assignment[self.selected_InterNetwork][self.selected_Entity]["base"] = {}

    if define_base:
      self.equation_assignment[self.selected_InterNetwork][self.selected_Entity]["base"] = self.__makeBase()
      print("debugging -- prepared a new base")
      self.__makeBase()

  def radioReceiverEquations(self, equ_text, index):

    print("debugging -- node equations checked", equ_text, index)
    # self.analyseBiPartiteGraph(self.selected_node, var_ID)
    pass

  def __makeBase(self):
    print("debugging -- define base")
    self.radio_Left = Selector(self.radioReceiverEquations)
    selected_state_equation_list = self.__makeStateEquationSelector()
    radio_selected_state_equation_list, self.radio_index = self.__makeRadioSelectorLists(selected_state_equation_list)

    self.radio_Left.makeTextSelector(radio_selected_state_equation_list["rendered"], self.vbox_Left)
    self.radio_Left.makePixelSelector(radio_selected_state_equation_list["pixelled"], self.vbox_Right)


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

    radio_selectors = {"rendered": [],
                       "pixelled": []}

    index = {"variable": [], "equation" : []}
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