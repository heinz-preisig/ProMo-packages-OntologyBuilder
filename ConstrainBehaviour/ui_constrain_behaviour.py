from os.path import join

from PyQt5 import QtGui, QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getOntologyName
from Common.resource_initialisation import DIRECTORIES
from Common.ontology_container import OntologyContainer
from Common.ui_radio_selector_w_scroll import Ui_Form


class MainWindowImpl(QtWidgets.QWidget):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_Form()
    self.ui.setupUi(self)
    self.move(QtCore.QPoint(0, 0))


    # first get ontology
    self.ontology_name = getOntologyName(task=icon_f, left_icon=None)

    # attach ontology
    self.ontology = OntologyContainer(self.ontology_name)
    location = DIRECTORIES["latex_doc_location"] % self.ontology_name

    RadioSelector = self.__makeAndAddSelector(location,
                                              self.radioReceiver,
                                              -1,
                                              self.ui.verticalLayout,
                                              autoexclusive=False)

  def radioReceiver(self, toggle):
    if toggle:
      print("debugging radio receiver")

  def __makeAndAddSelector(self, latex_file_paths, receiver, index, layout, autoexclusive=True):



    template = join(latex_file_paths, "equation_%s.png")
    f = {}
    f[1] = template%(1)
    f[2] = template%(10)

    for i in f:
      label = QtWidgets.QLabel()
      pix = QtGui.QPixmap(f[i])
      icon = QtGui.QIcon(pix)
      s = pix.size()
      radio_selector = QtWidgets.QRadioButton(label)
      radio_selector.setIcon(icon)
      radio_selector.setIconSize(s)
      layout.addWidget(radio_selector)

      radio_selector.toggled.connect(receiver)

