ui, mm = [None, None]
import numpy as np
import pandas as pd


class Structure_Main_Logic(object):
    def __init__(self, uix, mmx, ST):
        global ui, mm
        ui = uix
        mm = mmx
        self.selected_layer = None
        self.ST = ST
        mm.Initialize_Materials()
        self.Enable_AP_Recipes(False)
        self.Connect_Context_Actions()


    def Left_Click(self, select_btn):
        if select_btn.objectName() == "Add@Str_L":
            layer = self.Add_Layer()
            self.Fill_Materials(layer)
        elif select_btn.objectName().__contains__("Str@Layer"):
            self.Layer_Selected(select_btn)
        elif select_btn.objectName() == "Str@Block":
            select_btn = select_btn.parent()
            print(select_btn.objectName())
            self.Layer_Selected(select_btn)
        else:
            print("unknown structure object")
            print(select_btn)

    def Right_Click(self, select_btn, event):
        if select_btn.objectName().__contains__("Str@Layer"):
            if not select_btn == self.selected_layer:
                self.Layer_Selected(select_btn)
        elif select_btn.objectName() == "Str@Block":
            select_btn = select_btn.parent()
            if not select_btn == self.selected_layer:
                self.Layer_Selected(select_btn)


    def Add_Layer(self):
        layer = ui.SUI.Insert_New_Layer()
        self.ST.Add_Top_Layer()
        if self.selected_layer:
            ui.structure_viewer.focus_box.setParent(None)
            self.selected_layer = None
            self.Select_Material(None)
        return layer

    def Layer_Selected(self, layer):
        if layer:
            material = layer.material_edit.text()


        if not self.selected_layer:
            self.selected_layer = layer
            self.ST.current_layer_num = layer.num
            self.ST.current_layer_material = layer.material
            #drawing focus box around layer
            ui.SUI.Create_Focus_Box(layer)

            self.Select_Material(layer)

        else:
            if (layer == self.selected_layer) | (not layer):
                self.selected_layer = None
                self.ST.current_layer_num = None
                self.ST.current_layer_material = None
                ui.structure_viewer.focus_box.setParent(None)
                self.Select_Material(None)
            else:
                self.selected_layer = layer
                self.ST.current_layer_num = layer.num
                self.ST.current_layer_material = layer.material
                ui.structure_viewer.focus_box.setParent(None)
                ui.SUI.Create_Focus_Box(layer)
                self.Select_Material(layer)

    def Fill_Materials(self, layer):
        materials = mm.Return_Materials()
        #Destroying a menu in case it already exists
        if layer.material_edit.menu():
            layer.material_edit.menu().setParent(None)
        for mat in materials:
            ui.SUI.Add_Material_Menu_Item(mat, layer)
        ui.SUI.Add_Material_Menu_Item("Add Material", layer)

        # Spent many hours in these couple of lines
        # It turns out lambda makes a sort of mini-function, so to preserve the text info
        # for materials when I was connecting the triggered signals I had to define them within the lamda,
        # otherwise the values would not be stored, now I know haha
        for action in layer.material_edit.menu().actions():
            if action.text() == "Add Material":
                action.triggered.connect(lambda: self.Add_Material())
            elif action.text() != "Add Material":
                text = action.text()
                action.triggered.connect(lambda text=text, layer=layer: self.Assign_Material(text, layer))

    def Add_Material(self):
        popup = ui.SUI.Popup_Material_Edit()
        popup.bt_cancel.clicked.connect(lambda: self.Popup_Material_Events("close", popup))
        popup.bt_enter.clicked.connect(lambda: self.Popup_Material_Events("enter", popup))
        popup.exec()

    def Popup_Material_Events(self, type, window):
        if type == "close":
            window.done(0)
        elif type == "enter":
            mm.Create_Material(window.t_e.text())
            window.done(1)
            self.Fill_All_Materials()

    def Fill_All_Materials(self):
        for layer in ui.SUI.layers:
            self.Fill_Materials(layer)

    def Assign_Material(self, material, layer):
        layer.material_edit.setText(material)
        layer.material = material
        info = mm.Load_Material(material)
        self.ST.Set_Layer_Material(layer.material, layer.num)
        self.ST.info[layer.num][layer.material] = info
        if layer == self.selected_layer:
            self.Select_Material(layer)


    def Select_Material(self, layer):

        if (not layer)  :
            mm.Set_Existing_Material_Info(None, [])
            self.Enable_AP_Recipes(False)
        elif (layer.material) :
            info = self.ST.info[layer.num][layer.material]
            path = self.ST.info[layer.num]["Path"]
            mm.Set_Existing_Material_Info(info, path)
            self.Enable_AP_Recipes(True)
        elif (not self.ST.info[layer.num]):
            mm.Set_Existing_Material_Info(None, [])
            self.Enable_AP_Recipes(False)



    def Load_Default_Materials(self):
        mm.Load_Default_Materials()
        self.Fill_All_Materials()

    def Save_Default_Materials(self):
        #TODO: Insert a popup warning here
        mm.Save_Default_Materials(self.ST)

    #TODO: Maybe add a tooltip or message on these windows that the material has not been selected
    def Enable_AP_Recipes(self, bool):

        ui.attribute_viewer.setEnabled(bool)
        ui.parameter_viewer.setEnabled(bool)

        for child in ui.parameter_viewer.children():
            if child.objectName().__contains__("frame"):
                child.setVisible(bool)

    def Clear_Structure_Window(self):
        self.selected_layer = None
        self.ST.current_layer_num = None
        self.ST.current_layer_material = None
        if hasattr(ui.structure_viewer, "focus_box"):
            ui.structure_viewer.focus_box.setParent(None)
        frame = ui.SUI.frame
        for child in frame.children():
            child.setParent(None)
        ui.SUI.layers = []

    def Load_Structure(self):
        self.Clear_Structure_Window()
        info = self.ST.Load_Structure()
        if info:
            for layer_info in info:
                material = [key for key in layer_info.keys() if key != "Path"][-1]
                layer = ui.SUI.Insert_New_Layer()
                layer.material_edit.setText(material)
                layer.material = material
            self.Fill_All_Materials()

        ui.SUI.frame.adjustSize()

    def Set_and_Show_Structure(self, structure_info):
        self.Clear_Structure_Window()
        self.ST.info = structure_info
        if structure_info:
            for layer_info in structure_info:
                material = [key for key in layer_info.keys() if key != "Path"][-1]
                layer = ui.SUI.Insert_New_Layer()
                layer.material_edit.setText(material)
                layer.material = material
                self.Enable_AP_Recipes(False)
                mm.updater.Clear_Par_and_Attr()
        else:
            #TODO: This case may never be necessary, but put in a null handler as well
            pass

    def Save_Structure(self):
        #TODO: Maybe add in a warning dialog HERE
        self.ST.Save_Structure()

    """
    This function is the primary logic handler for the Export Structure action under the Structures menu
    It will first check to see that all paths in the structure are set, and if not, will return an error dialog
    If all paths are set, then it will generate as csv-friendly format for the structure, and save it
    """
    def Export_Structure(self):

        all_paths_filled = True

        for i in range(0,len(self.ST.info)):

            material = ui.SUI.layers[i].material
            path = self.ST.info[i]["Path"]
            if len(path) == 0:
                last_path = "@@primary"
            else:
                last_path = path[-1]

            info = self.ST.info[i][material][last_path]

            if "Parameters" in info and len(info["Parameters"]) > 0:
                all_paths_filled = False

        if all_paths_filled:
            array = self.Generate_Structure_Array()
            self.ST.Export_Structure(array)

        else:
            ui.SUI.Raise_Error_Dialog("""Not all layers have been assigned a full fabrication path.
                                        Please selects all paths and try again.""")
    def Return_Structure_Info(self):
        all_paths_filled = self.Check_All_Paths_Filled()

        if all_paths_filled:
            array = self.Generate_Structure_Array()
            self.ST.Export_Structure(array)

        else:
            ui.SUI.Raise_Error_Dialog("""Not all layers have been assigned a full fabrication path.
                                        Please selects all paths and try again.""")

    def Check_All_Paths_Filled(self):
        all_paths_filled = True

        for i in range(0,len(self.ST.info)):

            material = ui.SUI.layers[i].material
            path = self.ST.info[i]["Path"]
            if len(path) == 0:
                last_path = "@@primary"
            else:
                last_path = path[-1]

            info = self.ST.info[i][material][last_path]

            if "Parameters" in info and len(info["Parameters"]) > 0:
                all_paths_filled = False

        if all_paths_filled:
            return True

        else:
            return False



    """
    Deprecated function, replaced by Return_Structure_Info
    This function takes the current structure and formats it so that it can be saved as a CSV
    The first row is layer name, and the second to variable names
    The first column of every layer is for the fabrication path, and is labelled accordingly
    Group Names are added to the variable name (if applicable) in the format [group - variable]
    """
    """
    def Generate_Structure_Array(self):
        full_info = np.array([["Structure", ""]])
        all_layers = np.array([[""]])
        print(self.ST.info)
        for layer in ui.SUI.layers:
            material = layer.material
            info = self.ST.info[layer.num][layer.material]
            path = ["@@primary"]+self.ST.info[layer.num]["Path"]
            layer_info = np.array([[str(layer.num), material]])
            step_info = np.array([[]])
            for step in path:
                if "Attributes" in info[step]:
                    data = info[step]["Attributes"]
                    array = np.array([[step, ""],["",""]])
                    list = self.Find_All_Variables(data, "", "", array)
                else:
                    list = np.array([[step, ""]])

                #Makes sure that the concatenated arrays have the same number of columns
                if step_info.shape[0] > list.shape[0]:
                    needed_rows = step_info.shape[0] - list.shape[0]
                    expanded = np.full([needed_rows, list.shape[1]], "")
                    list = np.concatenate((list, expanded), 0)
                else:
                    needed_rows = list.shape[0] - step_info.shape[0]
                    expanded = np.full([needed_rows, step_info.shape[1]], "")
                    step_info = np.concatenate((step_info, expanded), 0)

                step_info = np.concatenate((step_info, list), 1)


                if step_info.shape[1] > layer_info.shape[1]:
                    needed_columns = int(step_info.shape[1] - layer_info.shape[1])
                    expanded = np.full([layer_info.shape[0], needed_columns], "")
                    layer_info = np.concatenate((layer_info, expanded), 1)

                layer_info = np.concatenate((layer_info, step_info), 0)


            if layer_info.shape[0] > all_layers.shape[0]:
                needed_rows = layer_info.shape[0] - all_layers.shape[0]
                expanded = np.full([needed_rows, all_layers.shape[1]], "")
                all_layers = np.concatenate((all_layers, expanded), 0)
            else:
                needed_rows = all_layers.shape[0] - layer_info.shape[0]
                expanded = np.full([needed_rows, layer_info.shape[1]], "")
                layer_info = np.concatenate((layer_info, expanded), 0)

            all_layers = np.concatenate((all_layers, layer_info), 1)


        if all_layers.shape[1] > full_info.shape[1]:
            needed_columns = int(all_layers.shape[1] - full_info.shape[1])
            expanded = np.full([full_info.shape[0], needed_columns], "")
            full_info = np.concatenate((full_info, expanded), 1)

        full_info = np.concatenate((full_info, all_layers), 0)

        return full_info
    """

    #If you specify an argument (structure.info object), it returns an array for that
    #If not, returns the current structure array
    def Generate_Structure_Array(self, structure_info=None):
        all_layers_info = pd.DataFrame()
        layer_count = 1;

        if structure_info==None:
            structure_info = self.ST.info
            print("There was no structure...")

        for layer in structure_info:
            layer_df = pd.DataFrame()

            layer_var_header = 'Layer {}'.format(layer_count) +' - Variable'
            layer_val_header = 'Layer {}'.format(layer_count) +' - Value'
            material = [key for key in layer.keys() if key != 'Path'][0]


            #TODO: Something for materials
            if material == '@@Treatment':

                print("Please do something else")


            else:

                material_df = pd.DataFrame([['Material', material]], columns = [layer_var_header, layer_val_header])
                layer_df = layer_df.append(material_df, ignore_index=True)

                path = layer['Path']
                path_var = ''
                for par in path:
                    if path_var:
                        path_var = path_var + '.' + par
                    else:
                        path_var = par

                    atr = layer[material][par]

                    if "Attributes" in atr:

                        data = atr["Attributes"]
                        array = np.array([[par, ""],["",""]])
                        #Remember to insert self below
                        list = self.Find_All_Variables(data, "", "", array)
                        for row in list:
                            if row[1]:
                                variable = path_var + '_' + row[0]
                                value = row[1]
                                row_df = pd.DataFrame([[variable, value]], columns = [layer_var_header, layer_val_header])
                                layer_df = layer_df.append(row_df, ignore_index=True)


                path_df = pd.DataFrame([['Path', path_var]], columns = [layer_var_header, layer_val_header])
                layer_df = layer_df.append(path_df, ignore_index=True)



            columns = all_layers_info.columns.values.tolist() + layer_df.columns.values.tolist()


            all_layers_info = pd.concat([all_layers_info, layer_df], ignore_index=True, axis=1)
            all_layers_info = all_layers_info.set_axis(columns, axis=1)

            layer_count +=1

        return all_layers_info

    def Linearize_Structure_Array(self, array):

        new_columns = ['Variable', 'Value']
        array_columns = array.columns.values.tolist()
        new_array = pd.DataFrame()
        layer_temp_item = []
        last_layer = ''
        for column in array_columns:
            parts = column.split(' - ')
            layer_name = parts[0]

            if last_layer != layer_name:
                layer_temp_item = [array[column].values.tolist()]

                for i in range(len(layer_temp_item[0])-1):
                    if type(layer_temp_item[0][i]) != float:
                        layer_temp_item[0][i] = layer_name + '_' + layer_temp_item[0][i]
            else:
                layer_temp_item = layer_temp_item + [array[column].values.tolist()]
                new_array = new_array.append(pd.DataFrame(list(zip(layer_temp_item[0], layer_temp_item[1])), columns=new_columns), ignore_index=True)

            last_layer = layer_name
        new_array = new_array.dropna(how='any')
        return new_array



    def Find_All_Variables(self, info, key, group_path, array):

        if key == "":
            for key in info.keys():
                array = self.Find_All_Variables(info[key], key, "", array)

        elif str(type(info)) == "<class 'str'>":
            full_name = group_path + key
            value = info

            array = np.concatenate((array, np.array([[full_name, value]])))

        elif str(type(info)) == "<class 'dict'>":
            group_path = group_path + str(key) + ".."
            for key in info.keys():
                array = self.Find_All_Variables(info[key], key, group_path, array)

        return array





    """
    This is just a self-referencing recursive class to help look through attribute data structures
    """
    def Find_All_Variables(self, info, key, group_path, array):

        if key == "":
            for key in info.keys():
                array = self.Find_All_Variables(info[key], key, "", array)

        elif str(type(info)) == "<class 'str'>":
            full_name = group_path + key
            value = info

            array = np.concatenate((array, np.array([[full_name, value]])))

        elif str(type(info)) == "<class 'dict'>":
            group_path = group_path + str(key) + " - "
            for key in info.keys():
                array = self.Find_All_Variables(info[key], key, group_path, array)

        return array

    def Insert_Above(self):

        pos = self.selected_layer.pos()
        target_num = self.selected_layer.num + 1
        for layer in ui.SUI.layers:
            if int(layer.num) >= int(target_num):
                #print("kkk")
                layer.num += 1
                layer.setObjectName(layer.objectName()[:-1] + str(int(layer.objectName()[-1])+1))
                #print(layer.num)
                #print(layer.objectName())
                #print(self.ST.info)

        self.ST.info.insert(target_num, {})
        #print([layer.keys() for layer in self.ST.info])
        created_layer = ui.SUI.Insert_New_Layer(target_num)
        ui.SUI.layers.insert(target_num, created_layer)

        self.Layer_Selected(self.selected_layer)

        self.Fill_All_Materials()
        ui.SUI.Set_Layer_Positions()
        ui.SUI.frame.adjustSize()


    def Insert_Below(self):

        pos = self.selected_layer.pos()
        target_num = self.selected_layer.num

        for layer in ui.SUI.layers:
            if int(layer.num) >= int(target_num):
                layer.num += 1

                layer.setObjectName(layer.objectName()[:-1] + str(int(layer.objectName()[-1])+1)  )


        self.ST.info.insert(target_num, {})
        #print([layer.keys() for layer in self.ST.info])
        created_layer = ui.SUI.Insert_New_Layer(target_num)
        ui.SUI.layers.insert(target_num, created_layer)

        self.Layer_Selected(self.selected_layer)


        self.Fill_All_Materials()
        ui.SUI.Set_Layer_Positions()
        ui.SUI.frame.adjustSize()




    def Delete(self):

        pos = self.selected_layer.pos()
        target_num = self.selected_layer.num
        layers = ui.SUI.layers
        target_layer = self.selected_layer

        self.Layer_Selected(None)
        #print(len(self.ST.info))
        self.ST.info.pop(target_num)

        ui.SUI.layers.pop(target_num)

        target_layer.hide()



        for layer in layers:
            if layer.num > target_num:
                layer.num -= 1
                layer.setObjectName(layer.objectName()[:-1] + str(int(layer.objectName()[-1])-1))






        self.Fill_All_Materials()
        ui.SUI.Set_Layer_Positions()
        ui.SUI.frame.adjustSize()


    def Connect_Context_Actions(self):
        ui.SUI.insert_layer_above.triggered.connect(self.Insert_Above)
        ui.SUI.insert_layer_below.triggered.connect(self.Insert_Below)
        ui.SUI.delete_layer.triggered.connect(self.Delete)
