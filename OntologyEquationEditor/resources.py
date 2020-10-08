"""
===============================================================================
 Resources for the equation editor
===============================================================================


"""

__project__ = "ProcessModeller  Suite"
__author__ = "PREISIG, Heinz A"
__copyright__ = "Copyright 2015, PREISIG, Heinz A"
__since__ = "2012. 03. 221"
__license__ = "GPL planned -- until further notice for Bio4Fuel & MarketPlace internal use only"
__version__ = "6.00"
__email__ = "heinz.preisig@chemeng.ntnu.no"
__status__ = "beta"

import os
import subprocess

from graphviz import Digraph
from PyQt5 import QtCore
from PyQt5 import QtGui

from Common.common_resources import invertDict
from Common.resource_initialisation import DIRECTORIES
from Common.resource_initialisation import FILES
from Common.treeid import ObjectTree

# INDENT = "    "
# LF = "\n"
NEW = "_new_"
NEW_EQ = NEW  # ..................... for new equation
EMPTY_EQ = "_empty_"  # ..............for no equation
PORT = "port"  # .....................for variables that are to be defined
UNDEF_EQ_NO = "Exxx"  # ..............for no equation defined
CONSTANT = "constant"
NEW_VAR = NEW
TEMP_VARIABLE = "temporary"
LAYER_DELIMITER = "_"
VAR_REG_EXPR = QtCore.QRegExp("[a-zA-Z_]\w*")
BLOCK_INDEX_SEPARATOR = " & "

TOOLTIPS = {}

TOOLTIPS["edit"] = {}
TOOLTIPS["edit"]["type"] = "click to shift variable type"
TOOLTIPS["edit"]["symbol"] = "click to modify symbol"
TOOLTIPS["edit"]["description"] = "modify description"
TOOLTIPS["edit"]["units"] = "time, lenth, amount, mass, temp, current, light\nmay only be modified for _new_ variable"
TOOLTIPS["edit"]["indices"] = "may only be modified for _new_ variable"
TOOLTIPS["edit"]["eqs"] = "add equation"
TOOLTIPS["edit"]["variable"] = "no action"
TOOLTIPS["edit"]["del"] = "delete"
TOOLTIPS["edit"]["network"] = "network where variable is defined"

TOOLTIPS["pick"] = {}
s = "click copy variable symbol into expression editor"
TOOLTIPS["pick"]["type"] = s
TOOLTIPS["pick"]["symbol"] = s
TOOLTIPS["pick"]["description"] = s
TOOLTIPS["pick"]["units"] = s
TOOLTIPS["pick"]["indices"] = s
TOOLTIPS["pick"]["eqs"] = s
TOOLTIPS["pick"]["variable"] = s
TOOLTIPS["pick"]["del"] = s
TOOLTIPS["pick"]["network"] = s


TOOLTIPS["show"] = {}
s = "sorting is enabled & click to see equation"
TOOLTIPS["show"]["type"] = s
TOOLTIPS["show"]["symbol"] = s
TOOLTIPS["show"]["description"] = s
TOOLTIPS["show"]["units"] = s
TOOLTIPS["show"]["indices"] = s
TOOLTIPS["show"]["eqs"] = s
TOOLTIPS["show"]["variable"] = s
TOOLTIPS["show"]["del"] = s
TOOLTIPS["show"]["network"] = s

# ------------
TEMPLATES = {}

# used in compile space
TEMPLATES["temp_variable"] = "temp_%s"

# used in physvars
TEMPLATES["Equation_definition_delimiter"] = ":="
TEMPLATES["definition_delimiter"] = " :: "
TEMPLATES["index_diff_state"] = "d%s"
TEMPLATES["block_index"] = "%s" + BLOCK_INDEX_SEPARATOR + "%s"
TEMPLATES["conversion_label"] = "%s_conversion"
TEMPLATES["conversion_alias"] = "C%s"
# TEMPLATES["sub_index"] = "%s_%s"

# differential space
TEMPLATES["differential_space"] = "d%s"

# table control

# columns are
# 0 type --> new variable
# 1 symbol
# 2 description / documentation
# 3 units
# 4 indices
# 5 equations
# 6 delete

ENABLED_COLUMNS = {}  # TODO: remove hard wiring
ENABLED_COLUMNS["initialise"] = {}
ENABLED_COLUMNS["initialise"]["constant"] = [0, 1, 2, 3, 4, 5]
ENABLED_COLUMNS["initialise"]["state"] = [1, 2, 3, ]
ENABLED_COLUMNS["initialise"]["frame"] = [1, 2, 3, ]
ENABLED_COLUMNS["initialise"]["network"] = [1, 2, 4]
ENABLED_COLUMNS["initialise"]["others"] = []

ENABLED_COLUMNS["edit"] = {}
ENABLED_COLUMNS["edit"]["constant"] = [0, 1, 2, 3, 4, 5, 6]
ENABLED_COLUMNS["edit"]["others"] = [0, 1, 2, 4, 5, 6]
ENABLED_COLUMNS["edit"]["state"] = [1, 2, 3, 4, 5]
ENABLED_COLUMNS["edit"]["frame"] = [1, 2, 3, 4, 5]
ENABLED_COLUMNS["edit"]["network"] = [1, 2, 4, 6]

