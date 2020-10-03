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
__since__ = "2014. 08. 09"
__license__ = "GPL planned -- until further notice for Bio4Fuel & MarketPlace internal use only"
__version__ = "6.00"
__email__ = "heinz.preisig@chemeng.ntnu.no"
__status__ = "beta"

import os
import subprocess
from collections import OrderedDict

import pydotplus.graphviz as GV  # python3 -m pip install pydotplus
from jinja2 import Environment  # sudo apt-get install python-jinja2
from jinja2 import FileSystemLoader
from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from Common.common_resources import CONNECTION_NETWORK_SEPARATOR
from Common.resources_icons import getIcon
from Common.common_resources import getOntologyName
from Common.common_resources import makeTreeView
from Common.common_resources import putData
from Common.resources_icons import roundButton
from Common.common_resources import saveBackupFile
from Common.ontology_container import OntologyContainer
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.ui_text_browser_popup_impl import UI_FileDisplayWindow
from OntologyBuilder.OntologyEquationEditor.resources import ENABLED_COLUMNS
from OntologyBuilder.OntologyEquationEditor.ui_variabletable_show_impl import UI_VariableTableShow
from OntologyBuilder.OntologyEquationEditor.resources import LANGUAGES
from OntologyBuilder.OntologyEquationEditor.resources import make_variable_equation_pngs
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal
from OntologyBuilder.OntologyEquationEditor.tpg import LexicalError
from OntologyBuilder.OntologyEquationEditor.tpg import SemanticError
from OntologyBuilder.OntologyEquationEditor.tpg import SyntacticError
from OntologyBuilder.OntologyEquationEditor.tpg import WrongToken
from OntologyBuilder.OntologyEquationEditor.ui_aliastableindices_impl import UI_AliasTableIndices
from OntologyBuilder.OntologyEquationEditor.ui_aliastablevariables_impl import UI_AliasTableVariables
from OntologyBuilder.OntologyEquationEditor.ui_equations_impl import UI_Equations
from OntologyBuilder.OntologyEquationEditor.ui_ontology_design import Ui_OntologyDesigner
from OntologyBuilder.OntologyEquationEditor.ui_variabletable_impl import UI_VariableTableDialog
from OntologyBuilder.OntologyEquationEditor.variable_framework import IndexStructureError
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeCompiler
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeIncidenceDictionaries
from OntologyBuilder.OntologyEquationEditor.variable_framework import makeIncidentList
from OntologyBuilder.OntologyEquationEditor.variable_framework import UnitError
from OntologyBuilder.OntologyEquationEditor.variable_framework import VarError
from OntologyBuilder.OntologyEquationEditor.variable_framework import Variables  # Indices

# RULE: fixed wired for initialisation -- needs to be more generic
INITIALVARIABLE_TYPES = {
        "initialise" : ["state", "frame"],
        "connections": ["constant", "transposition"]
        }

CHOOSE_NETWORK = "choose network"
CHOOSE_INTER_CONNECTION = "choose INTER connection"
CHOOSE_INTRA_CONNECTION = "choose INTRA connection"


class EditorError(Exception):
  """
  Exception reporting
  """

  def __init__(self, msg):
    self.msg = msg


