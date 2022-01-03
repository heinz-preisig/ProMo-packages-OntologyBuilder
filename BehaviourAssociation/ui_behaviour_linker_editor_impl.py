from copy import deepcopy
from os.path import abspath
from os.path import dirname
from os.path import join

from PyQt5 import QtCore
from PyQt5 import QtGui
from PyQt5 import QtWidgets
from PyQt5.Qt import QStandardItem
from jinja2 import Environment  # sudo apt-get install python-jinja2
from jinja2 import FileSystemLoader

from Common.common_resources import TEMPLATE_ENTITY_OBJECT
from Common.common_resources import getData
from Common.common_resources import getOntologyName
from Common.common_resources import indexList
from Common.common_resources import invertDict
from Common.common_resources import putData
from Common.common_resources import walkDepthFirstFnc
from Common.ontology_container import OntologyContainer
from Common.record_definitions_equation_linking import EntityBehaviour
from Common.record_definitions_equation_linking import NodeArcAssociations
from Common.record_definitions_equation_linking import VariantRecord
from Common.record_definitions_equation_linking import functionGetObjectsFromObjectStringID
from Common.record_definitions_equation_linking import functionMakeObjectStringID
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.resource_initialisation import checkAndFixResources
from Common.resources_icons import roundButton
from Common.ui_match_pairs_impl import UI_MatchPairs
from Common.ui_string_dialog_impl import UI_String
from Common.ui_two_list_selector_dialog_impl import UI_TwoListSelector
from OntologyBuilder.BehaviourAssociation.ui_behaviour_linker_editor import Ui_MainWindow
from OntologyBuilder.OntologyEquationEditor.resources import AnalyseBiPartiteGraph
from OntologyBuilder.OntologyEquationEditor.resources import isVariableInExpression
from OntologyBuilder.OntologyEquationEditor.resources import renderExpressionFromGlobalIDToInternal

# RULE : what variable class in what network for nodes and arcs
# TODO: integrate into base ontology editor