ENABLED_COLUMNS["inter_connections"] = {}
ENABLED_COLUMNS["inter_connections"]["constant"] = [0, 1, 2, 3, 4, 5, 6]
ENABLED_COLUMNS["inter_connections"]["transposition"] = [0, 1, 2, 5, 6]
ENABLED_COLUMNS["inter_connections"]["others"] = [0, 1, 2, 3, 4, 5, 6]
ENABLED_COLUMNS["inter_connections"]["state"] = [0, 1, 2, 3, 4, 5]

ENABLED_COLUMNS["intra_connections"] = {}
ENABLED_COLUMNS["intra_connections"]["constant"] = [0, 1, 2, 3, 4, 5, 6]
ENABLED_COLUMNS["intra_connections"]["transposition"] = [0, 1, 2, 5, 6]
ENABLED_COLUMNS["intra_connections"]["others"] = [0, 1, 2, 3, 4, 5, 6]
ENABLED_COLUMNS["intra_connections"]["state"] = [0, 1, 2, 3, 4, 5]

# code generation in abstract syntax


LIST_DELIMITERS = ["(", ")", "[", "]", "{", "}", "|", ",", "::", "&", "_"]
LIST_OPERATORS = ["+",  # ................ ordinary plus
                  "-",  # ................ ordinary minus
                  "^",  # ................ oridnary power
                  ":",  # ................ Khatri-Rao product
                  ".",  # ................ expand product
                  "|",  # ................ reduce product
                  "BlockReduce",  # ....... block reduce product
                  "ParDiff",  # .......... partial derivative
                  "TotalDiff",  # ........ total derivative
                  "Integral",  # ......... integral
                  "Product",  # ......... interval
                  "Instantiate",  # ...... instantiate
                  "max",  # .............. maximum
                  "min",  # .............. minimum
                  "in",  # ............... membership    TODO: behaves more like a delimiter...
                  ]

UNITARY_NO_UNITS = ["exp", "log", "ln", "sqrt", "sin", "cos", "tan", "asin", "acos", "atan"]
UNITARY_RETAIN_UNITS = ["abs", "neg", "diffSpace", "left", "right"]
UNITARY_INVERSE_UNITS = ["inv"]
UNITARY_LOOSE_UNITS = ["sign"]
NAMED_FUNCTIONS = ["blockProd", "Root"]

LIST_FUNCTIONS_SINGLE_ARGUMENT = UNITARY_NO_UNITS + UNITARY_RETAIN_UNITS + UNITARY_INVERSE_UNITS + UNITARY_LOOSE_UNITS

LIST_FUNCTIONS = LIST_FUNCTIONS_SINGLE_ARGUMENT + NAMED_FUNCTIONS

CODE = {}

## Languages
LANGUAGES = {}
# LANGUAGES["output"] = ["matlab", "latex"]
LANGUAGES["global_ID"] = "global_ID"
LANGUAGES["global_ID_to_internal"] = "global_ID_to_internal"
LANGUAGES["internal_code"] = "internal_code"
LANGUAGES["internals"] = [LANGUAGES["internal_code"], "global_ID_to_internal"]  # "rename"]
LANGUAGES["code_generation"] = ["global_ID", "python", "cpp", "matlab"]
LANGUAGES["documentation"] = ["latex"]
LANGUAGES["compile"] = LANGUAGES["code_generation"] + LANGUAGES["documentation"]
LANGUAGES["aliasing"] = LANGUAGES["compile"] + [LANGUAGES["internal_code"]]
LANGUAGES["aliasing_modify"] = LANGUAGES["compile"].copy()
LANGUAGES["aliasing_modify"].remove(LANGUAGES["global_ID"])
LANGUAGES["rename"] = "rename"
LANGUAGES["matrix_form"] = ["matlab", "python", "cpp"]

###########    Core representation -- our language

# =====================================================================================================================
language = LANGUAGES["global_ID"]
CODE[language] = {}

ID_spacer = " "

ID_delimiter = {
        "delimiter": ID_spacer + "D_%s",
        "operator" : ID_spacer + "O_%s",
        "function" : ID_spacer + "F_%s",
        "variable" : ID_spacer + "V_%s",
        "index"    : ID_spacer + "I_%s",
        "diff_node": ID_spacer + "diff_%s"
        }

delimiters = {d: ID_delimiter["delimiter"] % LIST_DELIMITERS.index(d) for d in LIST_DELIMITERS}
CODE[language]["delimiter"] = delimiters
CODE[language]["operator"] = {d: ID_delimiter["operator"] % LIST_OPERATORS.index(d) for d in LIST_OPERATORS}
CODE[language]["function"] = {d: ID_delimiter["function"] % LIST_FUNCTIONS.index(d) for d in LIST_FUNCTIONS}

CODE[language]["combi"] = {}
CODE[language]["combi"] = {
        "single_argument": CODE[language]["delimiter"]["("] + "%s" + \
                           CODE[language]["delimiter"][")"],
        "tuple"          : CODE[language]["delimiter"]["("] + "%s" + \
                           CODE[language]["delimiter"][","] + "%s" + \
                           CODE[language]["delimiter"][")"],
        "range"          : CODE[language]["delimiter"]["["] + "%s" + \
                           CODE[language]["delimiter"][","] + "%s" + \
                           CODE[language]["delimiter"]["]"]
        }

