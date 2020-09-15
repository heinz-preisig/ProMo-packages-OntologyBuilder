#!/usr/local/bin/python3
# encoding: utf-8

"""
===============================================================================
 editor for typed tokens -- list definition and conversion
===============================================================================


"""

__project__ = "ProcessModeller  Suite"
__author__ = "PREISIG, Heinz A"
__copyright__ = "Copyright 2015, PREISIG, Heinz A"
__since__ = "2019. 01. 04"
__license__ = "GPL planned -- until further notice for Bio4Fuel & MarketPlace internal use only"
__version__ = "6.00"
__email__ = "heinz.preisig@chemeng.ntnu.no"
__status__ = "beta"

from collections import OrderedDict

from PyQt5 import QtCore
from PyQt5 import QtWidgets

from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.common_resources import M_None
from Common.common_resources import putData
from Common.ontology_container import OntologyContainer
from Common.resource_initialisation import FILES
from OntologyBuilder.TypedTokenEditor.editor_typed_token import Ui_MainWindow

SPACING = 20
INSTANCES = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", ]


class Conversion(dict):
  def __init__(self, reactants, products):
    dict.__init__(self)
    self["reactants"] = reactants
    self["products"] = products


class TypedTokenData(OrderedDict):

  def __init__(self, file=None):
    OrderedDict.__init__(self)
    if file:
      self.read(file)
    else:
      pass

  def initialise(self, typed_tokens):
    for ttoken in typed_tokens:
      self[ttoken] = {}
      self[ttoken]["instances"] = []
      self[ttoken]["conversions"] = []

  def write(self, f):
    # print("write typed-tokens to %s" % f)
    putData(self, f, indent=2)

  def read(self, f):
    data = getData(f)
    if data:
      for hash in data:
        self[hash] = data[hash]
    # print("debugging")


class TypedRadioButton(QtWidgets.QRadioButton):
  def __init__(self, ID, typed_token):
    QtWidgets.QRadioButton.__init__(self, ID)
    self.ID = ID
    self.typed_token = typed_token
    self.setFixedHeight(SPACING)
    self.setAutoExclusive(False)


