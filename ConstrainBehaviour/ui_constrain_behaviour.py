from PyQt5 import QtGui, QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets

from Common.common_resources import getOntologyName
from Common.ontology_container import OntologyContainer
from Common.ui_radio_selector_w_scroll import Ui_Form


class MainWindowImpl(QtWidgets.QWidget):
  def __init__(self):

    super().__init__()
    self.ui = Ui_Form()
    self.ui.setupUi(self)
    self.move(QtCore.QPoint(0, 0))

    # first get ontology
    self.ontology_name = getOntologyName(task="task_model_composer", left_icon=None)

    # attach ontology
    self.ontology = OntologyContainer(self.ontology_name)
    self.ontology.variables

    RadioSelector = self.__makeAndAddSelector("equations",
                                              "gugus",
                                              "gugus",
                                              self.radioReceiver,
                                              -1,
                                              self.ui.verticalLayout,
                                              autoexclusive=False)

  def radioReceiver(self, toggle):
    if toggle:
      print("debugging radio receiver")

  def __makeAndAddSelector(self, title, variable_paths_list,equation_paths_list, receiver, index, layout, autoexclusive=True):

    location = "/home/heinz/1_Gits/CAM-projects_v8/Ontology_Repository/HAP_Ontology_Repository-playground_v8/LaTeX/"
    template = "%sequation_%s.png"
    f = {}
    f[1] = template%(location,1)
    f[2] = template%(location, 10) #"/home/heinz/1_Gits/CAM-projects_v8/ProMo/packages/Common/equation_10.png"
    # print("current dir", f)

    # pm1 = QtGui.QPixmap(f[1])
    # pm2 = QtGui.QPixmap(f[2])
    # w1 = pm1.size().width()
    # w2 = pm2.size().width()
    # h = pm1.size().height()
    # pm = QtGui.QPixmap(w1+w2, h)
    # label = QtWidgets.QLabel()
    # left_rectF = QtCore.QRectF(0, 0, w1, h)  # the left half
    # right_rectF = QtCore.QRectF(w1, 0, w1, h)  # the right half
    # painter = QtGui.QPainter(pm)
    # painter.drawPixmap(left_rectF, pm1, QtCore.QRectF(pm1.rect()))
    # painter.drawPixmap(right_rectF, pm2, QtCore.QRectF(pm2.rect()))
    # del painter
    # # label.setPixmap(pm)
    #
    # icon = QtGui.QIcon(pm)
    # s = pm.size()
    # radio_selector = QtWidgets.QRadioButton(label)
    # radio_selector.setIcon(icon)
    # radio_selector.setIconSize(s)
    # layout.addWidget(radio_selector)
    #
    # radio_selector.toggled.connect(receiver)

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

