from PySide2 import QtCore, QtGui, QtWidgets

#This class is very similar to that of the batches set viewer, but reimplemented
class Devices_Window(object):

    def __init__(self, devices_viewer):

        self.devices_viewer = devices_viewer


        self.h_offset = 18
        self.v_offset = 25

        self.abs_width = self.devices_viewer.width() - 2*self.h_offset
        self.abs_height = self.devices_viewer.height() - 25 - 2*self.v_offset
        self.Create_Tree_Viewer()


    def Create_Tree_Viewer(self):

        self.devices_tree = QtWidgets.QTreeWidget(self.devices_viewer)
        self.devices_tree.setGeometry(QtCore.QRect(self.h_offset-1, self.v_offset, self.abs_width, self.abs_height))
        self.devices_tree.setColumnCount(1)
        self.devices_tree.setLineWidth(2)

        header = QtWidgets.QTreeWidgetItem()
        header.setText(0, "Name")
        header.setBackground(0, QtGui.QBrush(QtGui.QColor(240, 240, 240)))
        header_font = QtGui.QFont()
        header_font.setBold(True)
        header.setFont(0, header_font)

        self.devices_tree.setHeaderItem(header)

    def Insert_Item(self, name, type, parent):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, name)
        if type=="Device":
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsAutoTristate)
        elif type=="Group":
            item.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsAutoTristate)
        elif type=="Pixel":
            item.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsAutoTristate)
        item.type = type

        item.previous_name = name

        return item

    def Resize(self):
        self.abs_width = self.devices_viewer.width() - 2*self.h_offset
        self.abs_height = self.devices_viewer.height() - 2*self.v_offset
        self.devices_tree.setGeometry(QtCore.QRect(self.h_offset-1, self.v_offset, self.abs_width, self.abs_height))