class Ui_TokenEditor(QtWidgets.QMainWindow):
  def __init__(self):
    QtWidgets.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    # attach ontology
    ontology_name = getOntologyName()
    ontology = OntologyContainer(ontology_name)  # DIRECTORIES["ontology_location"] % ontology_name)
    self.networks = ontology.list_leave_networks

    self.typed_token_file_spec = FILES["typed_token_file"] % ontology_name

    self.DATA = TypedTokenData()

    typed_tokens = []
    for nw in self.networks:
      for token in ontology.token_typedtoken_on_networks[nw]:
        for typed_token in ontology.token_typedtoken_on_networks[nw][token]:
          typed_tokens.append(typed_token)

    self.DATA.initialise(typed_tokens)
    self.__interfaceLogics("start")

  def __interfaceLogics(self, state):

    if state == "start":
      # self.ui.groupSaving.hide()
      self.ui.groupToken.hide()
      self.ui.groupConversion.hide()
      #
      # TODO: "save as" is not yet implemented - file name is fixed and one only
      self.ui.pushSaveAs.hide()

    elif state == "new":
      self.ui.pushLoad.hide()
      self.ui.groupToken.show()
      self.ui.groupStart.hide()

    elif state == "loaded":
      self.ui.groupToken.show()
      self.ui.spinNumberOfTypedTokens.hide()
      self.ui.groupStart.hide()

    elif state == "converting token defined":
      self.ui.groupConversion.show()
      self.ui.spinNumberOfTypedTokens.show()

    elif state == "not converting token define":
      self.ui.groupConversion.hide()
      self.ui.spinNumberOfTypedTokens.show()

    elif state == "modified":
      self.ui.groupSaving.show()

    elif state == "saved":
      self.ui.groupSaving.hide()

  def __makeTokenWithTypedTokensCombo(self):

    self.ui.comboTokenWithTypedTokens.clear()
    self.ui.comboTokenWithTypedTokens.addItem(M_None)
    ### tokens
    tokens = sorted(self.DATA.keys())  # self.tokens_without_conversion | self.tokens_with_conversion
    self.ui.comboTokenWithTypedTokens.addItems(list(tokens))

    return list(tokens)

  def __setupSpinNumberOfTypedTokens(self):
    min_no = self.__minNumberTypedTokens()
    self.ui.spinNumberOfTypedTokens.setMinimum(min_no)
    # print("min no", min_no)

  def __makeConversionCombos(self):
    self.ui.comboConversion.clear()

    conversions = self.DATA[self.token]["conversions"]

    if len(conversions) == 0:
      self.ui.spinConverstion.hide()
      self.ui.comboConversion.hide()
    else:
      self.ui.spinConverstion.setMinimum(0)
      self.ui.spinConverstion.setMaximum(len(conversions) - 1)
      for c in conversions:
        s = "%s --> %s" % (c["reactants"], c["products"])
        self.ui.comboConversion.addItem(s)
      self.ui.spinConverstion.show()
      self.ui.comboConversion.show()

  def __cleanLayout(self, layout):
    """ removes the widgets from the layout """
    for i in reversed(range(layout.count())):
      widgetToRemove = layout.itemAt(i).widget()
      # remove it from the layout list
      layout.removeWidget(widgetToRemove)
      # remove it from the gui
      widgetToRemove.setParent(None)

  def on_comboTokenWithTypedTokens_activated(self, token):
    s = self.ui.comboTokenWithTypedTokens.currentText()  # str(token)
    if s == M_None: return

    self.token = s
    self.__interfaceLogics("converting token defined")

    min_no = self.__minNumberTypedTokens()
    self.ui.spinNumberOfTypedTokens.setValue(min_no)
    self.__makeConversionCombos()

  def __minNumberTypedTokens(self):
    conversions = self.DATA[self.token]["conversions"]
    if len(conversions) == 0:
      return 1

    index = -1
    for no in range(len(INSTANCES)):
      s = INSTANCES[no]
      for c in conversions:
        for r in c["reactants"]:
          if r == s:
            if index < no:
              index = no
        for r in c["products"]:
          if r == s:
            if index < no:
              index = no

    return index + 1

  def on_spinNumberOfTypedTokens_valueChanged(self, no_of_typed_tokens):
    self.ui.message_box.clear()
    token = self.token
    tmp_instances = INSTANCES[0:int(no_of_typed_tokens)]
    differences = list(set(self.DATA[token]['instances']) - set(tmp_instances))
    strt = "<span style=\" font-size:10pt; font-weight:600;color:#ff0000;\">\n"
    msg = 'ERROR: Cannot remove typed token: {} \n used in conversion: {}'
    end_of_string = "</span>"
    for diff in differences:
      for i, conversion in enumerate(self.DATA[token]['conversions']):
        if diff in conversion['reactants'] or diff in conversion['reactants']:
          out_msg = msg.format(diff, i)
          self.ui.pushSave.hide()
          self.ui.message_box.setText(strt + out_msg + end_of_string)
          return  # Exit before redrawing
    self.ui.pushSave.show()
    self.redraw_conversion_radios(no_of_typed_tokens)
    self.DATA[self.token]["instances"] = tmp_instances
    ok_msg = 'Last new typed token: {}'
    self.ui.message_box.setText(ok_msg.format(tmp_instances[-1]))

  def redraw_conversion_radios(self, no_of_typed_tokens):
    self.__interfaceLogics("modified")
    token = self.token
    self.__cleanLayout(self.ui.formReactants)
    self.__cleanLayout(self.ui.formProducts)
    self.radioButtonsTokens = {
            "reactants": {},
            "products" : {}
            }
    for no in range(int(no_of_typed_tokens)):
      self.radioButtonsTokens[token] = {}
      t = INSTANCES[no]
      label = "%s :: %s" % (token, t)
      r = TypedRadioButton(label, t)
      self.radioButtonsTokens["reactants"][no] = r
      self.ui.formReactants.setWidget(no, QtWidgets.QFormLayout.LabelRole, r)
      r = TypedRadioButton(label, t)
      self.radioButtonsTokens["products"][no] = r
      self.ui.formProducts.setWidget(no, QtWidgets.QFormLayout.LabelRole, r)

  @QtCore.pyqtSlot(int)
  def on_spinConverstion_valueChanged(self, index):
    # print(" change index: ", index)
    self.ui.comboConversion.setCurrentIndex(index)

  def on_comboConversion_activated(self, index):
    set_products = self.ui.comboConversion.currentText()
    r, p = self.products = set_products.split('-->')
    index = self.ui.comboConversion.currentIndex()
    self.ui.spinConverstion.setValue(index)

  def on_pushNewSystem_pressed(self):
    self.ui.message_box.clear()
    self.ui.message_box.setText('Setting up new typed token file')
    tokens = self.__makeTokenWithTypedTokensCombo()
    self.__interfaceLogics("new")

  def on_pushLoad_pressed(self):
    self.ui.message_box.clear()
    self.ui.message_box.setText('Loading previous typed token file')
    tokens = self.__makeTokenWithTypedTokensCombo()
    self.DATA.read(self.typed_token_file_spec)
    self.__interfaceLogics("loaded")

  def on_pushSave_pressed(self):
    self.ui.message_box.clear()
    self.ui.message_box.setText('Saving typed token file to:\n'
                                + str(self.typed_token_file_spec))
    self.DATA.write(self.typed_token_file_spec)
    self.__interfaceLogics("saved")
    pass

  def on_pushSaveAs_pressed(self):
    pass

  def on_pushNewConversion_pressed(self):
    reactants = []
    products = []
    for r in self.radioButtonsTokens["reactants"]:
      a = self.radioButtonsTokens["reactants"][r]
      if a.isChecked():
        reactants.append(a.typed_token)
        a.setChecked(False)
      b = self.radioButtonsTokens["products"][r]
      if b.isChecked():
        products.append(b.typed_token)
        b.setChecked(False)

    c = Conversion(reactants, products)
    self.DATA[self.token]["conversions"].append(c)
    min_inst = self.__minNumberTypedTokens()
    self.DATA[self.token]["instances"] = INSTANCES[0:min_inst]
    self.__makeConversionCombos()
    self.__interfaceLogics("modified")

  def on_pushDelete_pressed(self):
    c = self.DATA[self.token]["conversions"].pop(self.ui.spinConverstion.value())
    self.__makeConversionCombos()
    self.__setupSpinNumberOfTypedTokens()
    self.__interfaceLogics("modified")
