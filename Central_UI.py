from PySide2 import QtCore, QtGui, QtWidgets
from UI_Layouts import Layouts
from Menu_UI import Main_Menus
import Attributes_UI
import Parameters_UI
import Structure_UI
import Batch_UI
import Devices_UI
import Results_UI
import Info_UI
import ctypes
import os
import json





class Central_UI(object):

#TODO: Windows kind of stutter when resizing, maybe use global pos instead of local ones when moving stuff
#TODO: ScrollArea Stuff
#TODO: Make fonts look nicer
#TODO: Make Attr window look nicer
#TODO: Redesign the header images, maybe add color schemes to them and give a trail
#TODO: Buttons look gross, fix them (pwpnt has some good bevel options I guess)
#TODO: Add in that feature to change the ratio between the two scroll areas

    def __init__(self):
        #I kind of understand this super line, its just making sure that QtWidget init is not overridden
        super(QtWidgets.QWidget).__init__()
        self.mode = "Importer"


        self.MainWindow = QtWidgets.QMainWindow()

        self.setupUi()
        self.main_menus = Main_Menus(self)
        self.main_menus.All_Menus_Init()

        #These two lines force the icon in the taskbar to be the one I want, instead of the random python one
        myappid = u'device_manager' # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

        #This way, the app always starts with the mode being Importer by default
        self.Change_Mode("Importer")

        self.MainWindow.show()




        with open(os.path.dirname(__file__) + r'/System Settings/Settings.txt', 'r') as file:
            system_settings = json.load(file)
            self.user = system_settings['Username']


    def setupUi(self):


        #Setting the base window up, most of this is uninteresting/redundant
        self.MainWindow.setObjectName("self.MainWindow")
        self.MainWindow.resize(1100, 700)
        #self.MainWindow.setFixedSize(1100, 700)
        self.MainWindow.resize(1100, 700)
        self.MainWindow.move(400, 100)


        #self.MainWindow.showMaximized()
        self.MainWindow.setWindowTitle("Device Manager")


        icon = QtGui.QIcon("Icon.png")
        self.MainWindow.setWindowIcon(icon)



        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setBold(False)
        font.setWeight(50)
        self.MainWindow.setFont(font)
        self.MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.MainWindow.setAutoFillBackground(False)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.layouts = Layouts(self)
        self.layouts.Resizing(self.MainWindow)

        #These are the windows associated with the Importer mode
        self.AUI = Attributes_UI.Attributes_Window(self.attribute_viewer)
        self.PUI = Parameters_UI.Parameters_Window(self.parameter_viewer)
        self.SUI = Structure_UI.Structure_Window(self.structure_viewer)
        self.BUI = Batch_UI.Batch_Window(self.batch_viewer)

        #These are the windows associated with the Viewer mode
        self.DUI = Devices_UI.Devices_Window(self.devices_viewer)
        self.IUI = Info_UI.Info_Window(self.info_viewer)
        self.RUI = Results_UI.Results_Window(self.results_viewer)


        self.MainWindow.setCentralWidget(self.centralwidget)


        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)



        #Passing the function with the actual amount of children the scrollbox has
        #Creating the first frame (to build up a new recipe)
        self.PUI.Create_Grid(0, "Par", self.parameter_viewer)

        self.main_menus = Main_Menus(self)

    #Just a convenience function to make a dialog message
    def Show_Dialog(self, top, text, detailed_info=None):

       msg = QtWidgets.QMessageBox()
       msg.setIcon(QtWidgets.QMessageBox.Information)
       msg.setText(text)
       msg.setWindowTitle(top)
       if detailed_info:
           msg.setDetailedText("The details are as follows:")
       msg.setStandardButtons(QtWidgets.QMessageBox.Ok)

       return(msg)

    #This function is triggered whenever the modes Importer or Viewer are changed from the menu system
    #While check the importer, hide the windows not in the selected modes, and make visible those that are
    def Change_Mode(self, new_mode):

        if new_mode == "Importer":
            self.mode = new_mode

            #Showing or hiding the associated windows
            #----------------------------------------
            self.actionImporter.setChecked(True)
            self.actionViewer.setChecked(False)

            self.devices_viewer.setVisible(False)
            self.results_viewer.setVisible(False)
            self.info_viewer.setVisible(False)

            self.attribute_viewer.setVisible(True)
            self.parameter_viewer.setVisible(True)
            self.batch_viewer.setVisible(True)
            self.structure_viewer.setVisible(True)
            #---------------------------------------

            #Showing or hiding the relevant menu items
            self.main_menus.Set_Menus_Mode("Importer")

        if new_mode == "Viewer":
            self.mode = new_mode

            self.actionViewer.setChecked(True)
            self.actionImporter.setChecked(False)


            self.devices_viewer.setVisible(True)
            self.results_viewer.setVisible(True)
            self.info_viewer.setVisible(True)

            self.attribute_viewer.setVisible(False)
            self.parameter_viewer.setVisible(False)
            self.batch_viewer.setVisible(False)
            self.structure_viewer.setVisible(False)

            #Showing or hiding the relevant menu items
            self.main_menus.Set_Menus_Mode("Viewer")

        self.layouts.Resizing(self.MainWindow)








if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    nice = Central_UI()


    sys.exit(app.exec_())