# ------------------------------------------------------------------------------------
CODE[language]["bracket"] = delimiters["("] + "%s" + delimiters[")"]

### operators ------------------------------------------------------------------------
CODE[language]["+"] = "%s" + CODE[language]["operator"]["+"] + "%s"
CODE[language]["-"] = "%s" + CODE[language]["operator"]["-"] + "%s"
CODE[language]["^"] = "%s" + CODE[language]["operator"]["^"] + \
                      CODE[language]["delimiter"]["("] + \
                      "%s" + CODE[language]["delimiter"][")"]  # power
CODE[language][":"] = "%s" + CODE[language]["operator"][":"] + "%s"  # Khatri-Rao product
CODE[language]["."] = "%s" + CODE[language]["operator"]["."] + "%s"  # expand product
CODE[language]["|"] = "%s " + CODE[language]["operator"]["|"] + "%s" + \
                      CODE[language]["operator"]["|"] + " %s"  # reduce product
CODE[language]["BlockReduce"] = "{}" + CODE[language]["operator"]["|"] + "{}" + \
                                CODE[language]["operator"]["in"] + "{}" + \
                                CODE[language]["operator"]["|"] + "{}"  # reduce product
CODE[language]["ParDiff"] = CODE[language]["operator"]["ParDiff"] + \
                            CODE[language]["combi"]["tuple"]
CODE[language]["TotalDiff"] = CODE[language]["operator"]["TotalDiff"] + \
                              CODE[language]["combi"]["tuple"]
CODE[language]["Integral"] = CODE[language]["operator"]["Integral"] + \
                             CODE[language]["delimiter"]["("] + \
                             "{integrand!s}" + \
                             CODE[language]["delimiter"]["::"] + \
                             "{differential!s}" + \
                             CODE[language]["operator"]["in"] + \
                             CODE[language]["delimiter"]["["] + \
                             "{lower!s}" + \
                             CODE[language]["delimiter"][","] + \
                             "{upper!s}" + \
                             CODE[language]["delimiter"]["]"] + \
                             CODE[language]["delimiter"][")"]
# CODE[language]["Interval"] = CODE[language]["operator"]["Interval"] + \
#                              CODE[language]["delimiter"]["("] + \
#                              "%s" + \
#                              CODE[language]["operator"]["in"] + \
#                              CODE[language]["combi"]["range"] + \
#                              CODE[language]["delimiter"][")"]
CODE[language]["Product"] = CODE[language]["operator"]["Product"] + \
                            CODE[language]["delimiter"]["("] + "{argument!s}" + \
                            CODE[language]["delimiter"][","] + "{index!s}" + \
                            CODE[language]["delimiter"][")"]
CODE[language]["Instantiate"] = CODE[language]["operator"]["Instantiate"] + \
                                CODE[language]["combi"]["tuple"]

CODE[language]["max"] = CODE[language]["operator"]["max"] + CODE[language]["combi"]["tuple"]
CODE[language]["min"] = CODE[language]["operator"]["min"] + CODE[language]["combi"]["tuple"]

for f in LIST_FUNCTIONS_SINGLE_ARGUMENT:
  CODE[language][f] = CODE[language]["function"][f] + CODE[language]["combi"]["single_argument"]

CODE[language]["blockProd"] = CODE[language]["function"]["blockProd"] + \
                              CODE[language]["delimiter"]["("] + "{}" + \
                              CODE[language]["delimiter"][","] + "{}" + \
                              CODE[language]["operator"]["in"] + "{}" + \
                              CODE[language]["delimiter"][")"]

CODE[language]["Root"] = CODE[language]["function"]["Root"] + CODE[language]["combi"]["tuple"]

CODE[language]["()"] = "%s"  # used by temporary variables

CODE[language]["variable"] = ID_delimiter["variable"]  # ID of the variable
CODE[language]["index"] = ID_delimiter["index"]  # ID of the index
CODE[language]["block_index"] = ID_delimiter["index"]  # ID of the blockindex
CODE[language]["index_diff_state"] = ID_delimiter["diff_node"]  # ID of the variable

CODE[language]["comment"] = ""

# =====================================================================================================================
language = LANGUAGES["global_ID_to_internal"]
source = LANGUAGES["global_ID"]
CODE[language] = {}
CODE[language].update(invertDict(CODE[source]["delimiter"]))
CODE[language].update(invertDict(CODE[source]["operator"]))
CODE[language].update(invertDict(CODE[source]["function"]))

# =====================================================================================================================
language = LANGUAGES["internal_code"]
CODE[language] = {}
CODE[language]["bracket"] = "(" + "%s" + ")"

CODE[language]["+"] = "%s + %s"
CODE[language]["-"] = "%s - %s"
CODE[language]["^"] = "%s^(%s)"  # power
CODE[language][":"] = "%s : %s"  # Khatri-Rao product
CODE[language]["."] = "%s . %s"  # expand product
CODE[language]["|"] = "%s |%s| %s"  # reduce product
CODE[language]["BlockReduce"] = "%s |%s in %s| %s"  # reduce product
CODE[language]["ParDiff"] = "ParDiff(%s,%s)"
CODE[language]["TotalDiff"] = "TotalDiff(%s,%s)"
CODE[language]["Integral"] = "Integral({integrand!s} :: {differential!s} in [{lower!s},{upper!s} ])"
# CODE[language]["Interval"] = "interval(%s in [%s , %s])"
CODE[language]["Product"] = "Product( {argument!s} \, {index!s} )"
CODE[language]["Instantiate"] = "Instantiate(%s, %s)"
CODE[language]["max"] = "max(%s, %s)"
CODE[language]["min"] = "min(%s, %s)"

