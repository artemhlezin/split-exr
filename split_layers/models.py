from PySide2 import QtCore
import re


class LayersListModel(QtCore.QAbstractListModel):
    Mimetype = 'application/vnd.row.list'
    def __init__(self, layers = [], parent = None):
        QtCore.QAbstractListModel.__init__(self, parent)
        self.__layers = layers

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self.__layers)

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            return self.__layers[index.row()]
        return None

    def dropMimeData(self, data, action, row, column, parent):
        if action == QtCore.Qt.IgnoreAction:
            return True
        if not data.hasFormat(self.Mimetype):
            return False
        if column > 0:
            return False
        if row == -1:
            row = self.rowCount()

        strings = str(data.data(self.Mimetype)).split('\n')
        self.insertRows(row, len(strings))
        for i, text in enumerate(strings):
            self.setData(self.index(row + i, 0), text)
        return True

    def flags(self, index):
        flags = super(LayersListModel, self).flags(index)
        if index.isValid():
            flags |= QtCore.Qt.ItemIsDragEnabled
        else:
            flags = QtCore.Qt.ItemIsDropEnabled
        return flags

    def insertRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), row, row + count - 1)
        self.__layers[row:row] = [''] * count
        self.endInsertRows()
        return True

    def mimeData(self, indexes):
        sortedIndexes = sorted([index for index in indexes
            if index.isValid()], key=lambda index: index.row())
        encodedData = '\n'.join(self.data(index, QtCore.Qt.DisplayRole)
                for index in sortedIndexes)
        encodedData = QtCore.QByteArray(encodedData.encode("utf-8"))
        mimeData = QtCore.QMimeData()
        mimeData.setData(self.Mimetype, encodedData)
        return mimeData

    def mimeTypes(self):
        return [self.Mimetype]

    def removeRows(self, row, count, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), row, row + count - 1)
        del self.__layers[row:row + count]
        self.endRemoveRows()
        return True

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            if role == QtCore.Qt.EditRole:
                value = re.findall("b'(.+)'", value)[0]
                self.__layers[index.row()] = value
                self.dataChanged.emit(index, index)
                return True
        return False

    def supportedDropActions(self):
        return QtCore.Qt.MoveAction