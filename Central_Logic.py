from PySide2 import QtCore, QtGui, QtWidgets
import Par_and_Attr_Recipes as RM
from Central_UI import Central_UI
from Parameters_Logic import Parameters_Main_Logic
from Attributes_Logic import Attributes_Main_Logic
from Batch_Logic import Batch_Main_Logic
from Structure_Logic import Structure_Main_Logic
import Materials_Recipes as mm
import Par_and_Attr_Updater as IU
from Structure_Recipes import Structure
from Batch_Recipes import Device_Manager
from Batch_Recipes import devices_info
from Par_and_Attr_Recipes import param_path
from Par_and_Attr_Recipes import saved_info
from Server_Logic import Server_Logic
from Initialization_Handler import Initialization_Handler
import Updater as updater
from Devices_Logic import Devices_Main_Logic
from Results_Logic import Results_Main_Logic
import json

version = '1.0.00'

#TODO: Figure out some way to deal with repeat names, probably just reject them
#TODO: Make an option to show all attributes in the attributes window (will take quite a bit of work to ensure proper data allocation)
#TODO: Make a log system for debugging purposes
#TODO: Organize the recipe data storage system, it is poorly organized and nearly unreadable
#TODO: Create a custom style that looks nice
#TODO: Overhaul the existing headers with something cool, the current ones look like trash

class Logic_Main():
    def __init__(self):

        #Creates a property to keep track of the click path
        #Whenever param_path.value is called, all the associated bookkeeping is also preformed (attributes and parameters are updated)


        #Designating the whole central widget as a clickable and trackable area
        ui.centralwidget.setMouseTracking(True)
        ui.centralwidget.mousePressEvent = self.Pressed
        self.Menu_Items()







    #This is 5the parent event handler for anytime the mouse is clicked. All logic is handled elsewheres
    def Pressed(self, event):
        #TODO: maybe replace this to get the sender of the signal somehow?
        select_btn  = ui.centralwidget.childAt(event.pos())
        if str(event.button()) == "PySide2.QtCore.Qt.MouseButton.LeftButton":
            self.Left_Click(select_btn)
        elif str(event.button()) == "PySide2.QtCore.Qt.MouseButton.RightButton":
            self.Right_Click(select_btn, event)



    #Handles all of the left click actions in this app
    def Left_Click(self, select_btn):

        if select_btn.objectName().__contains__("Par"):
            PL.Left_Click(select_btn)
        elif select_btn.objectName().__contains__("Attr"):
            AL.Left_Click(select_btn)
        elif select_btn.objectName().__contains__("Str"):
            SL.Left_Click(select_btn)

    def Right_Click(self, select_btn, event):
        if select_btn.objectName().__contains__("Par"):
            PL.Right_Click(select_btn, event)

        elif select_btn.objectName().__contains__("Attr"):
            AL.Right_Click(select_btn, event)

        elif select_btn.objectName().__contains__("Str"):
            SL.Right_Click(select_btn, event)

    def Change_Mode(self, mode):
        ui.Change_Mode(mode)
        DL.Unload_Devices()

        DL.Load_Devices(BL.devices.info)






    def Menu_Items(self):


        ui.actionExport.triggered.connect(lambda: BL.Export_Recipe())
        ui.actionImport_Devices.triggered.connect(lambda: BL.Import_Devices())
        ui.actionLoad_Default_Materials.triggered.connect(lambda: SL.Load_Default_Materials())
        ui.actionSave_Default_Materials.triggered.connect(lambda: SL.Save_Default_Materials())
        ui.actionLoad_Structure.triggered.connect(lambda: SL.Load_Structure())
        ui.actionSave_Structure.triggered.connect(lambda: SL.Save_Structure())
        ui.actionSet_Selected_Device_Structure.triggered.connect(lambda: BL.Set_Selected_Device_Structure())
        ui.actionSave_All_Device_Data.triggered.connect(lambda: BL.Save_All_Device_Data())
        ui.actionExport_Structure.triggered.connect(lambda: SL.Export_Structure())
        ui.actionQuick_Analysis.triggered.connect(lambda: BL.Quick_Analysis())
        ui.actionSync.triggered.connect(lambda: SVL.Sync())
        ui.actionViewer.triggered.connect(lambda: self.Change_Mode("Viewer"))
        ui.actionImporter.triggered.connect(lambda: self.Change_Mode("Importer"))



if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    #print(QtWidgets.QStyleFactory().keys())

    init = Initialization_Handler(version)
    #This is a loop to hold the program until the initializer window is done
    while not init.Is_Done:
        pass
    #Checks for updates from the server, eventually calls through to the Updater_Manager Class
    init.Check_For_Updates()

    ui = Central_UI()
    rp = RM.Recipe_Manager()
    ST = Structure()
    saved_info.Set_Structure(ST)
    param_path.Set_Structure(ST)
    AL = Attributes_Main_Logic(ui, rp, param_path)
    PL = Parameters_Main_Logic(ui, rp, param_path, AL)
    updater = IU.Info_Filler(AL, PL, param_path)
    mm = mm.Material_Manager(rp, updater)
    SL = Structure_Main_Logic(ui, mm, ST)
    dm = Device_Manager(ST)
    BL = Batch_Main_Logic(ui, dm, SL)
    SVL = Server_Logic(ui, BL)
    RL = Results_Main_Logic(ui)
    DL = Devices_Main_Logic(ui, RL)



    runtime = Logic_Main()


    """Convenience Stuff"""
    #BL.Import_Devices(r'C:\Users\Daniel\Documents\College\Georgia Tech\Research\Codes and More\Device Manager\New Codes\2021-10-13 -- TiO2ALD on spiro\2021-10-13 -- TiO2ALD on spiro')

    sys.exit(app.exec_())