for f in LIST_FUNCTIONS_SINGLE_ARGUMENT:  # UNITARY_NO_UNITS + UNITARY_RETAIN_UNITS:
  CODE[language][f] = f + "(%s)"  # identical syntax

CODE[language]["Root"] = "Root(%s,%s)"

CODE[language]["blockProd"] = "blockProd({}, {}, {})"  # exception from the above

CODE[language]["()"] = "%s"  # "(%s)"   # TODO: remove bracketing of temp variable (L)
CODE[language]["index"] = "%s"
CODE[language]["index_diff_state"] = "d%s"
CODE[language]["block_index.delimiter"] = " & "
CODE[language]["block_index"] = "%s" + CODE[language]["block_index.delimiter"] + "%s"

CODE[language]["comment"] = ""
CODE[language]["obj"] = "{}"

CODE[language]["variable"] = "%s"  # label of the variable

# =========================================================================================
language = "matlab"
CODE[language] = {}
CODE[language]["bracket"] = "(" + "%s" + ")"

CODE[language]["+"] = "%s + %s"
CODE[language]["-"] = "%s - %s"
CODE[language]["^"] = "%s ** (%s)"
CODE[language][":"] = "KhatriRaoProduct(%s, %s)"  # ..................Khatri-Rao product
CODE[language]["."] = "expandproduct(%s, %s)"  # .....................expand product
CODE[language]["."] = "%s .* %s"  # ..................................expand product
CODE[language]["|"] = "%s * %s"  # ...................................reduce product
CODE[language]["blockProd"] = "blockProduct({}, {}, {})"
CODE[language]["khatri_rao_matrix"] = "khatriRao(%s, %s, %s, %s)"
CODE[language]["ParDiff"] = "ParDiff(%s,%s)"
CODE[language]["TotalDiff"] = "TotalDiff(%s,%s)"
CODE[language]["Integral"] = "Integral({integrand!s},{differential!s}," \
                             "{lower!s},{upper!s})"
CODE[language]["Product"] = "Product( {argument!s} \, {index!s} )"
# CODE[language]["Interval"] = "interval(%s, %s , %s)"
CODE[language]["Instantiate"] = "Instantiate(%s, %s)"  # TODO: can be integrated with list with single input
CODE[language]["max"] = "max(%s, %s)"
CODE[language]["min"] = "min(%s, %s)"

for f in UNITARY_NO_UNITS + UNITARY_INVERSE_UNITS + UNITARY_LOOSE_UNITS:
  CODE[language][f] = f + "(%s)"  # identical syntax

CODE[language]["abs"] = "abs(%s)"
CODE[language]["neg"] = "- %s"
CODE[language]["diffSpace"] = "%s"
CODE[language]["left"] = "left(%s)"
CODE[language]["right"] = "right(%s)"

CODE[language]["blockProd"] = "blockProd({}, {}, {})"
CODE[language]["Root"] = "Root(%s,%s)"

CODE[language]["variable"] = "%s"  # label of the variable

CODE[language]["()"] = "%s"  # "(%s)"
CODE[language]["index"] = "%s"
CODE[language]["index_diff_state"] = "d%s"
CODE[language]["block_index.delimiter"] = "_x_"
CODE[language]["block_index"] = "%s" + CODE[language]["block_index.delimiter"] + "%s"
CODE[language]["transpose"] = "( %s )' "
CODE[language]["BlockReduce"] = "blockReduce({0}, {1}, {2}, {3})"
CODE[language]["matrix_reduce"] = "matrixProduct(%s,%s,%s,%s)"
CODE[language]["comment"] = "%"
CODE[language]["obj"] = "{}"

CODE[language]["variable"] = "%s"  # label of the variable
# ==============================================================================================
language = "python"
CODE[language] = {}
CODE[language]["bracket"] = "(" + "%s" + ")"

CODE[language]["array"] = "np.array(%s)"
CODE[language]["list"] = "np.array"

CODE[language]["+"] = "np.add(%s, %s)"
CODE[language]["-"] = "np.subtract(%s, %s)"
CODE[language]["^"] = "np.power(%s, %s)"
CODE[language][":"] = "khatriRao(%s, %s)"  # .......................Khatri-Rao product
CODE[language]["."] = "np.multiply(%s, %s)"  # .....................expand product
CODE[language]["|"] = "np.dot(%s, %s)"  # ..........................reduce product
CODE[language]["BlockReduce"] = "blockReduce({0}, {1}, {2}, {3})"
CODE[language]["ParDiff"] = "ParDiff(%s, %s)"
CODE[language]["TotalDiff"] = "TotalDiff(%s, %s)"
CODE[language]["Integral"] = "Integral({integrand!s},{differential!s}," \
                             "{lower!s},{upper!s})"