rules = {
        "nodes": {
                "physical": ["state", "diffState"],
                "control" : ["state", "diffState"],
                "intra"   : ["state", "diffState"],
                "inter"   : ["transform"],
                },
        "arcs" : {
                "physical": ["transport"],
                "control" : ["dataflow"],
                "inter"   : ["transform"]
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

  def __init__(self, radio_class, receiver, label_list, layout, mode="text", autoexclusive=True):
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

  def __radioAutoExclusive(self):
    for ID in self.radios:
      self.radios[ID].setAutoExclusive(self.autoexclusive)

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
      # self.radios[ID] = QtWidgets.QRadioButton(label)
      self.radios[ID] = QtWidgets.QCheckBox(label)
      # if self.autoexclusive:
      #   self.radios[ID].setAutoExclusive(True)
      # self.radios[ID].setAutoExclusive(self.autoexclusive)
      self.layout.addWidget(self.radios[ID])
      self.__radioAutoExclusive()
      self.radios[ID].toggled.connect(self.selector_toggled)

  def makePixelSelector(self):

    for ID in self.label_indices:
      icon, label, size = self.labels[ID]
      label = QtWidgets.QLabel()
      self.radios[ID] = QtWidgets.QRadioButton(label)
      self.radios[ID].setIcon(icon)
      self.radios[ID].setIconSize(size)
      self.radios[ID].resize(0, 0)  # Note: not sure what I am doing here -- reduces gaps between

      # if self.autoexclusive:
      #   self.radios[ID].setAutoExclusive(False)
      self.__radioAutoExclusive()
      self.layout.addWidget(self.radios[ID])

      self.radios[ID].toggled.connect(self.selector_toggled)

  def showList(self, show):
    self.show_list = show
    self.showIt()
    # self.resetChecked()

  def showIt(self):
    for ID in self.radios:
      self.radios[ID].setAutoExclusive(False)
      self.radios[ID].setChecked(False)
      if ID not in self.show_list:
        self.radios[ID].hide()
      else:
        self.radios[ID].show()
    self.__radioAutoExclusive()

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
        self.radios[ID].setCheckState(False)

    self.selected_ID = ID

    return ID

  def resetChecked(self):
    for ID in self.radios:
      self.radios[ID].setDown(False)


class MainWindowImpl(QtWidgets.QMainWindow):
  def __init__(self, icon_f):

    super().__init__()
    self.ui = Ui_MainWindow()
    self.ui.setupUi(self)

    roundButton(self.ui.pushButtonInformation, "info", tooltip="information")
    roundButton(self.ui.pushButtonSave, "save", tooltip="save entity behaviour")
    roundButton(self.ui.pushButtonCancel, "exit", tooltip="cancel and exit")
    roundButton(self.ui.pushButtonDelete, "delete", tooltip="delete current var/eq tree")

    self.ui.groupBoxControls.hide()
    self.ui.pushButtonLeft.hide()
    self.ui.pushButtonRight.hide()

    # first get ontology
    self.ontology_name = getOntologyName(task=icon_f)

    # check for infrastructure
    checkAndFixResources(self.ontology_name, stage="ontology_stage_2")

    # attach ontology
    self.ontology_container = OntologyContainer(self.ontology_name)
    self.location = DIRECTORIES["latex_doc_location"] % self.ontology_name

    self.ontology_location = DIRECTORIES["ontology_location"] % str(self.ontology_name)

    self.reduced_network_node_list = self.ontology_container.list_reduced_network_node_objects
    self.reduced_arc_list = self.ontology_container.list_reduced_network_arc_objects

    # instantiate entity behaviours
    networks = self.ontology_container.list_inter_branches
    # entities_list = self.reduced_network_node_list

    self.arc_objects = self.ontology_container.list_arc_objects_on_networks
    self.node_objects = self.ontology_container.list_inter_node_objects_tokens  # list_node_objects_on_networks_with_tokens
    entities_list = []
    for nw in self.node_objects:
      for o in self.node_objects[nw]:
        obj = TEMPLATE_ENTITY_OBJECT % (nw, "node", o, "base")
        entities_list.append(obj)
    for nw in self.arc_objects:
      for o in self.arc_objects[nw]:
        obj = TEMPLATE_ENTITY_OBJECT % (nw, "arc", o, "base")  # RULE: "base" is used for the base bipartite graph
        entities_list.append(obj)

    self.entity_behaviours = EntityBehaviour(entities_list)

    self.node_arc_associations = NodeArcAssociations(networks, self.node_objects, self.arc_objects)
    # self.entity_behaviour_graphs = EntityBehaviourGraphs(networks, entities_list)

    equations_label_list, \
    self.equation_information, \
    self.equation_inverse_index = self.__makeEquationAndIndexLists()
    # self.variable_equation_list = self.__makeEquationList_per_variable_type(networks)
    self.rules = {}

    # get existing data
    self.__readVariableAssignmentToEntity()

    # f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    # self.node_arc_associations, self.entity_behaviours = readVariableAssignmentToEntity(f)

    # interface components
    self.layout_InterNetworks = QtWidgets.QVBoxLayout()  # Vertical Box with horizontal boxes of radio buttons & labels
    self.ui.scrollAreaWidgetContentsInterNetworks.setLayout(self.layout_InterNetworks)

    # initialisations
    # network selector
    self.radio_InterNetworks = Selector("InterNetworks",
                                        self.radioReceiverState,
                                        networks,
                                        self.layout_InterNetworks)

    self.selected_InterNetwork_ID = None
    self.selected_Entity_ID = None
    self.selected_variant_ID = None
    self.selected_variant_str_ID = "base"
    self.radio_index = None
    self.selected_base_variable = None
    self.rightListEquationIDs = []
    self.rightListEquationIDs_radio_ID = []

    self.match_equations_label_list = []
    self.match_equation_ID = {}
    self.node_arc = "nodes"

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
    self.selected_variant = None
    self.state = "start"

  def __readVariableAssignmentToEntity(self):
    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    # loaded_entity_behaviours = getData(f)
    data = getData(f)
    if data:
      loaded_entity_behaviours = data["behaviours"]
      self.node_arc_associations = data["associations"]

      if loaded_entity_behaviours:
        for entity_str_ID in loaded_entity_behaviours:  # careful there may not be all entities at least during
          # developments
          if loaded_entity_behaviours[entity_str_ID]:
            dummy = VariantRecord()
            data = loaded_entity_behaviours[entity_str_ID]
            for atr in dummy:
              if atr not in data:
                data[atr] = None
            tree = {}
            for treeStrID in data["tree"]:
              tree[int(treeStrID)] = data["tree"][treeStrID]
            data["tree"] = tree

            nodes = {}
            for nodeStrID in data["nodes"]:
              nodes[int(nodeStrID)] = data["nodes"][nodeStrID]
            data["nodes"] = nodes

            self.entity_behaviours[entity_str_ID] = VariantRecord(tree=data["tree"],
                                                                  nodes=data["nodes"],
                                                                  IDs=data["IDs"],
                                                                  root_variable=data["root_variable"],
                                                                  blocked_list=data["blocked"],
                                                                  buddies_list=data["buddies"],
                                                                  to_be_inisialised=data["to_be_initialised"])

  def getObjectSpecificationState(self):
    state = -1
    if self.radio_InterNetworks.selected_ID != None:
      state += 1
      if self.radio_Entities.selected_ID != None:
        state += 1
        if self.radio_Variants.selected_ID != None:
          state += 1
    return state

  def isCompleteSpecificationState(self):
    return self.getObjectSpecificationState() == 2

  def superviseControls(self):
    if self.isCompleteSpecificationState():
      self.ui.groupBoxControls.show()

  def __makeObjectList(self):

    if self.node_arc == "nodes":
      ui = self.ui.listNodeObjects
      n = sorted(self.node_objects[self.selected_InterNetwork_strID])
    else:
      ui = self.ui.listArcObjects
      n = sorted(self.arc_objects[self.selected_InterNetwork_strID])
    ui.clear()
    ui.addItems(n)

  def on_tabWidgetNodesArcs_currentChanged(self, index):
    print("debugging tab", index)
    if not self.selected_InterNetwork_ID:
      return

    if index == 0:
      self.node_arc = "nodes"
    else:
      self.node_arc = "arcs"
    self.__makeObjectList()

  def on_listNodeObjects_itemClicked(self, v):
    print('item clicked', v.text())
    # selected_InterNetwork_strID self.node_arc v.text()
    # entity_behaviours
    self.selected_object = v.text()
    self.ui.pushButtonLeft.setText('')
    self.ui.pushButtonLeft.hide()
    self.ui.groupBoxControls.hide()
    self.ui.listLeft.clear()
    self.ui.listRight.clear()
    self.ui.listVariants.clear()
    obj_str = self.__makeCurrentObjectString()
    if not self.entity_behaviours[obj_str]: #self.node_arc_associations[self.selected_InterNetwork_strID]["nodes"][v.text()]:
      # self.selected_object = v.text()
      self.__makeBase()
    else:
      print("load")
      self.__makeVariantList(True)

  def on_listArcObjects_itemClicked(self, v):
    print('item clicked', v.text())
    self.selected_object = v.text()
    obj_str = self.__makeCurrentObjectString()
    if not self.entity_behaviours[obj_str]:
    # if self.node_arc_associations[self.selected_InterNetwork_strID]["arcs"]:
      self.selected_object = v.text()
      self.__makeBase()
    else:
      print("load")

  def on_listLeft_itemClicked(self, v):
    row = self.ui.listLeft.row(v)
    print('item clicked', v.text(), row)
    var_strID, equ_strID = self.leftIndex[row]
    equation_label = v.text()
    if self.state == "make_base":
      self.current_base_var_ID = int(var_strID)
      self.__makeEquationTextButton(equation_label, self.ui.pushButtonLeft, "click to accept")
    else:  # self.state == "duplicates":
      var_ID, eq_ID = self.leftIndex[row]
      self.leftListEquationIDs.remove(eq_ID)
      self.rightListEquationIDs.append(eq_ID)
      # print("debugging -- duplicates", self.leftListEquationIDs)
      # print("debugging -- blocked", self.rightListEquationIDs)
      self.leftIndex = self.__makeLeftRightList(self.leftListEquationIDs, self.ui.listLeft)
      self.rightIndex = self.__makeLeftRightList(self.rightListEquationIDs, self.ui.listRight)
      self.__makeEquationTextButton("accept", self.ui.pushButtonLeft, "click to accept")
      print("debugging")

  def on_listRight_itemClicked(self, v):
    row = self.ui.listRight.row(v)
    print("right item clicked", v.text(), row)
    # if self.state == "duplicates":
    var_ID, eq_ID = self.rightIndex[row]
    self.leftListEquationIDs.append(eq_ID)
    self.rightListEquationIDs.remove(eq_ID)
    # print("debugging -- duplicates", self.leftListEquationIDs)
    # print("debugging -- blocked", self.rightListEquationIDs)
    self.leftIndex = self.__makeLeftRightList(self.leftListEquationIDs, self.ui.listLeft)
    self.rightIndex = self.__makeLeftRightList(self.rightListEquationIDs, self.ui.listRight)

  def showVariant(self):
    self.state = "show"

  def radioReceiverState(self, radio_class, ID):
    print("debugging -- receiver state %s" % radio_class, ID)
    # self.superviseControls()

    if radio_class == "InterNetworks":
      self.selected_InterNetwork_ID = ID
      self.selected_InterNetwork_strID = self.radio_InterNetworks.getStrID()
      self.__makeObjectList()

      #
      # updating interface
      # self.radio_Variants.reset()
      # self.radio_Left.reset()
      # self.radio_Right.reset()
      self.ui.pushButtonLeft.hide()
      self.ui.pushButtonRight.hide()
      self.ui.listLeft.clear()
      self.ui.listRight.clear()



  def on_pushButtonLeft_pressed(self):
    # if self.ui.radioButtonShowVariant.isChecked():
    #   self.state = "show"

    print("debugging -- push left button state:", self.state)

    # nw_str_ID = self.radio_InterNetworks.getStrID()
    # entity_label_ID = self.radio_Entities.getStrID()
    entity_label_ID = self.selected_object

    if self.state == "make_base":
      variant = "base"
      var_ID = self.current_base_var_ID
      obj_str = self.__makeCurrentObjectString()
      # name = obj_str.replace(", ","-")#.replace("|","_")
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(obj_str, var_ID, [])
      self.status_report("generated graph for %s" % (obj_str))
      component = self.node_arc.strip("s")
      self.selected_variant_str_ID = "base"
      obj = self.__makeCurrentObjectString()
      self.entity_behaviours.addVariant(obj, entity_assignments)
      self.__makeVariantList(True)

      graph_file = var_equ_tree_graph.render()
      self.selected_variant_str_ID = variant
      self.ui.pushButtonLeft.hide()
      self.ui.groupBoxControls.show()
      self.ui.listLeft.clear()
      self.__makeAndDisplayEquationListLeftAndRight()
      self.ui.groupBoxControls.show()
      # self.ui.radioButtonShowVariant.setDown(True)#setChecked(True)

    elif self.state in ["duplicates", "new_variant", "edit_variant"]:  # accepting
      print("debugging -- accepting >>> %s <<< reduced entity object" % self.state)

      var_ID = self.selected_base_variable
      obj_str = self.__makeCurrentObjectString()
      # name = obj_str.replace(", ","-")#.replace("|","_")      #

      self.variant_list = self.__makeVariantStringList()
      if self.state in ["duplicates", "new_variant"]:
        self.selected_variant_str_ID = self.__askForNewVariantName(self.variant_list)
        if self.state == "duplicates":
          # name = TEMPLATE_ENTITY_OBJECT_REMOVED_DUPLICATES % name
          # self.selected_variant_str_ID = TEMPLATE_ENTITY_OBJECT_REMOVED_DUPLICATES % self.selected_variant_str_ID
          selectedListEquationIDs = self.entity_behaviours.getEquationIDList(obj_str)
          # this is tricky: the right list may include already blocked ones.
          for e in self.rightListEquationIDs:
            if e in selectedListEquationIDs:
              selectedListEquationIDs.remove(e)
            # [ selectedListEquationIDs.remove(i) for i in self.rightListEquationIDs]
          self.leftListEquationIDs = selectedListEquationIDs
      var_equ_tree_graph, entity_assignments = self.analyseBiPartiteGraph(obj_str, var_ID, self.rightListEquationIDs)
      graph_file = var_equ_tree_graph.render()
      self.status_report("generated graph for %s " % (obj_str))

      obj = self.__makeCurrentObjectString()  # TEMPLATE_ENTITY_OBJECT % (self.selected_InterNetwork_strID, component, self.selected_object, "base")
      self.entity_behaviours.addVariant(obj, entity_assignments)
      self.__makeVariantList(True)
      # self.ui.radioButtonShowVariant.setChecked(True)

    elif self.state == "show":
      print("debugging -- show don't do anything")

  def __makeVariantList(self, set):
    """
    gets the current variant list and builds the gui list
    """
    self.variant_list = self.__makeVariantStringList()
    self.ui.listVariants.clear()
    self.ui.listVariants.addItems(self.variant_list)
    if set:
      row = self.variant_list.index(self.selected_variant_str_ID)
      self.ui.listVariants.setCurrentRow(row)
      return True
    else:
      self.selected_variant_str_ID = "base"
      return False

  # push buttons
  def on_pushButtonRight_pressed(self):
    # print("debugging -- push right button")
    pass

  def on_listVariants_currentRowChanged(self, row):
    if self.variant_list:
      self.selected_variant_str_ID = self.variant_list[row]
      self.__makeAndDisplayEquationListLeftAndRight()
      self.ui.groupBoxControls.show()
      self.ui.radioButtonShowVariant.setChecked(True)
    else:
      self.ui.listLeft.clear()
      self.ui.listRight.clear()
      self.ui.radioButtonShowVariant.setChecked(False)
    print("debugg -- current variant", self.selected_variant_str_ID)


  def on_pushButtonDelete_pressed(self):
    obj = self.__makeCurrentObjectString()
    self.entity_behaviours.removeVariant(obj)  # nw_str_ID, entity_label_ID, variant)
    deleted_base = self.__makeVariantList(False)
    self.ui.listLeft.clear()
    # self.ui.radioButtonShowVariant.setChecked(True)
    if deleted_base:
      self.current_base_var_ID = "base"
      # self.on_radioButtonShowVariant_pressed()
    self.ui.pushButtonLeft.hide()

  def on_pushButtonSave_pressed(self):
    # print("debugging -- save file")
    # self.ontology_container.writeVariables()

    f = FILES["variable_assignment_to_entity_object"] % self.ontology_name
    for obj in self.entity_behaviours:
      if self.entity_behaviours[obj]:
        self.__makeVariablesToBeValueInitialised(obj)
    data = {"behaviours"  : self.entity_behaviours,
            "associations": self.node_arc_associations}

    # putData(self.entity_behaviours, f)
    putData(data, f)

  def on_pushButtonInformation_pressed(self):
    print("todo: not yet implemented")

  def on_radioButtonShowVariant_pressed(self):
    # print("debugging -- show variant")
    if not self.variant_list:
      return

    position = self.ui.radioButtonShowVariant.isChecked()
    print("debugging -- show variant -- toggle state:", position)

    if position:
      self.state = "show"
      self.__makeAndDisplayEquationListLeftAndRight()
    else:
      self.ui.listLeft.clear()

  def on_radioButtonDuplicates_pressed(self):
    print("debugging -- duplicates")
    if not self.variant_list:
      return

    self.state = "duplicates"

    entity_object_str = self.__makeCurrentObjectString()
    self.selected_base_variable = self.entity_behaviours[entity_object_str]["root_variable"]
    self.leftListEquationIDs = self.__makeDuplicateShows()
    self.leftIndex = self.__makeLeftRightList(self.leftListEquationIDs, self.ui.listLeft)
    self.ui.pushButtonLeft.hide()

  def on_radioButtonNewVariant_pressed(self):
    if not self.variant_list:
      return

    self.state = "new_variant"
    self.__makeAndDisplayEquationListLeftAndRight()  # self.selected_variant_str_ID)

  def on_radioButtonEditVariant_pressed(self):

    if not self.variant_list:
      return

    print("debugging -- edit variant")
    self.state = "edit_variant"
    self.__makeAndDisplayEquationListLeftAndRight()

  def on_radioButtonInstantiateVariant_pressed(self):

    if not self.variant_list:
      return

    print("debugging -- instantiate variant")

    entity_object_str = self.__makeEntityObjectStrID()
    self.__makeVariablesToBeValueInitialised(entity_object_str)

  def on_pushButtonNodeAssociations_pressed(self):
    print("debugging -- token topologies network %s" % self.selected_InterNetwork_ID)
    if not self.selected_InterNetwork_ID:
      self.status_report("define network first")
      return

    self.state = "token_topologies"
    nw = self.radio_InterNetworks.getStrID()
    # node_objects = self.ontology_container.list_node_objects_on_networks_with_tokens[nw]
    node_objects = sorted(self.node_arc_associations[nw]["nodes"].keys())

    self.match_equations_label_list = []
    self.match_node_equation_inverse = {}
    for ID in range(0, len(self.equation_inverse_index)):
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[ID]
      if var_type == "state":
        self.match_equations_label_list.append(equation_label)
        self.match_node_equation_inverse[equation_label] = eq_ID, var_ID

    selector = UI_MatchPairs(node_objects, self.match_equations_label_list, self.matchNodeReceiver, take_right=False)
    self.update()
    gugus = selector.exec_()

  def on_pushButtonArcAssociations_pressed(self):
    print("debugging -- token topologies network %s" % self.selected_InterNetwork_ID)
    if not self.selected_InterNetwork_ID:
      self.status_report("define network first")
      return

    self.state = "token_topologies"
    nw = self.radio_InterNetworks.getStrID()
    # arc_objects = self.ontology_container.list_arc_objects_on_networks[nw]
    arc_objects = sorted(self.node_arc_associations[nw]["arcs"].keys())
    self.match_equations_label_list = []
    self.match_arc_equation_inverse = {}
    for ID in range(0, len(self.equation_inverse_index)):
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[ID]
      if var_type == "transport":
        self.match_equations_label_list.append(equation_label)
        self.match_arc_equation_inverse[equation_label] = eq_ID, var_ID

    selector = UI_MatchPairs(arc_objects, self.match_equations_label_list, self.matchArcReceiver, take_right=False)
    self.update()
    gugus = selector.exec_()

  def matchNodeReceiver(self, selection):
    print("match receiver -- selection", selection)
    nw_str_ID = self.radio_InterNetworks.getStrID()
    for node_object, equation in selection:
      print("object : %s  \n equation : %s" % (node_object, equation))
      eq_ID, var_ID = self.match_node_equation_inverse[equation]
      self.node_arc_associations[nw_str_ID]["nodes"][node_object] = (eq_ID, var_ID)
    print("debugging -- wait")

  def matchArcReceiver(self, selection):
    print("match receiver -- selection", selection)
    nw_str_ID = self.radio_InterNetworks.getStrID()
    for arc_object, equation in selection:
      print("object : %s  \n equation : %s" % (arc_object, equation))
      eq_ID, var_ID = self.match_arc_equation_inverse[equation]
      self.node_arc_associations[nw_str_ID]["arcs"][arc_object] = (eq_ID, var_ID)
    print("debugging -- wait")

  def __makeVariablesToBeValueInitialised(self, entity_object_str):
    # find the ID for the "value" variable
    numerical_value = self.ontology_container.rules["numerical_value"]
    var_ID_value = -1
    variables = self.ontology_container.variables
    for var_ID in variables:
      if variables[var_ID]["label"] == numerical_value:
        var_ID_value = var_ID
        break
    if var_ID_value == -1:
      print("did not fine variable for numerical value")
    # find all those expressions that ask for a value
    # print("debugging -- ", dir(self.entity_behaviours[entity_object_str]))
    behaviour = self.entity_behaviours[entity_object_str]
    tree = behaviour["tree"]
    a = walkDepthFirstFnc(tree, 0)
    to_be_initialised = set()
    for ID in a:
      _ID = behaviour["nodes"][ID]
      lbl, varStrID = _ID.split("_")
      if lbl != "equation":
        varID = int(varStrID)

        var = self.ontology_container.variables[varID]
        equations = var["equations"]
        for e in equations:
          eq = equations[e]["rhs"]
          if isVariableInExpression(eq, var_ID_value):
            print("debugging -- variable ", var["label"], eq)
            to_be_initialised.add(varID)

    self.entity_behaviours[entity_object_str]["to_be_initialised"] = sorted(to_be_initialised)
    print("debugging -- to be initialised", sorted(to_be_initialised))

  # =============================

  def analyseBiPartiteGraph(self, entity, var_ID, blocked):
    obj = entity  # entity.replace("|", "_")
    var_equ_tree_graph, assignments = AnalyseBiPartiteGraph(var_ID,
                                                            self.ontology_container,
                                                            self.ontology_name,
                                                            blocked,
                                                            obj)
    # self.__makeLatexDoc(var_equ_tree_graph, assignments)
    return var_equ_tree_graph, assignments

  def __makeLatexDoc(self, var_eq_tree_graph, assignments):

    latex_equation_file = FILES["coded_equations"] % (self.ontology_location, "latex")
    latex_equations = getData(latex_equation_file)
    variables = self.ontology_container.variables
    nodes = assignments["nodes"]
    latex_var_equ = []
    count = 0
    for a in nodes:
      if "variable" in nodes[a]:
        print("debugging -- found variable:", nodes[a])
        # v, var_str_ID = nodes[a].split("_")
      elif "equation" in nodes[a]:
        print("debugging -- found equation:", nodes[a])
        e, eq_str_ID = nodes[a].split("_")
        var_ID = latex_equations[eq_str_ID]["variable_ID"]
        s = [count, str(var_ID), eq_str_ID, latex_equations[eq_str_ID]["lhs"], latex_equations[eq_str_ID]["rhs"],
             str(variables[var_ID]["tokens"])]
        latex_var_equ.append(s)
        count += 1
      else:
        pass
    print("debugging -- got here")

    nw = self.radio_InterNetworks.getStrID()
    variant = self.radio_Variants.getStrID()
    entity = self.radio_Entities.getStrID().replace("|", "_")
    name = nw + "-" + entity + "-" + variant

    THIS_DIR = dirname(abspath(__file__))
    j2_env = Environment(loader=FileSystemLoader(THIS_DIR), trim_blocks=True)
    template = FILES["latex_template_equation_list"]
    body = j2_env.get_template(template).render(equations=latex_var_equ)
    f_name = FILES["latex_equation_list"] % (self.ontology_name, name)
    f = open(f_name, 'w')
    f.write(body)
    f.close()

  def __askForNewVariantName(self, limiting_list):
    dialoge = UI_String("Provide a new variant name", placeholdertext="variant", limiting_list=limiting_list)
    dialoge.exec_()
    variant = dialoge.getText()
    del dialoge
    return variant

  def __makeCurrentObjectString(self):
    component = self.node_arc.strip("s")
    object_string = TEMPLATE_ENTITY_OBJECT % (
    self.selected_InterNetwork_strID, component, self.selected_object, self.selected_variant_str_ID)
    if object_string not in self.entity_behaviours:
      self.entity_behaviours[object_string]= None
    return object_string

  def __makeAndDisplayEquationListLeftAndRight(self):
    entity_str_ID = self.__makeCurrentObjectString()

    if self.state == "new_variant":
      print("debugging -- new variant, entity string", entity_str_ID)
      if "base" in entity_str_ID:
        print("debugging -- found D-D", entity_str_ID)

    self.selected_base_variable = self.entity_behaviours.getRootVariableID(entity_str_ID)
    if not self.selected_base_variable:
      return
    equation_ID_list = self.entity_behaviours.getEquationIDList(entity_str_ID)
    blocked_ = self.entity_behaviours.getBlocked(entity_str_ID)  # ok that is a copy
    blocked = deepcopy(blocked_)
    root_equation = equation_ID_list.pop(0)

    root_eq_ID = self.equation_inverse_index[root_equation]  # RULE: single equation
    eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[root_eq_ID]

    self.__makeEquationTextButton(equation_label, self.ui.pushButtonLeft, "click to accept")

    print("debugging -- left list showing ", equation_ID_list[0:5])

    equation_ID_set = set()
    [equation_ID_set.add(e) for e in equation_ID_list]
    block_set = set()
    [block_set.add(e) for e in blocked]
    left_eqs = list(equation_ID_set - block_set)
    self.leftListEquationIDs = left_eqs

    self.leftIndex = self.__makeLeftRightList(left_eqs, self.ui.listLeft)
    self.rightIndex = self.__makeLeftRightList(blocked, self.ui.listRight)

    self.rightListEquationIDs = deepcopy(blocked)

  def __makeLeftRightList(self, eq_list, ui):
    label_list = []
    index = {}
    count = 0
    for id in eq_list:
      e_ID = self.equation_inverse_index[id]
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[e_ID]
      # label = "%s>%s>   %s" % (var_ID, eq_ID, equation_label)
      index[count] = (var_ID, eq_ID)
      count += 1
      label_list.append(equation_label)
    ui.clear()
    ui.addItems(label_list)
    return index

  # def __makeEquationLists(self):
  #   component=self.node_arc.strip("s")
  #   object = TEMPLATE_ENTITY_OBJECT%(self.selected_InterNetwork_strID,component, self.selected_object, self.selected_variant_str_ID) #network, node|arc, object, variant
  #   entity_data = self.entity_behaviours[object]
  #   print("debugging")

  def __makeEntityObjectStrID(self):
    nw_str_ID = self.radio_InterNetworks.label_indices[self.selected_InterNetwork_ID]
    entity_label_ID = self.radio_Entities.label_indices[self.selected_Entity_ID]
    variant = self.radio_Variants.getStrID()  # label_indices[self.radio_Variants.getStrID()] #selected_variant_ID]
    entity_object_str = functionMakeObjectStringID(nw_str_ID, entity_label_ID, variant)
    return entity_object_str

  # def __makeRadioShowList(self, show):
  #   radio_show_list = []
  #   # print("debugging -- halting point")
  #   for i in self.equation_information:
  #     eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[i]
  #     if eq_ID in show:
  #       radio_show_list.append(i)
  #
  #   return radio_show_list

  def __makeRightSelector(self):
    show = self.rightListEquationIDs
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
    entity_object_str = self.__makeCurrentObjectString()

    nodes = self.entity_behaviours[entity_object_str]["nodes"]
    blocked = self.entity_behaviours[entity_object_str]["blocked"]
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
    for eq_ID in blocked:
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
    # self.ui.groupBoxControls.hide()


    print("debugging -- define base")
    self.ui.pushButtonLeft.setText('')
    self.ui.pushButtonLeft.hide()
    self.ui.groupBoxControls.hide()

    self.state = "make_base"
    nw = self.selected_InterNetwork_strID
    rules_selector = UI_TwoListSelector()
    rules_selector.setWindowTitle("chose a list of variable classes")
    rules_selector.setToolTip("we show only those variable types that have equations")
    # Rule: this is being tightened now one can only choose variable types that have equations
    self.rules[nw] = self.ontology_container.variable_types_on_networks[nw]
    variable_equation_list, variable_types_having_equations = self.__makeEquationList_per_variable_type()

    selection = []
    while selection == []:
      rules_selector.populateLists(variable_types_having_equations, []) #self.ontology_container.variable_types_on_networks[nw], [])
      rules_selector.exec_()
      selection = rules_selector.getSelected()
    self.rules[nw] = rules_selector.getSelected()

    self.variable_equation_list,variable_types_having_equations = self.__makeEquationList_per_variable_type()

    left_equations = self.variable_equation_list[self.selected_InterNetwork_strID][self.node_arc] #  self.variable_equation_list[self.selected_InterNetwork_strID][self.node_arc]
    self.leftIndex = self.__makeLeftRightList(left_equations, self.ui.listLeft)
    self.status_report("making base for %s" % self.selected_Entity_ID)
    self.selected_variant = None


    # self.superviseControls()
  #
  # def __makeEquationList_per_variable_type(self, networks):
  #
  #   variable_equation_list = {}
  #   for nw in networks:
  #     variable_equation_list[nw] = {}
  #     for component in rules:
  #       variable_equation_list[nw][component] = []
  #
  #   for nw in networks:
  #     for e in self.equation_information:
  #       eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[e]
  #
  #       # (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation) = self.equations[eq_ID]
  #
  #       if nw in self.ontology_container.networks:
  #         nws = list(self.ontology_container.ontology_tree[nw]["parents"])
  #         nws.append(nw)
  #         for component in rules:
  #           selected_var_types = []
  #           for p_nw in nws:
  #             if p_nw in rules[component]:
  #               selected_var_types = rules[component][p_nw]
  #           for p_nw in nws:
  #             for selected_var_type in selected_var_types:
  #               if p_nw == nw_eq and selected_var_type in var_type:
  #                 # label = "%s>%s>   %s"%(var_ID, eq_ID, equation_label)
  #                 variable_equation_list[nw][component].append(eq_ID)  # (var_ID, eq_ID, equation_label))
  #
  #   return variable_equation_list


  def __makeEquationList_per_variable_type(self):

    variable_equation_list = {}
    nw = self.selected_InterNetwork_strID
    variable_types_having_equations = set()

    for e in self.equation_information:
      eq_ID, var_ID, var_type, nw_eq, equation_label = self.equation_information[e]

      # (var_ID, var_type, nw_eq, rendered_equation, pixelled_equation) = self.equations[eq_ID]

      nws = list(self.ontology_container.ontology_tree[nw]["parents"])
      nws.append(nw)

      for i_nw in nws:
        if nw not in variable_equation_list:
          variable_equation_list[nw] = {}
          variable_equation_list[nw]["nodes"] = []
          variable_equation_list[nw]["arcs"] = []

        for i_var_type in self.rules[self.selected_InterNetwork_strID]:
          if i_nw == nw_eq and i_var_type in var_type:
            variable_equation_list[nw][self.node_arc].append(eq_ID)
            variable_types_having_equations.add(var_type)

    return variable_equation_list, variable_types_having_equations

  def __makeVariantStringList(self):

    nw_str_ID = self.selected_InterNetwork_strID
    current_component = self.node_arc.strip("s")
    object = self.selected_object
    entity_str_IDs = sorted(self.entity_behaviours)
    variants = set()
    for o in entity_str_IDs:
      network, component, entity, variant = functionGetObjectsFromObjectStringID(o)
      if network == nw_str_ID and current_component == component and entity == object:
        if self.entity_behaviours[o]:
          variants.add(variant)
    #
    # self.ui.listVariants.clear()
    # self.ui.listVariants.addItems(list(variants))
    return sorted(variants)

  def __makeVariantRadioIDList(self):

    variant_list = self.entity_behaviours.getVariantList(self.selected_InterNetwork_strID, self.selected_object)
    self.ui.listVariants.clear()
    self.ui.listVariants.addItems(variant_list)

    return

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
