from PySide import QtCore
from PySide import QtGui


class SplitLayersUI(QtGui.QWidget):
    def __init__(self):
        super(SplitLayersUI, self).__init__()
        self.setWindowTitle('Split Layers')
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.resize(550, 340)

        # Widgets
        self.merge_checkbox = QtGui.QCheckBox("Merge all")
        self.merge_checkbox.setChecked(True)
        self.unpremult_checkbox = QtGui.QCheckBox('Unpremult all')
        self.unpremult_checkbox.setChecked(True)
        self.postagestamp_checkbox = QtGui.QCheckBox('Postage Stamp')
        self.postagestamp_checkbox.setChecked(False)
        self.mirrortree_checkbox = QtGui.QCheckBox('Mirror tree')
        self.mirrortree_checkbox.setChecked(False)

        method_label = QtGui.QLabel('Method')
        method_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.method_combobox = QtGui.QComboBox()
        self.method_combobox.addItems(['implicit', 'explicit'])
        self.method_combobox.setCurrentIndex(1)    # set explicit by default

        alpha_label = QtGui.QLabel('Alpha')
        alpha_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.alpha_combobox = QtGui.QComboBox()

        input_label = QtGui.QLabel('Input:')
        self.input_listview = QtGui.QListView()
        self.input_listview.setAlternatingRowColors(True)
        self.input_listview.setDragEnabled(True)
        self.input_listview.setAcceptDrops(True)
        self.input_listview.setDropIndicatorShown(True)
        self.input_listview.setSelectionMode(self.input_listview.ExtendedSelection)

        split_label = QtGui.QLabel('For split:')
        self.split_listview = QtGui.QListView()
        self.split_listview.setAlternatingRowColors(True)
        self.split_listview.setDragEnabled(True)
        self.split_listview.setAcceptDrops(True)
        self.split_listview.setDropIndicatorShown(True)
        self.split_listview.setSelectionMode(self.split_listview.ExtendedSelection)

        self.filter_lineedit = QtGui.QLineEdit()
        self.filter_lineedit.setPlaceholderText("Filter Layers")
        filter_tooltip = r"""Filter provides pattern matching using regular expressions.
CASEINSENSITIVE by default.

Cheatsheet:
.           any single character
\w          any word character
\d          any didgit
\s          any whitespace character
\W          any non-word character
\D          any non-didgit
\S          any non-whitespace character
[abc]       a single character of: a, b, or c
[^abc]      a character except: a, b, or c
[a-z]       character in the range: a-z

^           start of the string
$           end of the string

\. \* \\    escaped special characters

(abc)       capture group
(a|b)       match either a or b
(?:abc)     non-capturing group
(?=abc)     positive lookahead
(?!abc)     negative lookahead

a?          zero or one of a
a*          zero or more of a
a+          one or more of a
a{3}        exactly 3 of a
a{1,3}      between one and three of a
"""

        self.filter_lineedit.setToolTip(filter_tooltip)

        self.split_pushbutton = QtGui.QPushButton('Split')
        self.cancel_pushbutton = QtGui.QPushButton('Cancel')

        # Layouts
        top_left_layout = QtGui.QGridLayout()
        top_left_layout.addWidget(self.merge_checkbox, 0 ,0)
        top_left_layout.addWidget(self.unpremult_checkbox, 1, 0)
        top_left_layout.addWidget(self.postagestamp_checkbox, 0, 1)
        top_left_layout.addWidget(self.mirrortree_checkbox, 1, 1)


        top_right_layout = QtGui.QGridLayout()
        top_right_layout.addWidget(method_label, 0, 1)
        top_right_layout.addWidget(self.method_combobox, 0, 2)
        top_right_layout.addWidget(alpha_label, 1, 1)
        top_right_layout.addWidget(self.alpha_combobox, 1, 2)

        top_layout = QtGui.QHBoxLayout()
        top_layout.addLayout(top_left_layout)
        top_layout.addLayout(top_right_layout)

        action_layout = QtGui.QHBoxLayout()
        action_layout.addWidget(self.split_pushbutton)
        action_layout.addWidget(self.cancel_pushbutton)

        layers_layout = QtGui.QGridLayout()
        layers_layout.addWidget(input_label, 0, 0)
        layers_layout.addWidget(split_label, 0, 1)
        layers_layout.addWidget(self.input_listview, 1, 0)
        layers_layout.addWidget(self.split_listview, 1, 1)
        layers_layout.addWidget(self.filter_lineedit, 2, 0)
        layers_layout.addLayout(action_layout, 2, 1)

        root_layout = QtGui.QVBoxLayout()
        root_layout.addLayout(top_layout)
        root_layout.addLayout(layers_layout)

        self.setLayout(root_layout)