CODE[language]["Product"] = "Product( {argument!s} \, {index!s} )"
# CODE[language]["Interval"] = "interval(%s, %s, %s)"
CODE[language]["Instantiate"] = "np.ones(np.shape(%s)), %s"
CODE[language]["max"] = "np.fmax(%s, %s)"
CODE[language]["min"] = "np.fmin(%s, %s)"

CODE[language]["()"] = "%s"  # "(%s)"    # TODO: remove bracketing of temporary variable in code (L)
CODE[language]["index"] = "%s"
CODE[language]["index_diff_state"] = "d%s"
CODE[language]["block_index.delimiter"] = "_x_"
CODE[language]["block_index"] = "%s" + CODE[language]["block_index.delimiter"] + "%s"
CODE[language]["transpose"] = "np.transpose(%s)"
CODE[language]["matrix_reduce"] = "matrixProduct(%s, %s, %s, %s)"
CODE[language]["khatri_rao_matrix"] = "khatriRao(%s, %s, %s, %s)"
CODE[language]["comment"] = "#"
CODE[language]["exp"] = "np.exp(%s)"
CODE[language]["log"] = "np.log10(%s)"
CODE[language]["ln"] = "np.log(%s)"
CODE[language]["sqrt"] = "np.sqrt(%s)"
CODE[language]["sin"] = "np.sin(%s)"
CODE[language]["asin"] = "np.arcsin(%s)"
CODE[language]["tan"] = "np.tan(%s)"
CODE[language]["atan"] = "np.arctan(%s)"
CODE[language]["cos"] = "np.cos(%s)"
CODE[language]["acos"] = "np.arccos(%s)"
CODE[language]["abs"] = "np.abs(%s )"  # .........................not fabs complex numbers
CODE[language]["neg"] = "np.negative(%s)"
CODE[language]["diffSpace"] = "diffSpace(%s)"
CODE[language]["left"] = "left(%s)"
CODE[language]["right"] = "right(%s)"
CODE[language]["inv"] = "np.reciprocal(%s)"
CODE[language]["sign"] = "np.sign(%s)"
CODE[language]["blockProd"] = "blockProduct({}, {}, {})"
CODE[language]["Root"] = "Root(%s, %s)"
CODE[language]["obj"] = "self.{}"

CODE[language]["variable"] = "%s"  # label of the variable

# ==============================================================================================
language = "cpp"
CODE[language] = {}
CODE[language]["bracket"] = "(" + "%s" + ")"
CODE[language]["array"] = "np.array(%s)"
CODE[language]["list"] = "liste(%s)"

CODE[language]["+"] = "np.add(%s, %s)"
CODE[language]["-"] = "np.subtract(%s, %s)"
CODE[language]["^"] = "np.power(%s, %s)"
CODE[language][":"] = "khatriRao(%s, %s)"  # ........................Khatri-Rao product
CODE[language]["."] = "ganger(%s, %s)"  # ...........................expand product
CODE[language]["|"] = "np.dot(%s, %s)"  # ...........................reduce product
CODE[language]["BlockReduce"] = "blockReduce({0}, {1}, {2}, {3})"
CODE[language]["ParDiff"] = "ParDiff(%s, %s)"
CODE[language]["TotalDiff"] = "TotalDiff(%s, %s)"
CODE[language]["Integral"] = "integral({integrand!s},{differential!s}," \
                             "{lower!s},{upper!s})"
# CODE[language]["Interval"] = "interval(%s, %s, %s)"
CODE[language]["Product"] = "Product( {argument!s} \, {index!s} )"
CODE[language]["Instantiate"] = "np.ones(np.shape(%s)), %s"
CODE[language]["max"] = "np.fmax(%s, %s)"
CODE[language]["min"] = "np.fmin(%s, %s)"

CODE[language]["exp"] = "np.exp(%s)"
CODE[language]["log"] = "np.log10(%s)"
CODE[language]["ln"] = "np.log(%s)"
CODE[language]["sqrt"] = "np.sqrt(%s)"
CODE[language]["sin"] = "np.sin(%s)"
CODE[language]["cos"] = "np.cos(%s)"
CODE[language]["tan"] = "np.tan(%s)"
CODE[language]["asin"] = "np.arcsin(%s)"
CODE[language]["acos"] = "np.arccos(%s)"
CODE[language]["atan"] = "np.arctan(%s)"
CODE[language]["abs"] = "np.abs(%s )"  # not fabs complex numbers
CODE[language]["neg"] = "np.negative(%s)"
CODE[language]["diffSpace"] = "diffSpace(%s)"
CODE[language]["left"] = "left(%s)"
CODE[language]["right"] = "right(%s)"
CODE[language]["inv"] = "np.reciprocal(%s)"
CODE[language]["sign"] = "np.sign(%s)"

CODE[language]["blockProd"] = "blockProduct(%s, %s, %s)"
CODE[language]["Root"] = "Root(%s, %s)"

CODE[language]["()"] = "%s"  # "(%s)"   # TODO: remove corresponding bracketing in temp variables

