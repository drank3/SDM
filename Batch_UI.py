from PySide2 import QtCore, QtGui, QtWidgets


class Batch_Window(object):

    def __init__(self, batch_viewer):

        self.batch_viewer = batch_viewer


        self.h_offset = 18
        self.v_offset = 25

        self.abs_width = self.batch_viewer.width() - 2*self.h_offset
        self.abs_height = self.batch_viewer.height() - 25 - 2*self.v_offset

        self.Create_Tree_Viewer(25, 55)

        self.Set_Header()

        self.batches_loaded = None


    def Set_Header(self):
        self.header4 = QtWidgets.QLabel(self.batch_viewer)
        self.header4.setGeometry(QtCore.QRect(1, 1, 150, 50))
        image = QtGui.QImage("Batch Picture.png")
        image = image.smoothScaled(150, 50)
        pixs = QtGui.QPixmap.fromImage(image)
        self.header4.setPixmap(pixs)


    def Create_Tree_Viewer(self, xPos, yPos):

        self.batch_tree = QtWidgets.QTreeWidget(self.batch_viewer)
        self.batch_tree.setGeometry(QtCore.QRect(self.h_offset-1, self.v_offset + 25, self.abs_width, self.abs_height))
        self.batch_tree.setColumnCount(1)
        self.batch_tree.setLineWidth(2)

        header = QtWidgets.QTreeWidgetItem()
        header.setText(0, "Name")
        header.setBackground(0, QtGui.QBrush(QtGui.QColor(240, 240, 240)))
        header_font = QtGui.QFont()
        header_font.setBold(True)
        header.setFont(0, header_font)

        self.batch_tree.setHeaderItem(header)

    def Insert_Item(self, name, type, parent):
        item = QtWidgets.QTreeWidgetItem(parent)
        item.setText(0, name)
        if type!="Batch":
            item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsAutoTristate)
        else:
            item.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsAutoTristate)
        item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)

        item.type = type

        item.previous_name = name

        return item

    def Change_Item_Color(self, item, color):
        if color == "blue":
            item.setBackground(0, QtGui.QBrush(QtGui.QColor(172, 208, 255, 150)))
        elif color == "green":
            item.setBackground(0, QtGui.QBrush(QtGui.QColor(154, 255, 134, 150)))
