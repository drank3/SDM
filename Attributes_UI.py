VSpacer = 5
VHeight = 25
HSpacer = 25
Indent = 10
from PySide2 import QtCore, QtGui, QtWidgets
import traceback

class Attributes_Window(object):

    def __init__(self, existing_widget):
        self.VSpacer, self.VHeight, self.HSpacer, self.Indent = [VSpacer, VHeight, HSpacer, Indent]
        self.attribute_viewer = existing_widget
        self.plus_width = 14

        self.Set_Header()

        self.Top_Buttons()

        self.Create_Tree_Viewer()

        self.attribute_viewer.layout.setRowStretch(0, 1)
        self.attribute_viewer.layout.setRowStretch(1, 20)
        self.attribute_viewer.layout.setRowStretch(2, 3)
        self.attribute_viewer.layout.setRowStretch(3, 150)

        self.attribute_viewer.layout.setColumnStretch(0, 1)
        self.attribute_viewer.layout.setColumnStretch(1, 25)
        self.attribute_viewer.layout.setColumnStretch(2, 25)
        self.attribute_viewer.layout.setColumnStretch(3, 1)

        self.attribute_viewer.layout.setHorizontalSpacing(1)
        self.attribute_viewer.layout.setContentsMargins(13, self.header.height(), 13, 13)

    def Set_Header(self):

        self.header = QtWidgets.QLabel(self.attribute_viewer)
        self.header.setGeometry(QtCore.QRect(1, 1, 150, 50))
        image = QtGui.QImage("Attr Picture.png")
        image = image.smoothScaled(150, 50)
        pixs = QtGui.QPixmap.fromImage(image)
        self.header.setPixmap(pixs)



    def Insert_Item(self, name, value, type, parent):
        print(parent)
        attr = QtWidgets.QTreeWidgetItem(parent)
        attr.setText(0, name)
        if type == "Attr":
            attr.setText(1, value)
            attr.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable)
        else:
            attr.setFlags(QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsAutoTristate)


        attr.type = type

        if name == "Enter Name":
            attr.previous_name = None
        else:
            attr.previous_name = name


        if str(parent) == str(self.viewer):
            attr.path = []
        elif not parent.path:
            attr.path = [parent.text(0)]
            parent.setExpanded(True)
        elif parent.path:
            attr.path = parent.path + [parent.text(0)]
            parent.setExpanded(True)
        return attr




    def Create_Tree_Viewer(self):

        self.viewer = QtWidgets.QTreeWidget()
        self.attribute_viewer.layout.addWidget(self.viewer, 3, 1, 1, 2)
        #sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        #sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        #self.viewer.setSizePolicy(sizePolicy)
        self.viewer.setObjectName("Attr@Viewer")
        self.viewer.setGeometry(QtCore.QRect(0, 0, 300, 300))
        self.viewer.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.viewer.setFrameShape(QtWidgets.QFrame.Panel)
        self.viewer.setLineWidth(1)
        self.viewer.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.viewer.setColumnCount(2)
        self.viewer.header().resizeSection(0, self.viewer.width()*.6)

        #self.viewer.setHeaderHidden(True)

        header = QtWidgets.QTreeWidgetItem()
        header.setText(0, " Name")
        header.setText(1, " Value")
        header_font = QtGui.QFont()
        header_font.setBold(True)
        header_font.setPointSize(11)

        header.setFont(0, header_font)
        header.setFont(1, header_font)

        self.viewer.setHeaderItem(header)
        self.viewer.setMouseTracking(True)
        self.viewer.setAlternatingRowColors(True)
        return self.viewer


    def Top_Buttons(self):


        button_height = 35
        button_h_offset = 20
        button_width = (self.attribute_viewer.width())/2 - button_h_offset

        font = QtGui.QFont()
        font.setPointSize(15)

        self.Add_Variable = QtWidgets.QLabel()
        self.attribute_viewer.layout.addWidget(self.Add_Variable, 1, 0, 1, 2)
        self.Add_Variable.setObjectName("Add@Attr_Variable")
        self.Add_Variable.setGeometry(QtCore.QRect(button_h_offset, 45, button_width, button_height))
        self.Add_Variable.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.Add_Variable.setText("Add Variable")
        self.Add_Variable.setAlignment(QtCore.Qt.AlignCenter)
        self.Add_Variable.setFont(font)
        self.Add_Variable.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))


        self.Add_Group = QtWidgets.QLabel()
        self.attribute_viewer.layout.addWidget(self.Add_Group, 1, 2, 1, 2)
        self.Add_Group.setObjectName("Add@Attr_Group")
        self.Add_Group.setGeometry(QtCore.QRect(button_h_offset + button_width, 45, button_width, button_height))
        self.Add_Group.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
        self.Add_Group.setText("Add Group")
        self.Add_Group.setAlignment(QtCore.Qt.AlignCenter)
        self.Add_Group.setFont(font)
        self.Add_Group.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

    def Context_Menu(self, point, parent):
        print("triggered")
        menu = QtWidgets.QMenu(parent)
        menu.setObjectName("menuok")
        menu.setGeometry(QtCore.QRect(0, 0, 25, 21))
        self.actionDelete = QtWidgets.QAction(menu)
        self.actionDelete.setObjectName("actionNot_me")
        menu.addAction(self.actionDelete)
        menu.setTitle("Attribute Menu")
        self.actionDelete.setText("Delete")
        menu.popup(point)