CODE[language]["index"] = "%s"
CODE[language]["index_diff_state"] = "d%s"
CODE[language]["block_index.delimiter"] = "_x_"
CODE[language]["block_index"] = "%s" + CODE[language]["block_index.delimiter"] + "%s"
CODE[language]["transpose"] = "np.transpose(%s)"
CODE[language]["matrix_reduce"] = "matrixProduct(%s, %s, %s, %s)"
CODE[language]["khatri_rao_matrix"] = "khatriRao(%s, %s, %s, %s)"
CODE[language]["comment"] = "#"

CODE[language]["variable"] = "%s"  # label of the variable

# ============================================================================================
language = "latex"
CODE[language] = {}
CODE[language]["bracket"] = r"\left(" + r"%s" + r"\right)"

CODE[language]["+"] = "%s  + %s"
CODE[language]["-"] = "%s  - %s"
CODE[language]["^"] = "%s^{%s}"  # power
CODE[language][":"] = "%s \, {\odot} \, %s"  # .........................Khatri-Rao product
CODE[language]["."] = "%s \, . \, %s"  # ...............................expand product
CODE[language]["|"] = "%s \stackrel{%s}{\,\star\,} %s"  # ..............reduce product
CODE[language]["BlockReduce"] = "{0} \stackrel{{ {1} \, \in \, {2} }}{{\,\star\,}} {3}"
CODE[language]["ParDiff"] = "\ParDiff{%s}{%s}"
CODE[language]["TotalDiff"] = "\TotDiff{%s}{%s}"
CODE[language]["Integral"] = "\int_{{ {lower!s} }}^{{ {upper!s} }} \, {integrand!s} \enskip d\,{differential!s}"
# CODE[language]["Interval"] = r"%s \in \left[ {%s} , {%s} \right] "
CODE[language]["Product"] = "\prod\left(  {argument!s}   \\right)"
CODE[language]["Instantiate"] = "Set(%s, %s)"
CODE[language]["max"] = r"\mathbf{max}\left( %s, %s \right)"
CODE[language]["min"] = r"\mathbf{min}\left( %s, %s \right)"
CODE[language]["index_diff_state"] = "\dot{%s}"

for f in UNITARY_NO_UNITS:
  CODE[language][f] = f + r"(%s)"

CODE[language]["abs"] = r"|%s|"

CODE[language]["neg"] = r"\left( -%s \right)"
CODE[language]["inv"] = r"\left( %s \right)^{-1}"
CODE[language]["sign"] = r"\text{sign} \left( %s \right)"

CODE[language]["blockProd"] = r"\displaystyle \prod_{{ {1} \in {2} }} {0}"
CODE[language]["Root"] = r"Root\left( %s, %s \right)"

CODE[language]["diffSpace"] = "diffSpace(%s)"
CODE[language]["left"] = "%s^{-\epsilon}"
CODE[language]["right"] = "%s^{+\epsilon}"
CODE[language]["equation"] = "%s = %s"
CODE[language]["()"] = "%s"  # r"\left(%s \right)"
#
CODE[language]["index"] = "{\cal{%s}}"
CODE[language]["block_index.delimiter"] = " "

CODE[language]["variable"] = "%s"  # label of the variable

CODE[language]["block_index"] = "{%s" + \
                                CODE[language]["block_index.delimiter"] + \
                                "%s}"

# generating the operator lists for the equation editor

OnePlace_TEMPLATE = LIST_FUNCTIONS_SINGLE_ARGUMENT
TwoPlace_TEMPLATE = ["+", "-",
                     "^",
                     ".",
                     ":",
                     "ParDiff",
                     "TotalDiff",
                     "max",
                     "min",
                     "Instantiate"
                     ]
ThreePlace_TEMPLATE = ["blockProd"]
internal = LANGUAGES["internal_code"]
Special_TEMPLATE = {
        "Integral"   : CODE[internal]['Integral'].format(integrand='var',
                                                         differential='t',
                                                         lower='l',
                                                         upper='u'),
        "BlockReduce": [],
        "Product"    : CODE[internal]["Product"].format(argument="a",
                                                        index="I")
        }

# TODO: not nice needs fixing
OPERATOR_SNIPS = []
internal = LANGUAGES["internal_code"]
for i in OnePlace_TEMPLATE:
  OPERATOR_SNIPS.append(CODE[internal][i] % ('a'))
for i in TwoPlace_TEMPLATE:
  try:
    OPERATOR_SNIPS.append(CODE[internal][i] % ('a', 'b'))
  except:
    print("failed with :", i)

for i in ThreePlace_TEMPLATE:
  OPERATOR_SNIPS.append(CODE[internal]['|'] % ('a', 'b', 'c'))

for c in Special_TEMPLATE:
  OPERATOR_SNIPS.append(str(Special_TEMPLATE[c]))

OPERATOR_SNIPS.append(CODE[internal]["Root"] % ('expression to be explicit in var', 'var'))


def setValidator(lineEdit):
  validator = QtGui.QRegExpValidator(VAR_REG_EXPR, lineEdit)
  lineEdit.setValidator(validator)
  return validator


