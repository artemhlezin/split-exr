import nuke
from PySide2 import QtCore
from PySide2 import QtGui
from models import LayersListModel
from ui import SplitLayersUI
import nuke_actions



def main():
    node = None
    try:
        node = nuke.selectedNode()
    except ValueError as err:
        print err
        nuke.message('no node selected')
    if node:
        node_data = data_collect(node)
        main.panel = SplitLayers(node_data, nuke_actions.split_explicit, nuke_actions.split_implicit)
        main.panel.show()

def data_collect(node):
    data = {'node': None, 'channels': [], 'layers': [], 'split_layers':[]}
    data['node'] = node
    data['channels'] = node.channels()
    data['layers'] = sorted(list(set([c.split('.')[0] for c in node.channels()])))
    return data

class SplitLayers(SplitLayersUI):
    def __init__(self, data, split_explicit, split_implicit):
        super(SplitLayers, self).__init__()

        self.node = data['node']
        self.channels = data['channels']
        self.layers = data['layers']
        self.layers_for_split = data['split_layers']
        self.split_explicit = split_explicit
        self.split_implicit = split_implicit

        self.proxyModel = QtCore.QSortFilterProxyModel()
        self.input_model = LayersListModel(self.layers)
        self.split_model = LayersListModel(self.layers_for_split)

        self.proxyModel.setSourceModel(self.input_model)
        self.proxyModel.setDynamicSortFilter(True)

        self.proxyModel.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)

        self.input_listview.setModel(self.proxyModel)
        self.split_listview.setModel(self.split_model)


        self.alpha_combobox.addItems(self.channels)
        i = self.alpha_combobox.findText('rgba.alpha')
        self.alpha_combobox.setCurrentIndex(i)
        self.filter_lineedit.textChanged.connect(self.proxyModel.setFilterRegExp)

        self.split_pushbutton.clicked.connect(lambda: self.split(self.method_combobox.currentText()))
        self.cancel_pushbutton.clicked.connect(self.close)
        self.method_combobox.currentIndexChanged.connect(self.check_method)

    def check_method(self, index):
        if index == 0: # if implicit
            self.unpremult_checkbox.setEnabled(False)
            self.merge_checkbox.setEnabled(False)
            self.postagestamp_checkbox.setEnabled(False)
            self.alpha_combobox.setEnabled(False)
            self.mirrortree_checkbox.setEnabled(False)
        else:
            self.unpremult_checkbox.setEnabled(True)
            self.merge_checkbox.setEnabled(True)
            self.postagestamp_checkbox.setEnabled(True)
            self.alpha_combobox.setEnabled(True)
            self.mirrortree_checkbox.setEnabled(True)

    def split(self, method):
        if method == 'explicit':
            self.split_explicit(self.node, self.layers_for_split, self.alpha_combobox.currentText(),
                                self.unpremult_checkbox.isChecked(), self.merge_checkbox.isChecked(),
                                self.postagestamp_checkbox.isChecked(), self.mirrortree_checkbox.isChecked())
        elif method == 'implicit':
            self.split_implicit(self.node, self.layers_for_split)
        self.close()