from PySide2 import QtCore, QtGui, QtWidgets
import traceback

ui, rp, param_path = [None, None, None]



class Attributes_Main_Logic(object):

    def __init__(self, uix, rpx, param_pathx):
        global ui, rp, param_path
        ui = uix
        rp = rpx
        param_path = param_pathx

        self.current_pos = ui.AUI.viewer

        ui.AUI.viewer.itemChanged.connect(self.Attr_and_Group_Creation)
        ui.AUI.viewer.itemSelectionChanged.connect(self.Selected)
        ui.AUI.viewer.customContextMenuRequested.connect(self.Context_Menu_Link)


    def Fill_Attrs(self):
        self.Clear_Attr_Window()
        try:
            if not param_path.attributes:
                raise TypeError("No attributes")
            else:
                try:
                    self.Clear_Attr_Window()
                except:
                    ui.AUI.Create_Tree_Viewer()



                count = 0
                self.current_pos = ui.AUI.viewer
                for attr in param_path.attributes.keys():
                    value = param_path.attributes[attr]


                    if str(type(value)) == "<class 'str'>": #Case if the parameter is a attribute
                        ui.AUI.Insert_Item(attr, value, "Attr", self.current_pos)
                    elif str(type(param_path.attributes[attr])) == "<class 'dict'>":    #Case if this is an group
                        item = ui.AUI.Insert_Item(attr, "", "Group", self.current_pos)
                        print(item.text(0))
                        self.Group_Filling(param_path.attributes[attr], item)
                    else:
                        pass
                    count = count+1

                param_path.attributes = []
                ui.AUI.viewer.collapseAll()

        except Exception as e:
            print(traceback.format_exc())
            if not ui.AUI.viewer:
                #There is only one grid for the attribute window, and there will never be any more, so says I
                ui.AUI.Create_Tree_Viewer()


            elif ui.AUI.viewer:
                self.Clear_Attr_Window()



    def Group_Filling(self, group, parent):
        for key in group.keys():
            if str(type(group[key])) == "<class 'str'>":
                ui.AUI.Insert_Item(key, group[key], "Attr", parent)
            elif str(type(group[key])) == "<class 'dict'>":
                item = ui.AUI.Insert_Item(key, "", "Group", parent)
                self.Group_Filling(group[key], item)
            else:
                pass

    #Deletes Everything on the attribute window
    def Clear_Attr_Window(self):
        ui.AUI.viewer.clear()

    def Selected(self):
        item = ui.AUI.viewer.selectedItems()
        print(item[0].path)
        if item:
            self.current_pos = item[-1]
            #ui.AUI.viewer.setCurrentItem([item])
        elif not item:
            self.current_pos = ui.AUI.viewer

    #A Slightly modified reimplementation of Parameter_Creation for attributes
    def Attr_and_Group_Creation(self, item, col):
        try:
            if (item.type == "Attr"):
                attr = item
                if (not attr.previous_name) and (attr.text(0) != "Enter Name"):
                    rp.Attribute_Init(attr.text(0), attr.text(1), attr.path)
                    attr.previous_name = attr.text(0)
                elif (attr.previous_name is not None) and (attr.text(0) != attr.previous_name):
                    rp.Rename_Attribute(attr.previous_name, attr.text(0), attr.path)
                elif (attr.previous_name is not None) and (attr.text(0) == attr.previous_name):
                    rp.Attribute_Init(attr.text(0), attr.text(1), attr.path)

                if (attr.text(0) != "Enter Name") and (col == 0):
                    font = attr.font(0)
                    font.setItalic(False)
                    attr.setFont(0, font)
                elif (col == 1) and (attr.text(1) != "Enter Value"):
                    font = attr.font(1)
                    font.setItalic(False)
                    attr.setFont(1, font)

            elif (item.type == "Group") :
                group = item
                if (not group.previous_name) and (group.text(0) != "Enter Name"):
                    rp.Group_Init(group.text(0), group.path)
                    group.previous_name = group.text(0)
                elif (group.previous_name is not None) and (group.text(0) != group.previous_name):
                    rp.Rename_Attribute(group.previous_name, group.text(0), group.path)
                elif (group.previous_name is not None) and (group.text(0) == group.previous_name):
                    rp.Group_Init(group.text(0), group.path)

                if (group.text(0) != "Enter Group") and (col == 0):
                    font = group.font(0)
                    font.setItalic(False)
                    group.setFont(0, font)


        except Exception as e:
            print(e)

    def Delete(self):
        item = ui.AUI.viewer.selectedItems()[-1]
        path = item.path
        name = item.text(0)
        rp.Delete_Attribute(name, path)
        self.Fill_Attrs()

    #Left Click handler for the attribute window. Whenever the window is disabled (no layer/material is selected),
    # all left clicks are ignored
    def Left_Click(self, select_btn):

        if (select_btn.objectName() == "Add@Attr_Variable") & ui.attribute_viewer.isEnabled():

            if (hasattr(self.current_pos, 'type')):          #Checking to make sure that the currently selected item is a group
                if (self.current_pos.type == "Group"):
                    self.Add_Variable()
            else:
                self.Add_Variable()
        elif (select_btn.objectName() == "Add@Attr_Group") & ui.attribute_viewer.isEnabled():
            if (hasattr(self.current_pos, 'type')):          #Checking to make sure that the currently selected item is a group
                if (self.current_pos.type == "Group"):
                    self.Add_Group()
            else:
                self.Add_Group()


    def Right_Click(self, select_btn, event):

        if select_btn.objectName().__contains__("AttrV@"):
            ui.AUI.Context_Menu(select_btn, event)

            try:
                ui.AUI.actionDelete.triggered.connect(lambda: self.Delete(ui.AUI.actionDelete.trigger))
            except Exception as e:
                print(["Context Menu Action Failed with log:" + e])

    def Add_Variable(self):
        parent = self.current_pos
        attr = ui.AUI.Insert_Item("Enter Name", "Enter Value", "Attr", parent)
        special_font = QtGui.QFont()
        special_font.setWeight(5)
        special_font.setItalic(True)

        attr.setFont(0, special_font)
        attr.setFont(1, special_font)

    def Add_Group(self):
        parent = self.current_pos
        attr = ui.AUI.Insert_Item("Enter Group", "", "Group", parent)
        special_font = QtGui.QFont()
        special_font.setWeight(5)
        special_font.setItalic(True)

        attr.setFont(0, special_font)
        attr.setFont(1, special_font)

    """
    This function acts as a central handler for the creation of a context menu whenever the tree widget is right-clicked
    It is able to figure out if it was an item that had been right clicked or not and will set up all of the signal-slot
        connections for the context menu's actions
    If you want to start adding more menu options, first add them in Attributes_UI, Context_Menu function
    """
    def Context_Menu_Link(self, point):
        point = ui.AUI.viewer.mapToGlobal(point)
        item = ui.AUI.viewer.selectedItems()

        if item:
            item = item[-1]

            ui.AUI.Context_Menu(point, ui.MainWindow)
            ui.AUI.actionDelete.triggered.connect(lambda item: self.Delete())