def renderExpressionFromGlobalIDToInternal(expression, variables, indices):
  """
  render from global ID representation to internal text representation

  Issue here is that the variable may be of type PhysicalVariable in which case the label is an attribute
    or a dictionary as read from the variable file directly, in which case is is a hash tag
  :param expression:
  :param variables:
  :param indices:
  :return:
  """
  s = ""
  items = expression.split(" ")
  for w in items:
    if w:
      hash = " " + w
      if w[0] in ["D", "O", "F"]:
        if "{" in w:
          print("found a {")
        r = CODE[LANGUAGES["global_ID_to_internal"]]
        try:
          a = CODE[LANGUAGES["global_ID_to_internal"]][hash]
        except:
          # print("debugging", hash)
          a = ""
      elif w[0] == "V":
        v_ID = int(w.replace("V_", "").strip())
        try:
          a = variables[v_ID].label  # RULE: label is used not alias TODO: fix alias edit table -- remove alias
        except:
          a = variables[v_ID]["label"]
      elif w[0] == "I":
        i_ID = int(w.replace("I_", "").strip())
        a = indices[i_ID]["aliases"]["internal_code"]  # RULE: we use alias to reduce length of string
      else:
        a = "bla......%s........" % w
      s += " "
      s += a
  return s


def renderIndexListFromGlobalIDToInternal(indexList, indices):
  """
  render an index list to display representation
  :param indexList:
  :param indices:
  :return: string with indices
  """
  s = ""
  count = 0
  for i_ID in indexList:
    sI = indices[i_ID]["aliases"]["internal_code"]
    if count == 0:
      s += "%s " % sI
    else:
      s += ",  %s" % sI
    count += 1

  return s


def make_variable_equation_pngs(variables, changes, ontology_name):
  global lhs, rhs, reader, line, number, network, error

  rhs = {}
  latex_file = os.path.join(DIRECTORIES["ontology_location"] % ontology_name, "equations_latex.json")
  with open(latex_file, 'r') as reader:
    # Read and print the entire file line by line
    line = reader.readline()
    number, lhs_, rhs[number], network = parseLine(reader)
    while number:  # The EOF char is an empty string
      number, lhs_, rhs[number], network = parseLine(reader)

  lhs = makeVariables(variables)

  f_name = FILES["pnglatex"]
  ontology_location = DIRECTORIES["ontology_location"] % ontology_name

  header = os.path.join(ontology_location, "LaTeX", "resources", "header.tex")

  header_file = open(header, 'w')

  # RULE: make header for equation and variable latex compilations.
  # math packages
  # \usepackage{amsmath}
  # \usepackage{amssymb}
  # \usepackage{calligra}
  # \usepackage{array}
  # \input{../../Ontology_Repository/HAP_playground_02_extend_ontology/LaTeX/resources/defs.tex}
  header_file.write(r"\usepackage{amsmath}")
  header_file.write(r"\usepackage{amssymb}")
  header_file.write(r"\usepackage{calligra}")
  header_file.write(r"\usepackage{array}")
  header_file.write(r"\input{../../Ontology_Repository/%s/LaTeX/resources/defs.tex}" % ontology_name)
  header_file.close()

  for eq_ID in rhs:
    if eq_ID in changes["equations"]["changed"]:
      out = os.path.join(ontology_location, "LaTeX", "equation_%s.png" % eq_ID)

      args = ['bash', f_name, "-P5", "-H", header, "-o", out, "-f", rhs[eq_ID],
              ontology_location]

      try:  # reports an error after completing the last one -- no idea
        make_it = subprocess.Popen(
                args,
                start_new_session=True,
                # restore_signals=False,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE
                )
        out, error = make_it.communicate()
      except:
        pass

  for var_ID in lhs:
    if var_ID in changes["variables"]["changed"]:

      out = os.path.join(ontology_location, "LaTeX", "variable_%s.png" % var_ID)

      args = ['bash', f_name, "-P5", "-H", header, "-o", out, "-f", lhs[var_ID],
              ontology_location]

      try:  # reports an error after completing the last one -- no idea
        make_it = subprocess.Popen(
                args,
                start_new_session=True,
                restore_signals=False,
                # stdout=subprocess.PIPE,
                # stderr=subprocess.PIPE
                )
        out, error = make_it.communicate()
      except:
        pass


def makeVariables(variables):
  lhs = {}
  for var_ID in variables:
    lhs[var_ID] = variables[var_ID]["aliases"]["latex"]
  return lhs


def parseLine(line):
  line1 = reader.readline()
  arr1 = line1.split('"')
  if len(arr1) != 1:
    number = int(arr1[1])
    line2 = reader.readline()
    arr2 = line2.split('"')
    lhs = arr2[3]
    line3 = reader.readline()
    arr3 = line3.split('"')
    network = arr3[3]
    line4 = reader.readline()
    arr4 = line4.split('"')
    rhs = arr4[3].replace('\\\\', '\\')
    line5 = reader.readline()
  else:
    number = None
    lhs = None
    rhs = None
    network = None

  return number, lhs, rhs, network


