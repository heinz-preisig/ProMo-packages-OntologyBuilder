from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.ontology_container import OntologyContainer
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.qt_resources import cleanLayout
from Common.resources_icons import roundButton
from OntologyBuilder.ConstrainBehaviour.ui_constrain_behaviour import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import AnalyseBiPartiteGraph


def clearLayout(layout, items=None):
  if items is None:
    items = []
  while layout.count():
    child = layout.takeAt(0)
    if child.widget() is not None:
      child.widget().deleteLater()
    elif child.layout() is not None:
      clearLayout(child.layout())

  if items:
    to_delete = list(items.keys())
    for i in to_delete:
      del items[i]
    layout.update()

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

    # attach ontology
    self.ontology_container = OntologyContainer(self.ontology_name)
    self.location = DIRECTORIES["latex_doc_location"] % self.ontology_name

    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    self.equation_assignment = getData(f)
    self.entity_objects = sorted(self.equation_assignment.keys())

    self.current_entity_object = self.entity_objects[0]
    v = self.equation_assignment[self.current_entity_object]["base"]["tree"]["nodes"]["0"]
    _v, var_ID_str = v.split("_")
    self.current_source_variable = int(var_ID_str)

    self.block = []
    self.radio_selectorEquations = {}
    self.radio_selectorEntities = {}

    self.vbox_entities = QtWidgets.QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
    self.ui.scrollAreaWidgetContentsEntities.setLayout(self.vbox_entities)

    self.vbox_equations = QtWidgets.QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
    self.ui.scrollAreaWidgetContentsEquations.setLayout(self.vbox_equations)

    self.type_behaviour = None
    self.behaviours = ["base", "duplicates", "constrain"]

  def on_radioButtonBaseGraph_pressed(self):
    print("debugging base graph")
    self.type_behaviour = 0
    self.__makeEntitySelector(self.radioReceiverEntity)

  def on_radioButtonDuplicates_pressed(self):
    print("debugging -- duplicates")
    self.type_behaviour = 1
    self.__makeEntitySelector(self.radioReceiverEntity)

  def on_radioButtonConstrain_pressed(self):
    print("debugging -- constrain")
    self.type_behaviour = 2
    self.__makeEntitySelector(self.radioReceiverEntity)

  def on_pushButtonSave_pressed(self):
    print("debugging -- push saved")

  def on_pushButtonCancle_pressed(self):
    print("debugging -- push cancle")

  def on_pushButtonInformation(self):
    print("debugging -- push information")


    # RadioSelector = self.__makeEquationSelector(self.radioReceiver, show="all") #, show=[4, 115])

  def __makeEntitySelector(self, receiver ):
    if  self.radio_selectorEntities:
      return

    entities = self.ontology_container.list_reduced_network_node_objects
    expanded_entities =[]
    for nw in entities:
      for entity in entities[nw]:
        expanded_entities.append("%s|%s"%(nw,entity))
    print("debugging -- entities")
    for entity in expanded_entities:
      radio_selector = QtWidgets.QRadioButton(entity)
      self.vbox_entities.addWidget(radio_selector)

      radio_selector.toggled.connect(receiver)

      self.radio_selectorEntities[entity] = radio_selector

  def radioReceiverEntity(self, toggle):
    if toggle:
      print("debugging == entity reciever")

    for item in self.radio_selectorEntities:
      if self.radio_selectorEntities[item].isChecked():
        print("goit it :", item)
        self.current_entity_object = item



  def radioReceiverEquations(self, toggle):

    if toggle:
      print("debugging radio receiver")
      # eq_removed = self.radio_selectorEquations

    for item in self.radio_selectorEquations:
      if self.radio_selectorEquations[item].isChecked():
        print("goit it :", item)
        self.block.append(int(item))

    self.var_equ_tree, \
    self.equation_assignment["dynamic|lumped"]["base"] = \
      AnalyseBiPartiteGraph(self.current_source_variable,
                            self.ontology_container,
                            self.ontology_name,
                            self.block,
                            self.current_entity_object)

    # clearLayout(self.vbox_equations, self.radio_selector)
    cleanLayout(self.vbox_equations)
    self.__makeEquationSelector(self.radioReceiverEquations)



  def __makeEquationSelector(self, receiver, show):

    # equation_IDs = sorted(self.ontology.equation_variable_dictionary.keys())
    equation_IDs = []
    nodes = self.equation_assignment["dynamic|lumped"]["base"]["tree"]["nodes"]
    first=True
    for i in nodes:
      _eq, eq_str_ID = nodes[i].split("_")
      if _eq == "equation":
        if show == "all":
          equation_IDs.append(eq_str_ID)
        elif  (int(eq_str_ID) in show) or first:
          equation_IDs.append(eq_str_ID)
        first=False

    print("debugging__ eq_IDs", equation_IDs)

    icon, label, pixmap, size = self.__make_icon(equation_IDs[0])
    self.ui.labelSource.setPixmap(pixmap)

    for eq_str_ID in equation_IDs[1:]:
      icon, label, pixmap, size = self.__make_icon(eq_str_ID)
      radio_selector = QtWidgets.QRadioButton(label)
      radio_selector.setIcon(icon)
      radio_selector.setIconSize(size)
      self.vbox_equations.addWidget(radio_selector)

      radio_selector.toggled.connect(receiver)

      s_h = radio_selector.size()
      size += s_h

      self.radio_selectorEquations[eq_str_ID] = radio_selector

    print("debugging -- size", size)

    self.ui.scrollAreaEquations.resize(size)
    self.ui.gridLayout.totalMaximumSize()

  def __make_icon(self, eq_ID):

    template = join(self.location, "equation_%s.png")
    f = template % eq_ID
    label = QtWidgets.QLabel()
    pix = QtGui.QPixmap(f)
    icon = QtGui.QIcon(pix)
    size = pix.size()
    return icon, label, pix, size

  # def initUI(self):
  #   self.scroll = QtWidgets.QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
  #   self.widget = QtWidgets.QWidget()  # Widget that contains the collection of Vertical Box
  #   self.vbox = QtWidgets.QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
  #
  #   for i in range(1, 50):
  #     object = QtWidgets.QLabel("TextLabel")
  #     self.vbox.addWidget(object)
  #
  #   self.widget.setLayout(self.vbox)
  #
  #   # Scroll Area Properties
  #   self.scroll.setVerticalScrollBarPolicy(QtWidgets.ScrollBarAlwaysOn)
  #   self.scroll.setHorizontalScrollBarPolicy(QtWidgets.ScrollBarAlwaysOff)
  #   self.scroll.setWidgetResizable(True)
  #   self.scroll.setWidget(self.widget)
  #
  #   self.setCentralWidget(self.scroll)
  #
  #   self.setGeometry(600, 100, 1000, 900)
  #   self.setWindowTitle('Scroll Area Demonstration')
  #   self.show()
  #
  #   return