class UiOntologyDesign(QMainWindow):
  """
  Main window for the ontology design:
  """

  def __init__(self):
    """
    The editor has  the structure of a wizard,  thus goes through several steps
    to define the ontology.
    - get the base ontology that provides the bootstrap procedure.
    - construct the index sets that are used in the definition of the different
      mathematical objects
    - start building the ontology by defining the state variables
    """

    # set up dialog window with new title
    QMainWindow.__init__(self)
    self.ui = Ui_OntologyDesigner()
    self.ui.setupUi(self)
    # self.ui.pushBack.setIcon(getIcon('^'))
    self.ui.pushWrite.setIcon(getIcon('->'))
    self.setWindowTitle("OntologyFoundationEditor Design")
    roundButton(self.ui.pushInfo, "info", tooltip="information")
    roundButton(self.ui.pushCompile, "compile", tooltip="compile")

    roundButton(self.ui.pushShowVariables, "variable_show", tooltip="show variables")
    roundButton(self.ui.pushWrite, "save", tooltip="save")

    self.radio = [
            self.ui.radioVariables,
            self.ui.radioVariablesAliases,
            self.ui.radioIndicesAliases
            ]
    [i.hide() for i in self.radio]

    self.ui.groupFiles.hide()
    self.ui.groupVariables.hide()

    try:
      assert os.path.exists(DIRECTORIES["ontology_repository"])
    except:
      print("directory %s does not exist" % DIRECTORIES["ontology_repository"])

    a = DIRECTORIES["ontology_repository"]
    self.ontology_name = getOntologyName(task="task_ontology_equations")
    if not self.ontology_name:
      os._exit(-1)

    ### set up editor =================================================
    self.current_network = None  # holds the current ontology space name
    self.current_variable_type = None
    self.edit_what = None
    self.state = None  # holds this programs state

    # get ontology
    self.ontology_location = DIRECTORIES["ontology_location"] % str(self.ontology_name)
    self.ontology_container = OntologyContainer(self.ontology_name)
    self.ui.groupOntology.setTitle("ontology : %s" % self.ontology_name)
    # works only for colour and background not font size and font style
    # style = "QGroupBox:title {color: rgb(1, 130, 153);}" # not supported: font-size: 48pt;  background-color:
    # yellow; font-style: italic}"
    # self.ui.groupOntology.setStyleSheet(style)

    self.variable_types_on_networks = self.ontology_container.variable_types_on_networks
    # self.variable_types_on_networks_per_component = self.ontology_container.variable_types_on_networks_per_component
    self.converting_tokens = self.ontology_container.converting_tokens

    self.rules = self.ontology_container.rules
    self.ontology_hiearchy = self.ontology_container.ontology_hiearchy
    self.networks = self.ontology_container.networks
    self.interconnection_nws = self.ontology_container.interconnection_network_dictionary
    self.intraconnection_nws = self.ontology_container.intraconnection_network_dictionary
    self.intraconnection_nws_list = list(self.intraconnection_nws.keys())
    self.interconnection_nws_list = list(self.interconnection_nws.keys())

    self.indices = self.ontology_container.indices  # readIndices()  # indices
    self.variables = Variables(self.ontology_container)
    self.variables.importVariables(self.ontology_container.variables, self.indices)  # also link the indices for compilation

    # ### converting version 6 --> 7:
    # if self.ontology_container.version_variable_equation == "6":
    #   for var_ID in self.variables:
    #     equations = self.variables[var_ID].equations
    #     for equ_ID in equations:
    #       compiler = makeCompiler(self.variables, self.indices, var_ID, equ_ID, language="global_ID")
    #       try:
    #         expression = equations[equ_ID]["rhs"]
    #         res = compiler(expression)
    #       except (SemanticError,
    #               SyntacticError,
    #               LexicalError,
    #               WrongToken,
    #               UnitError,
    #               IndexStructureError,
    #               VarError,
    #               ) as _m:
    #         print('checked expression failed %s -- %s' % (self.variables[var_ID].label, _m))
    #         res = compiler(expression)  # NOTE: for debugging
    #         os._exit(-1)
    #         res = None
    #
    #       # the following is all a little tricky. Direct assignment fails...
    #       ID_string = deepcopy(str(res))
    #       # print(ID_string)
    #       self.variables[var_ID].equations[equ_ID]["rhs"] = ID_string
    #   self.ontology_container.writeVariables(self.variables)
    #
    #   _answ = makeMessageBox("variable file was converted from version 6 to 7 \n restart", buttons=["OK"])
    #
    #   os._exit(-1)

    # ============================================  continue for version 7 code =======================================
    self.state = "edit"

    # setup for next GUI-phase
    [i.show() for i in self.radio]
    makeTreeView(self.ui.treeWidget, self.ontology_container.ontology_tree)
    self.ui.combo_InterConnectionNetwork.clear()
    self.ui.combo_IntraConnectionNetwork.clear()
    self.ui.combo_InterConnectionNetwork.addItems(self.interconnection_nws_list)
    self.ui.combo_IntraConnectionNetwork.addItems(self.intraconnection_nws_list)
    self.ui.combo_InterConnectionNetwork.show()
    self.ui.combo_IntraConnectionNetwork.show()
    self.ui.groupFiles.hide()
    self.ui.groupEdit.hide()

    # prepare for compiled versions
    self.compiled_equations = {language: {} for language in LANGUAGES["compile"]}
    self.compiled_equations[LANGUAGES["global_ID_to_internal"]] = {}
    self.compiled_variable_labels = {}

    self.compile_only = True

    # self.__compile("latex")
    # self.__compile("python")
    # self.__compile("cpp")
    # self.__compile("matlab")

    # self.__makeDotGraphs()
    return

  def on_pushInfo_pressed(self):
    msg_popup = UI_FileDisplayWindow(FILES["info_ontology_design_editor"])
    msg_popup.exec_()

  def on_radioVariables_pressed(self):
    self.__checkRadios("variables")
    self.__hideTable()
    self.ui.groupVariables.show()
    if self.current_network:
      self.ui.groupEdit.show()
      self.ui.combo_EditVariableTypes.show()
      # self.table_aliases_v.hide()
      # self.table_aliases_i.hide()
      self.__writeMessage("edit variables/equations")
    else:
      self.__writeMessage("select variable type first")

  def on_radioVariablesAliases_pressed(self):
    self.__checkRadios("variable_aliases")
    self.__hideTable()
    self.__writeMessage("edit variable alias table")
    self.ui.groupVariables.show()
    self.ui.groupEdit.hide()
    self.ui.combo_EditVariableTypes.hide()
    if self.current_network:
      self.__setupVariablesAliasTable()
    else:
      self.__writeMessage("select variable type first")
      # self.ui.radioVariablesAliases.setDown(False)

  def on_radioIndicesAliases_pressed(self):
    self.__checkRadios("indices_aliase")
    self.__hideTable()
    self.__writeMessage("edit alias table")
    self.ui.groupVariables.hide()
    self.__setupIndicesAliasTable()
    # self.ontology_container.indices = self.indices #(self.indices, ["index", "block_index"])



  def on_pushCompile_pressed(self):
    # self.__checkRadios("compile")
    # self.compile_only = True
    for l in LANGUAGES["code_generation"]:
      try:
        self.__compile(l)
      except (EditorError) as error:
        self.__writeMessage(error.msg)

    self.__compile("latex")
    self.__writeMessage("finished latex document")

    self.__makeRenderedOutput()

  def on_pushShowVariables_pressed(self):
    self.__makeVariableTable()

  def __makeVariableTable(self):
    print("debugging -- make variable table")
    enabled_var_types = self.variable_types_on_networks[self.current_network]
    variable_table = UI_VariableTableShow("All defined variables",
                                   self.variables,
                                   self.indices,
                                   self.current_network,
                                   enabled_var_types,
                                   [],
                                   [],
                                   None,
                                  ["info", "new", "port"]
                                   )
    variable_table.exec_()

  def on_pushFinished_pressed(self):
    print("debugging -- got here")

  def on_radioGraph_clicked(self):
    self.__hideTable()
    self.ui.combo_EditVariableTypes.clear()
    self.ui.combo_EditVariableTypes.addItems(
            self.ontology_container.ontology_tree[self.current_network]["behaviour"]["graph"])

  def on_radioNode_clicked(self):
    self.__hideTable()
    self.ui.combo_EditVariableTypes.clear()
    self.ui.combo_EditVariableTypes.addItems(
            self.ontology_container.ontology_tree[self.current_network]["behaviour"]["node"])

  def on_radioArc_clicked(self):
    self.__hideTable()
    self.ui.combo_EditVariableTypes.clear()
    self.ui.combo_EditVariableTypes.addItems(
            self.ontology_container.ontology_tree[self.current_network]["behaviour"]["arc"])

  def on_treeWidget_clicked(self, index):  # state network_selected
    self.current_network = str(self.ui.treeWidget.currentItem().name)
    self.__writeMessage("current network selected: %s" % self.current_network)
    # print(">>> ", self.ui.radioVariablesAliases.isDown(), self.ui.radioVariablesAliases.isChecked())
    if self.ui.radioVariablesAliases.isChecked():
      # self.ui.radioVariablesAliases.setDown(False)
      self.on_radioVariablesAliases_pressed()
    elif self.ui.radioVariables.isChecked():
      self.__setupEdit("networks")
      self.ui.groupEdit.show()
      self.ui.combo_EditVariableTypes.show()
      self.on_radioVariables_pressed()

  @QtCore.pyqtSlot(str)
  def on_combo_InterConnectionNetwork_activated(self, choice):
    self.__hideTable()
    self.current_network = str(choice)
    self.state = "inter_connections"
    self.__setupEdit("interface")

  @QtCore.pyqtSlot(str)  # combo_IntraConnectionNetwork
  def on_combo_IntraConnectionNetwork_activated(self, choice):
    self.__hideTable()
    self.current_network = str(choice)
    self.state = "intra_connections"
    self.__setupEdit("intraface")

  @QtCore.pyqtSlot(int)
  def on_tabWidget_currentChanged(self, which):
    # print("debugging -- changed tab")
    self.ui.combo_EditVariableTypes.hide()

  def __setupEdit(self, what):
    """

    @param what: string "network" | "interface" | "intraface"
    @return: None
    """

    self.__hideTable()

    nw = self.current_network

    if what == "interface":
      vars_types_on_network_variable = self.ontology_container.interfaces[nw]["internal_variable_classes"]
      self.ui.combo_EditVariableTypes.clear()
      self.ui.combo_EditVariableTypes.addItems(vars_types_on_network_variable)
      network_for_variable = nw
      network_for_expression = nw  # self.ontology_container.interfaces[nw]["left_network"]
      # network_variable_source = self.ontology_container.interfaces[nw]["left_network"]
      vars_types_on_network_expression = self.ontology_container.interfaces[nw]["left_variable_classes"]
    elif what in "intraface":
      network_for_variable = nw  # self.intraconnection_nws[nw]["right"]
      _types = self.ontology_container.variable_types_on_networks
      _left = self.intraconnection_nws[nw]["left"]
      _right = self.intraconnection_nws[nw]["right"]
      _set = set(_types[_left]) | set(_types[_right])
      network_for_expression = nw
      # network_for_expression = list(_set) #self.intraconnection_nws[nw]["left"]  # NOTE: this should be all from both sides
      # network_variable_source = network_for_expression
      # vars_types_on_network_variable = self.ontology_container.variable_types_on_networks[network_for_variable]
      # RULE: NOTE: the variable types are the same on the left, the right and the boudnary -- at least for the time
      # being
      vars_types_on_network_variable = sorted(_set) #self.ontology_container.variable_types_on_networks[network_for_expression]
      self.ui.combo_EditVariableTypes.clear()
      self.ui.combo_EditVariableTypes.addItems(vars_types_on_network_variable)
      vars_types_on_network_expression = list(_set) #self.ontology_container.variable_types_on_networks[network_for_expression]
    else:
      self.ui.radioNode.toggle()
      self.on_radioNode_clicked()
      network_for_variable = nw
      network_for_expression = nw

      vars_types_on_network_variable = sorted(self.ontology_container.variable_types_on_networks[network_for_variable])

      interface_variable_list = []
      oc = self.variables.ontology_container
      for nw in oc.heirs_network_dictionary[network_for_expression]:
        for inter_nw in oc.interconnection_network_dictionary:
          if oc.interconnection_network_dictionary[inter_nw]["right"] == nw:
            interface_variable_list.append(inter_nw)
          # print("debugging -- inter_nw", inter_nw)

      network_variable_source = network_for_expression
      vars_types_on_network_expression = sorted(self.ontology_container.variable_types_on_networks[network_variable_source])
      for nw in interface_variable_list:
        for var_type in self.ontology_container.variable_types_on_interfaces[nw]:
          vars_types_on_network_expression.append(var_type)
      vars_types_on_network_expression = list(set(vars_types_on_network_expression))


    self.ui_eq = UI_Equations(what,  # what: string "network" | "interface" | "intraface"
                              self.variables,
                              self.indices,
                              network_for_variable,
                              network_for_expression,
                              vars_types_on_network_variable,
                              vars_types_on_network_expression
                              )
    self.ui_eq.update_space_information.connect(self.__updateVariableTable)

    self.ui.combo_EditVariableTypes.show()
    self.ui.groupFiles.show()
    self.ui.groupEdit.show()
    self.ui.pushWrite.show()

  def __hideTable(self):
    if "table_variables" in self.__dir__():
      self.table_variables.hide()
    if "table_aliases_i" in self.__dir__():
      self.table_aliases_i.close()
    if "table_aliases_v" in self.__dir__():
      self.table_aliases_v.close()

  @QtCore.pyqtSlot(str)
  def on_combo_EditVariableTypes_activated(self, selection):
    selection = str(selection)
    if selection == "choose":
      return

    self.current_variable_type = selection
    self.ui.groupEdit.show()
    self.__setupVariableTable()
    self.table_variables.show()

    self.ui.combo_EditVariableTypes.show()
    self.ui.groupFiles.show()
    self.ui.pushWrite.show()
    self.ui.groupEdit.show()

  def on_pushWrite_pressed(self):
    filter = self.ontology_container.variable_record_filter
    variables = self.variables.extractVariables(filter)
    self.ontology_container.writeVariables(variables, self.indices, self.variables.ProMoIRI)
    self.state = 'edit'

    self.compile_only = False

    for l in LANGUAGES["compile"]:  # ["code_generation"]:
      try:
        self.__compile(l)
      except (EditorError) as error:
        self.__writeMessage(error.msg)


    self.__makeRenderedOutput()

  def __makeRenderedOutput(self):
    self.__writeMessage("generating variable and equation pictures")
    language = LANGUAGES["global_ID_to_internal"]
    incidence_dictionary, inv_incidence_dictionary = makeIncidenceDictionaries(self.variables)
    e_name = FILES["coded_equations"] % (self.ontology_location, language)

    for equ_ID in sorted(incidence_dictionary):
      lhs_var_ID, incidence_list = incidence_dictionary[equ_ID]
      expression_ID = self.variables[lhs_var_ID].equations[equ_ID]["rhs"]
      network = self.variables[lhs_var_ID].equations[equ_ID]["network"]
      var_label = self.variables[lhs_var_ID].label
      expression = renderExpressionFromGlobalIDToInternal(expression_ID, self.variables, self.indices)
      self.compiled_equations[language][equ_ID] = {
              "lhs"    : var_label,
              "network": network,
              "rhs"    : expression
              }

    putData(self.compiled_equations[language], e_name)

    e_name = FILES["coded_equations"] % (self.ontology_location, "just_list_internal_format")
    e_name = e_name.replace(".json", ".txt")
    file = open(e_name, 'w')
    for equ_ID in sorted(incidence_dictionary):
      e = self.compiled_equations[language][equ_ID]
      file.write("%s :: %s = %s\n" % (equ_ID, e["lhs"], e["rhs"]))
    file.close()

    # print("debugging --- rendered version", e_name)

  def __compile(self, language):

    incidence_dictionary, inv_incidence_dictionary = makeIncidenceDictionaries(self.variables)
    e_name = FILES["coded_equations"] % (self.ontology_location, language)
    for equ_ID in sorted(incidence_dictionary):
      lhs_var_ID, incidence_list = incidence_dictionary[equ_ID]
      expression_ID = self.variables[lhs_var_ID].equations[equ_ID]["rhs"]
      network = self.variables[lhs_var_ID].equations[equ_ID]["network"]
      var_label = self.variables[lhs_var_ID].label
      expression = renderExpressionFromGlobalIDToInternal(expression_ID, self.variables, self.indices)
      compiler = makeCompiler(self.variables, self.indices, lhs_var_ID, equ_ID, language=language)

      try:
        # print("debugging --  expression being translated into language %s:"%language, expression)
        res = str(compiler(expression))
        self.compiled_equations[language][equ_ID] = {
                "lhs"    : var_label,
                "network": network,
                "rhs"    : res
                }

      except (SemanticError,
              SyntacticError,
              LexicalError,
              WrongToken,
              UnitError,
              IndexStructureError,
              VarError,
              ) as _m:
        print(
                'checked expression failed %s : %s = %s -- %s' % (
                        equ_ID, self.variables[lhs_var_ID].label, expression, _m))

        compiler = makeCompiler(self.variables, self.indices, lhs_var_ID, equ_ID, language=language, verbose=100)
        try:
          res = compiler(expression)  # NOTE: for debugging
        except:
          pass
          os._exit(-1)

    putData(self.compiled_equations[language], e_name)

    for var_ID in self.variables:  # used in internally
      self.variables[var_ID].setLanguage(language)
      compiled_label = str(self.variables[var_ID])
      if var_ID not in self.compiled_variable_labels:
        self.compiled_variable_labels[var_ID] = {}
      self.compiled_variable_labels[var_ID][language] = compiled_label

    if language == "latex":
      self.__makeLatexDocument()

    self.__makeOWLFile()

  def __makeOWLFile(self):

    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    # OWL.tex
    names_names = []

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    body = j2_env.get_template(FILES["OWL_template"]).render(variables=self.variables, ProMo="ProcessModeller_v7_04",
                                                             ontology="flash_03")  # self.networks)
    f_name = FILES["OWL_variables"] % self.ontology_name
    f = open(f_name, 'w')
    f.write(body)
    f.close()

  def __makeLatexDocument(self):

    # latex
    #
    print('=============================================== make latex ================================================')
    language = "latex"
    THIS_DIR = os.path.dirname(os.path.abspath(__file__))

    # main.tex
    names_names = []
    for nw in self.networks + self.interconnection_nws_list + self.intraconnection_nws_list:
      names_names.append(str(nw).replace(CONNECTION_NETWORK_SEPARATOR, '--'))

    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    body = j2_env.get_template(FILES["latex_template_main"]).render(ontology=names_names)  # self.networks)
    f_name = FILES["latex_main"] % self.ontology_name
    f = open(f_name, 'w')
    f.write(body)
    f.close()

    for nw in self.networks + self.interconnection_nws_list + self.intraconnection_nws_list:
      index_dictionary = self.variables.index_definition_network_for_variable_component_class
      j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
      body = j2_env.get_template(FILES["latex_template_variables"]).render(variables=self.variables,
                                                                           compiled_labels=self.compiled_variable_labels,
                                                                           index=index_dictionary[nw])
      name = str(nw).replace(CONNECTION_NETWORK_SEPARATOR, '--')
      f_name = FILES["latex_variables"] % (self.ontology_location, name)
      f = open(f_name, 'w')
      f.write(body)
      f.close()

    eqs = self.__getAllEquationsPerType("latex")
    # print("debugging tex rep")
    for e_type in self.variables.equation_type_list:
      j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
      ID = j2_env.get_template(FILES["latex_template_equations"]). \
        render(equations=eqs[e_type], sequence=sorted(eqs[e_type].keys()))
      f_name = FILES["latex_equations"] % (self.ontology_location, str(e_type))
      f = open(f_name, 'w')
      f.write(ID)
      f.close()

    # self.__makeDotGraphs()

    location = DIRECTORIES["latex_main_location"] % self.ontology_location
    f_name = FILES["latex_shell_var_equ_doc_command_exec"] % self.ontology_location
    documentation_file = FILES["latex_documentation"] % self.ontology_name

    if not self.compile_only:
      saveBackupFile(documentation_file)

    self.__writeMessage("busy making var/eq images")

    args = ['sh', f_name, location]
    print('ARGS: ', args)
    make_it = subprocess.Popen(
            args,
            # start_new_session=True,
            # stdout=subprocess.PIPE,
            # stderr=subprocess.PIPE
            )
    out, error = make_it.communicate()
    print("debugging -- ",out, error)
    # make_it.wait()

    make_variable_equation_pngs(self.ontology_container.variables, self.ontology_name)
    self.__writeMessage("Wrote {} output".format(language), append=True)

  def __getAllEquationsPerType(self, language):
    eqs = {}
    for e_type in self.variables.equation_type_list:  # split into equation types
      eqs[e_type] = OrderedDict()
    for var_ID in self.variables:
      for equ_ID in self.variables[var_ID].equations:
        eq = self.variables[var_ID].equations[equ_ID]
        this_eq_type = eq["type"]  # equation_type
        eqs[this_eq_type][equ_ID] = {}
        eqs[this_eq_type][equ_ID]["rhs"] = self.compiled_equations[language][equ_ID][
          "rhs"]  # [var_ID][equ_ID][language]
        eqs[this_eq_type][equ_ID]["lhs"] = self.compiled_variable_labels[var_ID][language]
        if eq["doc"] == "":
          eq["doc"] = "var doc : %s" % self.variables[var_ID].doc
        eqs[this_eq_type][equ_ID]["doc"] = eq["doc"].replace("_", " ")  # self.variables[ID].doc
        eqs[this_eq_type][equ_ID]["var_ID"] = var_ID
        eqs[this_eq_type][equ_ID]["var_network"] = self.variables[var_ID].network
        eqs[this_eq_type][equ_ID]["network"] = eq["network"]
    return eqs

  def __makeDotGraphs(self):
    # http://www.graphviz.org/doc/info/colors.html

    vt_colour = ['white', 'yellow', 'darkolivegreen1', 'salmon', 'tan',
                 'tomato', 'cyan', 'green', 'grey',
                 'lightcyan', 'lightcyan1', 'lightcyan2',
                 'lightcyan3', 'lightcyan4',
                 ]

    dot_graph = {}
    s_nw_vt = "%s___%s"

    vt_colours = {}
    var_types = set()
    for nw in self.networks:
      [var_types.add(vt)
       for vt in self.ontology_container.variable_types_on_networks[nw]]

    var_types = list(var_types)
    for i in range(len(var_types)):
      vt_colours[var_types[i]] = vt_colour[i]

    for nw in self.networks:
      dot_graph[nw] = GV.Dot(graph_name=nw, label=nw,
                             # suppress_disconnected=True,
                             rankdir='LR')

      vt_cluster = {}
      vt_count = 0
      for vt in self.ontology_container.variable_types_on_networks[nw]:
        vt_cluster[vt] = GV.Cluster(graph_name=s_nw_vt % (nw, vt),
                                    suppress_disconnected=False,
                                    label=vt,
                                    rankdir='LR')
        for v_ID in self.variables.getVariablesForTypeAndNetwork(vt, nw):
          v_name = str(v_ID)
          v_node = GV.Node(name=v_name,
                           style='filled',
                           fillcolor=vt_colours[vt],
                           penwidth=3,
                           fontsize=12,
                           label=self.variables[v_ID].label)
          vt_cluster[vt].add_node(v_node)
        for v_ID, e_ID in self.variables.index_equation_in_definition_network[nw]:
          if self.variables[v_ID].type == vt:
            e_node = GV.Node(name=e_ID,
                             shape='box',
                             style='filled',
                             fillcolor='pink',
                             fontsize=12)
            vt_cluster[vt].add_node(e_node)
            equation = self.variables[v_ID].equations[e_ID]["rhs"]
            for i_ID in makeIncidentList(equation):
              edge = GV.Edge(src=e_ID, dst=i_ID,
                             splines='ortho')
              dot_graph[nw].add_edge(edge)
            v_name = self.variables[v_ID].label
            e_name = str(self.variables[v_ID].equations[e_ID])
            edge = GV.Edge(src=e_ID, dst=v_ID,
                           splines='ortho')
            vt_cluster[vt].add_edge(edge)
        vt_count += 1
        dot_graph[nw].add_subgraph(vt_cluster[vt])
      f_name = FILES["ontology_graphs_ps"] % (self.ontology_location, nw)

      # dot_graph[nw].write_ps(f_name, )  # prog='fdp')
      # f_name2 = DIRECTORIES["ontology_graphs_dot"] % (self.ontology_location, nw)
      # dot_graph[nw].write(f_name2, format='raw')

      try:
        dot_graph[nw].write_ps(f_name, )  # prog='fdp')
        f_name2 = FILES["ontology_graphs_dot"] % (self.ontology_location, nw)
        dot_graph[nw].write(f_name2, format='raw')
      except:
        print("cannot generate dot graph", f_name)

    # print("debugging ferdig med det - no of colours") # %s - %s"%(nw_count, vt_count))

  def update_tables(self):
    variable_type = self.current_variable_type
    print(">>> udating table :", variable_type)
    self.tables["variables"][variable_type].reset_table()
    self.ui_eq.variable_table.reset_table()

  def finished_edit_table(self, what):
    # print("finished editing table : ", what)
    # self.__makeAliasDictionary()  # check if all variables are defined
    self.ui.groupEdit.show()
    self.ui.groupFiles.show()
    self.ui.pushWrite.show()
    try:
      self.table_aliases_i.close()
    except:
      pass
    try:
      self.table_aliases_v.close()
    except:
      pass
    try:
      self.ui_eq.close()
    except:
      pass

  def closeEvent(self, event):
    self.close_children(event)
    self.close()

  def close_children(self, event):
    try:
      self.table_variables.close()
    except:
      pass
    try:
      self.table_aliases_v.close()
    except:
      pass
    try:
      self.table_aliases_i.close()
    except:
      pass
    try:
      self.ui_eq.closeEvent(event)
    except:
      pass

  def __setupVariableTable(self):
    choice=self.current_variable_type
    if self.current_network in self.interconnection_nws:
      network_variable = self.current_network  # self.interconnection_nws[self.current_network]["right"]
      network_expression = network_variable  # self.interconnection_nws[self.current_network]["left"]
    elif self.current_network in self.intraconnection_nws:
      network_variable = self.current_network #self.intraconnection_nws[self.current_network]["right"]
      network_expression = self.current_network #self.intraconnection_nws[self.current_network]["left"]
    else:
      network_variable = self.current_network
      network_expression = self.current_network

    if choice[0] == "*":
      hide = ["port"]
    elif choice not in self.rules["variable_classes_having_port_variables"]:
      hide = ["port"]
    else:
      hide = []

    self.table_variables = UI_VariableTableDialog("create & edit variables",
                                                  self.variables,
                                                  self.indices,
                                                  self.variable_types_on_networks,
                                                  network_variable,
                                                  network_expression,
                                                  choice,
                                                  info_file=FILES["info_ontology_variable_table"],
                                                  hidden=hide,
                                                  )
    self.table_variables.show()  # Note: resolved tooltip settings, did not work during initialisation of table (
    # ui_variabletable_implement)

    for choice in choice:
      try:
        enabled_columns = ENABLED_COLUMNS[self.state][choice]
      except:
        enabled_columns = ENABLED_COLUMNS[self.state]["others"]
      self.table_variables.enable_column_selection(enabled_columns)

    # self.ui_eq.def_given_variable.connect(self.table_variables.defineGivenVariable)
    self.table_variables.completed.connect(self.finished_edit_table)
    self.table_variables.new_variable.connect(self.ui_eq.setupNewVariable)
    self.table_variables.new_equation.connect(self.ui_eq.setupNewEquation)

  def __updateVariableTable(self):
    self.table_variables.close()
    self.__setupVariableTable()
    self.table_variables.show()

  def __setupVariablesAliasTable(self):

    # variables = self.variables.getVariableList(self.current_network)
    variables_ID_list = self.variables.index_definition_networks_for_variable[self.current_network]
    if variables_ID_list:
      self.table_aliases_v = UI_AliasTableVariables(self.variables,
                                                    self.current_network)  # , self.aliases_v[self.current_network])
      # self.table_aliases_v.completed.connect(self.__updateAliases_Variables)
      self.table_aliases_v.completed.connect(self.finished_edit_table)
      self.table_aliases_v.show()
      OK = True
    else:
      self.__writeMessage(" no variables in this network %s" % self.current_network)
      # self.table_aliases_v.hide()
      OK = False
    return OK

  def __setupIndicesAliasTable(self):
    # print("gotten here")
    self.table_aliases_i = UI_AliasTableIndices(self.indices)  # , self.aliases_i)
    self.table_aliases_i.completed.connect(self.__updateAliases_Indices)
    self.table_aliases_i.completed.connect(self.finished_edit_table)
    self.table_aliases_i.show()

  def __writeMessage(self, message, append=False):
    if not append:
      self.ui.msgWindow.clear()
    self.ui.msgWindow.setText(message)
    self.show()
    self.ui.msgWindow.show()
    self.ui.msgWindow.update()

  def __updateAliases_Variables(self):
    pass

  def __updateAliases_Indices(self):
    pass
    # self.ontology_container.indices = self.indices

  def __checkRadios(self, active):

    radios_ui = [self.ui.radioVariables, self.ui.radioVariablesAliases,
                 self.ui.radioIndicesAliases]
    radios = ["variables", "variable_aliases", "indices_aliase"]
    which = radios.index(active)
    for ui in radios_ui:
      ui.setChecked(False)
    radios_ui[which].setChecked(True)