class VarEqTree():
  """
  Generate a variable equation tree starting with a variable

  self. tree is an object tree with
  tree :
      tree.tree :: a recursive dictionary
                  primary hash :: enumerated object (variable | equation)
                  secondary hash :: ancestor & children
      tree.nodes :: a dictionary with
                  hash :: IDs identifiers of type enumberation (integers)
                  value :: variable_<variable ID> | equation_<equation_ID>
                  a recursive dictionary
      tree.IDs :: inverse of tree.nodes
                  hash :: variable_<variable ID> | equation_<equation_ID>
                  value :: IDs identifiers of type enumberation (integers)
  """
  def __init__(self, variables, var_ID):
    self.TEMPLATE_VARIABLE = "variable_%s"
    self.TEMPLATE_EQUATION = "equation_%s"
    self.variables = variables
    self.tree = ObjectTree(self.TEMPLATE_VARIABLE % var_ID)

    self.initObjects()

    self.makeObjecTree(var_ID)

  def makeObjecTree(self, var_ID):
    Tree = self.tree
    self.starting_node_ID_label = self.TEMPLATE_VARIABLE % var_ID
    stack = []
    eq_IDs = self.get_equs(var_ID)
    for eq_ID in eq_IDs:
      stack.append((var_ID, eq_ID))
    first = True

    var_label = self.TEMPLATE_VARIABLE % var_ID
    self.addVariable(var_label, first)

    while stack:
      var_ID, eq_ID = stack[0]
      stack = stack[1:]  # shift stack

      equ_label = self.TEMPLATE_EQUATION % eq_ID
      var_label = self.TEMPLATE_VARIABLE % var_ID

      Tree.addChildtoNode(equ_label, var_label)
      self.addEquation(equ_label)
      self.addLink(equ_label, var_label)

      vars = self.get_vars(var_ID, eq_ID)
      for next_var_ID in vars:
        next_var_label = self.TEMPLATE_VARIABLE % next_var_ID
        if next_var_label not in Tree.IDs:
          Tree.addChildtoNode(next_var_label, equ_label)
          self.addVariable(next_var_label)
          next_eq_IDs = self.get_equs(next_var_ID)
          for next_eq_ID in next_eq_IDs:
            if next_eq_ID:
              stack.append((next_var_ID, next_eq_ID))
        self.addLink(next_var_label, equ_label)

  def initObjects(self):
    return None

  def addVariable(self, var_ID, first=False):
    None

  def addEquation(selfself, eq_ID, first=False):
    None

  def addLink(self, source_label, sink_label):
    return None

  def get_equs(self, var_ID):
    return self.variables[int(var_ID)]["equations"]

  def get_vars(self, var_ID, eq_ID):
    return self.variables[int(var_ID)]["equations"][eq_ID]["incidence_list"]


class DotGraphVariableEquations(VarEqTree):

  # pdfposter -p999x4A3 vars_equs.pdf try2.pdf

  def __init__(self, variables, indices, var_ID, ontology_name):
    self.ontology_name = ontology_name
    self.indices = indices
    self.latex_directory = os.path.join(DIRECTORIES["ontology_repository"], "%s",
                                        DIRECTORIES["latex"]) % ontology_name

    super().__init__(variables, var_ID)
    self.simple_graph.view()  # generates pdf
    os.remove(self.file)

  def initObjects(self):

    self.var_labels = self.get_var_labels()
    self.equ_labels = self.get_equ_labels()

    o_template = os.path.join(DIRECTORIES["ontology_repository"], self.ontology_name,
                              DIRECTORIES["ontology_graphs_location"],
                              "%s")
    # the tree of networks
    f = o_template % "vars_equs"
    print(f)
    graph_attr = {}
    graph_attr["nodesep"] = "1"
    graph_attr["ranksep"] = ".5"
    graph_attr["color"] = "black"
    graph_attr["splines"] = "true"  # ""polyline"
    edge_attr = {}
    edge_attr["tailport"] = "s"
    edge_attr["headport"] = "n"
    self.simple_graph = Digraph("T", filename=f)
    self.simple_graph.graph_attr = graph_attr
    self.simple_graph.edge_attr = edge_attr

    self.file = f

  def addLink(self, source_label, sink_label):
    if sink_label == self.starting_node_ID_label:
      colour = "red"
    else:
      colour = "black"
    self.simple_graph.edge(source_label, sink_label, color=colour)
    return None

  def get_var_labels(self):
    var_labels = {}
    self.equ_labels = {}
    for var_id in self.variables:
      ID = self.TEMPLATE_VARIABLE % var_id
      var_labels[ID] = self.variables[var_id]["aliases"]["internal_code"]
      for equ_ID in self.variables[var_id]["equations"]:
        ID = self.TEMPLATE_EQUATION % equ_ID
        equation = self.variables[var_id]["equations"][equ_ID]["rhs"]
        rendered_expressions = renderExpressionFromGlobalIDToInternal(equation, self.variables,
                                                                      self.indices)
        self.equ_labels[ID] = rendered_expressions

    return var_labels

  def get_equ_labels(self):
    return self.equ_labels

  def addVariable(self, var_ID_label, first=False):
    node_ID_label = str(var_ID_label)
    node_label = self.var_labels[var_ID_label]
    if first:
      colour = "red"
    else:
      colour = "cornsilk"
    image = os.path.join(self.latex_directory, "%s.png" % var_ID_label)
    self.simple_graph.node(node_ID_label, "", image=image, style="filled", color=colour)

  def addEquation(self, eq_ID_label, first=False):
    node_ID_label = str(eq_ID_label)
    node_label = self.equ_labels[eq_ID_label]
    colour = "cyan"
    image = os.path.join(self.latex_directory, "%s.png" % eq_ID_label)
    self.simple_graph.node(node_ID_label, '', image=image, shape="box", height="0.8cm", style="filled", color=colour)
