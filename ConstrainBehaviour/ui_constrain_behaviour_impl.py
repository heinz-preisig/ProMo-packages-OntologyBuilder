from os.path import join

from PyQt5 import QtGui, QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getOntologyName
from Common.common_resources import getData
from Common.resource_initialisation import DIRECTORIES, FILES
from Common.ontology_container import OntologyContainer
from OntologyBuilder.ConstrainBehaviour.ui_constrain_behaviour import Ui_MainWindow


class MainWindowImpl(QtWidgets.QMainWindow):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)
    self.move(QtCore.QPoint(0, 0))


    # first get ontology
    self.ontology_name = getOntologyName(task=icon_f, left_icon=None)

    # attach ontology
    self.ontology = OntologyContainer(self.ontology_name)
    self.location = DIRECTORIES["latex_doc_location"] % self.ontology_name

    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    self.equation_assignment = getData(f)



    RadioSelector = self.__makeAndAddSelector(self.radioReceiver,
                                              autoexclusive=False)

  def radioReceiver(self, toggle):
    if toggle:
      print("debugging radio receiver")

  def __makeAndAddSelector(self, receiver, autoexclusive=True):


    vbox = QtWidgets.QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
    self.ui.scrollAreaWidgetContents.setLayout(vbox)

    # equation_IDs = sorted(self.ontology.equation_variable_dictionary.keys())
    equation_IDs = []
    nodes = self.equation_assignment["dynamic|lumped"]["base"]["tree"]["nodes"]
    for i in nodes:
      _eq, eq_ID = nodes[i].split("_")
      if _eq == "equation":
        equation_IDs.append(eq_ID)

    print("debugging__ eq_IDs", equation_IDs)

    icon,label,pixmap, size = self.__make_icon(equation_IDs[0])
    self.ui.labelSource.setPixmap(pixmap)

    for eq_ID in equation_IDs[1:]:
      icon, label, pixmap, size = self.__make_icon(eq_ID)
      radio_selector = QtWidgets.QRadioButton(label)
      radio_selector.setIcon(icon)
      radio_selector.setIconSize(size)
      vbox.addWidget(radio_selector)

      radio_selector.toggled.connect(receiver)

      s_h = radio_selector.size()
      size += s_h

    print("debugging -- size", size)

    self.ui.scrollArea.resize(size)
    self.ui.verticalLayout.totalMaximumSize()

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