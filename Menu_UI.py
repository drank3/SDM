from PySide2 import QtCore, QtGui, QtWidgets
class Main_Menus:
    def __init__(self, ui):
        #Adding an attribute link to the ui object here because I'm ignorant
        self.ui = ui


    #Sets up all the menus and actions for the main window
    def All_Menus_Init(self):
        self.ui.menubar = QtWidgets.QMenuBar(self.ui.MainWindow)
        self.ui.menubar.setGeometry(QtCore.QRect(0, 0, 1692, 21))
        self.ui.menubar.setObjectName("menubar")
        self.ui.MainWindow.setMenuBar(self.ui.menubar)
        self.ui.statusbar = QtWidgets.QStatusBar(self.ui.MainWindow)
        self.ui.statusbar.setObjectName("statusbar")
        self.ui.MainWindow.setStatusBar(self.ui.statusbar)

        """ Stuff for the file menu option"""

        self.ui.menuFile = QtWidgets.QMenu(self.ui.menubar)
        self.ui.menuFile.setObjectName("menuFile")
        self.ui.menuFile.setTitle("File")
        self.ui.menubar.addAction(self.ui.menuFile.menuAction())

        self.ui.menuMode = QtWidgets.QMenu(self.ui.MainWindow)
        self.ui.menuMode.setObjectName("Mode")
        self.ui.menuMode.setTitle("Mode")
        self.ui.menuFile.addAction(self.ui.menuMode.menuAction())


        self.ui.actionImporter = QtWidgets.QAction(self.ui.menuMode)
        self.ui.actionImporter.setCheckable(True)
        self.ui.actionImporter.setObjectName("Importer")
        self.ui.actionImporter.setText("Importer")
        self.ui.menuMode.addAction(self.ui.actionImporter)

        self.ui.actionImporter.setChecked(True)
        self.ui.actionImporter.setEnabled(True)


        self.ui.actionViewer = QtWidgets.QAction(self.ui.menuMode)
        self.ui.actionViewer.setCheckable(True)
        self.ui.actionViewer.setObjectName("Viewer")
        self.ui.actionViewer.setText("Viewer")
        self.ui.menuMode.addAction(self.ui.actionViewer)

        self.ui.actionViewer.setChecked(False)
        self.ui.actionViewer.setEnabled(True)



        self.ui.actionExport = QtWidgets.QAction(self.ui.MainWindow)
        self.ui.actionExport.setObjectName("actionExport")
        self.ui.menuFile.addAction(self.ui.actionExport)
        self.ui.actionExport.setText("Export Recipe")

        self.ui.actionSync = QtWidgets.QAction(self.ui.MainWindow)
        self.ui.actionSync.setObjectName("actionSync")
        self.ui.menuFile.addAction(self.ui.actionSync)
        self.ui.actionSync.setText("Sync to Database")



        """Stuff for the View menu option"""
        self.ui.menuView = QtWidgets.QMenu(self.ui.menubar)
        self.ui.menuView.setObjectName("menuView")
        self.ui.menuView.setTitle("View")
        self.ui.menubar.addAction(self.ui.menuView.menuAction())


        """Stuff for the Devices menu option"""
        self.ui.menuDevices = QtWidgets.QMenu(self.ui.menubar)
        self.ui.menuDevices.setObjectName("menuDevices")
        self.ui.menubar.addAction(self.ui.menuDevices.menuAction())
        self.ui.menuDevices.setTitle("Devices")

        self.ui.actionImport_Devices = QtWidgets.QAction(self.ui.menuDevices)
        self.ui.actionImport_Devices.setObjectName("actionImport_Devices")
        self.ui.actionImport_Devices.setText("Import New Devices")
        self.ui.menuDevices.addAction(self.ui.actionImport_Devices)

        self.ui.actionSave_All_Device_Data = QtWidgets.QAction(self.ui.menuDevices)
        self.ui.actionSave_All_Device_Data.setObjectName("actionSave_All_Device_Data")
        self.ui.actionSave_All_Device_Data.setText("Save All Device Data")
        self.ui.menuDevices.addAction(self.ui.actionSave_All_Device_Data)

        self.ui.actionSet_Selected_Device_Structure = QtWidgets.QAction(self.ui.menuDevices)
        self.ui.actionSet_Selected_Device_Structure.setObjectName("actionSet_Selected_Device_Structure")
        self.ui.actionSet_Selected_Device_Structure.setText("Set Selected Device Structure")
        self.ui.menuDevices.addAction(self.ui.actionSet_Selected_Device_Structure)

        self.ui.actionExport_Selected_Devices_Structure = QtWidgets.QAction(self.ui.menuDevices)
        self.ui.actionExport_Selected_Devices_Structure.setObjectName("actionExport_Selected_Devices_Structure")
        self.ui.actionExport_Selected_Devices_Structure.setText("Export Selected Device Structure")
        self.ui.menuDevices.addAction(self.ui.actionExport_Selected_Devices_Structure)

        self.ui.actionQuick_Analysis = QtWidgets.QAction(self.ui.menuDevices)
        self.ui.actionQuick_Analysis.setObjectName("actionQuick_Anlaysis")
        self.ui.actionQuick_Analysis.setText("Quick Analysis")
        self.ui.menuDevices.addAction(self.ui.actionQuick_Analysis)


        """Stuff for the Materials menu option"""
        self.ui.menuMaterials = QtWidgets.QMenu(self.ui.menubar)
        self.ui.menuMaterials.setObjectName("menuMaterials")
        self.ui.menubar.addAction(self.ui.menuMaterials.menuAction())
        self.ui.menuMaterials.setTitle("Materials")

        self.ui.actionLoad_Default_Materials = QtWidgets.QAction(self.ui.menuMaterials)
        self.ui.actionLoad_Default_Materials.setObjectName("actionLoad_Default_Materials")
        self.ui.actionLoad_Default_Materials.setText("Load Default Materials")
        self.ui.menuMaterials.addAction(self.ui.actionLoad_Default_Materials)

        self.ui.actionSave_Default_Materials = QtWidgets.QAction(self.ui.menuMaterials)
        self.ui.actionSave_Default_Materials.setObjectName("actionSave_Default_Materials")
        self.ui.actionSave_Default_Materials.setText("Save Default Materials")
        self.ui.menuMaterials.addAction(self.ui.actionSave_Default_Materials)


        """Stuff for the Structures menu Option"""
        self.ui.menuStructures = QtWidgets.QMenu(self.ui.menubar)
        self.ui.menuStructures.setObjectName("menuStructures")
        self.ui.menubar.addAction(self.ui.menuStructures.menuAction())
        self.ui.menuStructures.setTitle("Structures")

        self.ui.actionLoad_Structure = QtWidgets.QAction(self.ui.menuStructures)
        self.ui.actionLoad_Structure.setObjectName("actionLoad_Structure")
        self.ui.actionLoad_Structure.setText("Load Structure")
        self.ui.menuStructures.addAction(self.ui.actionLoad_Structure)

        self.ui.actionSave_Structure = QtWidgets.QAction(self.ui.menuStructures)
        self.ui.actionSave_Structure.setObjectName("actionSave_Structure")
        self.ui.actionSave_Structure.setText("Save Structure")
        self.ui.menuStructures.addAction(self.ui.actionSave_Structure)

        self.ui.actionExport_Structure = QtWidgets.QAction(self.ui.menuStructures)
        self.ui.actionExport_Structure.setObjectName("actionExport_Structure")
        self.ui.actionExport_Structure.setText("Export Structure")
        self.ui.menuStructures.addAction(self.ui.actionExport_Structure)


    def Set_Menus_Mode(self, mode):
        if mode == "Importer":
            #Quickly checking to see if the menubar is already in Importer mode
            #Doing this just by checking to see if there is a structures menu
            #   if not, the condition is satisfied
            if self.ui.menuStructures.menuAction() not in self.ui.menubar.actions():
                self.ui.menubar.addAction(self.ui.menuDevices.menuAction())
                self.ui.menubar.addAction(self.ui.menuMaterials.menuAction())
                self.ui.menubar.addAction(self.ui.menuStructures.menuAction())




        elif mode=="Viewer":
            if self.ui.menuStructures.menuAction() in self.ui.menubar.actions():
                self.ui.menubar.removeAction(self.ui.menuDevices.menuAction())
                self.ui.menubar.removeAction(self.ui.menuMaterials.menuAction())
                self.ui.menubar.removeAction(self.ui.menuStructures.menuAction())
