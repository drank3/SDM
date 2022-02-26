VSpacer = 3
VHeight = 40
HSpacer = 20

from PySide2 import QtCore, QtGui, QtWidgets

class Parameters_Window(object):

    def __init__(self, existing_widget):
        self.VSpacer, self.VHeight, self.HSpacer = [VSpacer, VHeight, HSpacer]
        self.parameter_viewer = existing_widget

        self.Set_Header()


    def Set_Header(self):

        self.header = QtWidgets.QLabel(self.parameter_viewer)
        self.header.setGeometry(QtCore.QRect(1, 1, 150, 50))
        image = QtGui.QImage("Param Picture.png")
        image = image.smoothScaled(150, 50)
        pixs = QtGui.QPixmap.fromImage(image)

        self.header.setPixmap(pixs)


    """
    Creates a grid with an inital plus button
    """

    def Create_Grid(self, num, name, location):

        #The x position of the first column of Parameters
        first_location = 25

        #Finds the location and size of the last frame, and sets a new one a certain distance away
        child_frames = self.parameter_viewer.children()
        lastFrame = child_frames[-1]
        xPos = lastFrame.x()
        yPos = lastFrame.y()
        width = lastFrame.width()
        #How much the frames are separated by

        self.frame = QtWidgets.QFrame(self.parameter_viewer)

        #Controls the position of the first column of parameters
        if num == 0:
            self.frame.setGeometry(QtCore.QRect(first_location, 20, 120, 80))
        else:
            self.frame.setGeometry(QtCore.QRect(xPos+width+HSpacer, 20, 120, 80))

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.frame.setFrameShape(QtWidgets.QFrame.Panel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame_"+str(num))
        plus = self.Create_Plus(0, 30, name, self.frame)
        self.frame.setVisible(True)

        return plus



    def Create_Plus(self, xPos, yPos, name, location):
        #The box is set to be wider than the actual label so spacing is maintained
        box = QtWidgets.QFrame(location)
        box.setGeometry(QtCore.QRect(xPos, yPos, VHeight, VHeight))
        box.setObjectName("box")
        label = QtWidgets.QLabel(box)
        label.setGeometry(QtCore.QRect(0, 0, 20, 20))
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        label.setFont(font)
        label.setText("+")

        label.setFrameShape(QtWidgets.QFrame.Box)
        label.setFrameShadow(QtWidgets.QFrame.Raised)
        label.setAlignment(QtCore.Qt.AlignCenter)

        label.setObjectName("Add@"+name)
        label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        box.setVisible(True)

        return box



    def Create_Cell(self, xPos, yPos, type, name, location):


        cell1 = QtWidgets.QLabel(location)
        cell1.setGeometry(QtCore.QRect(xPos, yPos, 51, VHeight))
        cell1.setText(name)
        font = QtGui.QFont()
        font.setFamily("Helvetica")
        font.setBold(False)
        font.setWeight(60)
        font.setPointSize(15)
        cell1.setFont(font)
        cell1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        cell1.setToolTipDuration(1)
        cell1.setFrameShape(QtWidgets.QFrame.Box)
        cell1.setFrameShadow(QtWidgets.QFrame.Raised)
        cell1.setStyleSheet('''background-color: rgb(248,248,248);''')
        cell1.setLineWidth(2)
        cell1.setTextFormat(QtCore.Qt.RichText)
        cell1.setScaledContents(True)
        cell1.setAlignment(QtCore.Qt.AlignCenter)
        cell1.adjustSize()
        cell1.resize(cell1.width()+10, VHeight-5)
        cell1.setObjectName(type+"@"+name)
        cell1.setVisible(True)


        #status = 0 means the button is unpressed, 1 means it is pressed
        cell1.status = 0

        return cell1

    def Create_TextEdit(self, xPos, yPos, num, location):
        self.lineEdit = QtWidgets.QLineEdit(location)
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit.setFont(font)
        self.lineEdit.setGeometry(QtCore.QRect(xPos, yPos, 160, VHeight))
        self.lineEdit.setObjectName("lineEdit"+str(num))
        self.lineEdit.setPlaceholderText("Enter Name")
        self.lineEdit.setVisible(True)
        location.adjustSize()
        return self.lineEdit

    def Context_Menu(self, location, event):
        self.menuok = QtWidgets.QMenu(self.parameter_viewer.parent())
        self.menuok.setObjectName("menuok")
        self.menuok.setGeometry(QtCore.QRect(0, 0, 25, 21))
        self.actionDelete = QtWidgets.QAction(self.menuok)
        self.actionDelete.setObjectName("actionNot_me")
        self.menuok.addAction(self.actionDelete)
        self.menuok.setTitle("Attribute Menu")
        self.actionDelete.setText("Delete")
        self.actionDelete.trigger = self.parameter_viewer.childAt(event.pos())
        self.menuok.popup(event.globalPos())
