from PySide2 import QtCore, QtGui, QtWidgets
global all_batches
import pandas as pd
import os
import tkinter as tk

ui, dm, SL = [None, None, None]

class Batch_Main_Logic(object):

    def __init__(self, uix, dmx, SLx):
        global ui, dm, SL
        ui = uix
        dm = dmx
        SL = SLx
        ui.BUI.batch_tree.itemSelectionChanged.connect(lambda: self.Device_Selected())
        self.devices = dm.devices
        self.loaded = False


    def Import_Devices(self, path=None):
        global all_batches

        all_batches = dm.Import_New_Devices(path=path)

        for batch in self.devices.info["Batches"].keys():
            b_parent = ui.BUI.Insert_Item(batch, "Batch", ui.BUI.batch_tree)
            b_parent.status = 0
            for device in self.devices.info["Batches"][batch].keys():
                item = ui.BUI.Insert_Item(device, "Device", b_parent)
                item.status = 0
        for device in self.devices.info["Unsorted Devices"].keys():
            ui.BUI.Insert_Item(device, "Unsorted Device", ui.BUI.batch_tree)

    def Set_Selected_Device_Structure(self):
        structure_path_set = SL.Check_All_Paths_Filled()
        if structure_path_set:
            dm.structure.temp_storage = dm.structure.info
            checked_items = self.Find_Checked()
            unsorted_devices = [x for x in checked_items if x.type == "Unsorted Device"]
            batch_devices = [x for x in checked_items if x.type == "Device"]

            for item in unsorted_devices:
                device = item.text(0)
                dm.Set_Device_Structure_To_Current(device, None)
                ui.BUI.Change_Item_Color(item, "blue")
                item.status = 1
                item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)

            for item in batch_devices:
                batch = item.parent().text(0)
                device = item.text(0)
                dm.Set_Device_Structure_To_Current(device, batch)
                ui.BUI.Change_Item_Color(item, "blue")
                item.status = 1
                item.setCheckState(0, QtCore.Qt.CheckState.Unchecked)
            self.Manual_Autotristation()
            self.Unselect_All()
        else:
            pass

    #This returns a list of all checked items in the batch tree viewer
    def Find_Checked(self):
        checked = []
        root = ui.BUI.batch_tree.invisibleRootItem()

        for i in range(root.childCount()):
            top_item = root.child(i)
            #This catches the unsorted devices
            if top_item.childCount() == 0:
                if top_item.checkState(0) == QtCore.Qt.Checked:
                    checked += [top_item]
            elif top_item.childCount() > 0:
                #This segment catches the devices inside a batch
                for g in range(top_item.childCount()):
                    child = top_item.child(g)
                    if child.checkState(0) == QtCore.Qt.Checked:
                        checked += [child]
                #This line catches all of the batches
                if top_item.checkState(0) == QtCore.Qt.Checked:
                    checked += [top_item]

        return(checked)

    #This function returns a list of the info's of all checked devices
    def Return_Checked_Info(self):

        checked_items = self.Find_Checked()

        all_set_with_structures = True
        for item in [x for x in checked_items if x.type == "Unsorted Device" or x.type == "Device"]:
            print(item.status)
            if item.status == 0:
                all_set_with_structures = False

        if all_set_with_structures == False:
            dialog_box = ui.Show_Dialog("Device Structure Error", "Please ensure that the structures of all devices being synced have already been set. Database sync has been aborted")
            dialog_box.exec()
            return False


        unsorted_devices = [x for x in checked_items if x.type == "Unsorted Device"]
        batch_devices = [x for x in checked_items if x.type == "Device"]

        devices_info = pd.DataFrame(columns = ['Name', 'Batch', 'Data'])

        for item in unsorted_devices:
            device = item.text(0)
            batch = "Unsorted"
            device_data = dm.devices.Return_Device_Info(device, None)
            devices_info = devices_info.append(pd.DataFrame([[device, batch, device_data]], columns = ['Name', 'Batch', 'Data']), ignore_index=True)

        for item in batch_devices:
            batch = item.parent().text(0)
            device = item.text(0)
            device_data = dm.devices.Return_Device_Info(device, batch)
            devices_info = devices_info.append(pd.DataFrame([[device, batch, device_data]], columns = ['Name', 'Batch', 'Data']), ignore_index=True)


        self.Manual_Autotristation()
        self.Unselect_All()

        return devices_info, checked_items



    def Manual_Autotristation(self):
        root = ui.BUI.batch_tree.invisibleRootItem()
        for i in range(root.childCount()):
            top_item = root.child(i)
            count = 0
            statuses = []
            if top_item.childCount() > 0:
                #This segment catches the devices inside a batch
                for g in range(top_item.childCount()):
                    child = top_item.child(g)
                    statuses += [child.status]

                if all(status == 1 for status in statuses):
                    ui.BUI.Change_Item_Color(top_item, "blue")
                elif all(status == 2 for status in statuses):
                    ui.BUI.Change_Item_Color(top_item, "green")

    def Save_All_Device_Data(self):

        result = dm.Save_All_Device_Data()
        if result:
            print("Save completed successfully")
        else:
            print("Save operation failed")

    def Load_Device_Data(self):
        pass

    def Unselect_All(self):
        item_list = ui.BUI.batch_tree.selectedItems()
        for item in item_list:
            item.setSelected(False)

    def Device_Selected(self):
        selection = ui.BUI.batch_tree.selectedItems()
        #This feature is giving me some trouble, excluding it for now
        if len(selection) == 0:
            pass
            """
            SL.Set_and_Show_Structure(dm.structure.temp_storage)
            """
        else:
            """
            print(selection[0].status)
            item = selection[0]
            if item.status == 1 or item.status == 2:
                if item.type == "Unsorted Device":
                    print("ok bro")
                elif item.type == "Device":
                    device = item.text(0)

                    batch = item.parent().text(0)
                    print("device: " + device + ",  Batch: " + batch)
                    structure_info = dm.devices.Return_Structure_Info(device, batch)
                    SL.Set_and_Show_Structure(structure_info)

            elif item.status == 0:
                SL.Set_and_Show_Structure(dm.structure.temp_storage)
            """


    """
    This function save a summary of your devices to a specific directory as a CSV
    TODO: Make this function more powerful, maybe a secondary window


    """
    def Quick_Analysis(self):
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        try:
            filename = tk.filedialog.asksaveasfilename(initialdir = save_dir, title = "Save Device Summary", filetypes = (("CSV", "*.csv*"), ("All files", "*.*")))
            if not filename:
                print("Quick Analysis Aborted")
                return False
            elif (filename[-4:] != '.csv'):
                filename = filename + '.csv'
        except:
            print("Quick Analysis Aborted")
            return False



        try:
            #Collecting the devices' info from the Structure ST.info object

            devices_data = self.Return_Devices_Info()

            devices_data.to_csv(filename, index=False)

        except Exception as error:
            print("Quick Analysis failed with error message: {}".format(error))


    """
    This function will take every device in the batch window, its parameters, and its structure,
    and export it to a csv.

    Does this function belong in this file? maybe...

    """


    def Export_Recipe(self):

        all_info = self.Return_All_Info()
        dm.Export_Recipe(all_info)


    """
    Returns a dataframe with specified (in function) device parameters that is compatible for csv exporting
    """
    def Return_Devices_Info(self):
        batches = self.devices.info['Batches']
        unsorted_devices = self.devices.info['Unsorted Devices']
        column_headers = ['Batch', 'Device', 'Pixel', 'Scan', 'PCE[%] Rv', 'PCE[%] Fw', 'Voc[V] Rv',
                            'Voc[V] Fw', 'FF[%] Rv', 'FF[%] Fw', 'Jsc[mA/cm2] Rv',
                            'Jsc[mA/cm2] Fw', 'Stabilized_MPP [%]']

        devices_data = pd.DataFrame(columns=column_headers)
        for b_name in batches.keys():
            batch = batches[b_name]
            for d_name in batch.keys():
                device = batch[d_name]
                for p_name in device.keys():
                    if p_name.__contains__('pixel'):
                        pixel = device[p_name]
                        storage_indexes = ['Scan number','PCE[%] Rv', 'PCE[%] Fw', 'Voc[V] Rv',
                                        'Voc[V] Fw', 'FF[%] Rv', 'FF[%] Fw', 'Jsc[mA/cm2] Rv',
                                        'Jsc[mA/cm2] Fw', 'Stabilized_MPP [%]']

                        extracted_data = [pixel[index] for index in storage_indexes]

                        data_to_insert = pd.Series([b_name, d_name, p_name] + extracted_data, index=devices_data.columns)
                        devices_data = devices_data.append(data_to_insert, ignore_index=True)

            for d_name in unsorted_devices.keys():
                device = unsorted_devices[d_name]
                for p_name in device.keys():
                    if p_name.__contains__('pixel'):
                        pixel = device[p_name]
                        storage_indexes = ['Scan number','PCE[%] Rv', 'PCE[%] Fw', 'Voc[V] Rv',
                        'Voc[V] Fw', 'FF[%] Rv', 'FF[%] Fw', 'Jsc[mA/cm2] Rv',
                                        'Jsc[mA/cm2] Fw', 'Stabilized_MPP [%]']
                        extracted_data = [pixel[index] for index in storage_indexes]

                        data_to_insert = pd.Series(['NONE', d_name, p_name] + extracted_data, index=devices_data.columns)
                        devices_data = devices_data.append(data_to_insert, ignore_index=True)
        return devices_data


    """
    Returns a DataFrame with linearized data for every pixel in the batch window with its according structural information

    """

    def Return_All_Info(self):
        final_columns = ['Variable', 'Value']

        devices_df = self.Return_Devices_Info()
        final_df = pd.DataFrame()

        for index, pixel in devices_df.iterrows():
            #print(row.reset_index(inplace=True))
            pixel_variables = pixel.keys().tolist()
            pixel_values = pixel.values.tolist()

            pixel_df = pd.DataFrame(list(zip(pixel_variables, pixel_values)), columns=final_columns   )
            batch = pixel['Batch']
            device = pixel['Device']

            structure_info = self.devices.info['Batches'][batch][device]['Structure']

            linear_structure_array = SL.Linearize_Structure_Array(SL.Generate_Structure_Array(structure_info))

            pixel_df = pixel_df.append(linear_structure_array, ignore_index=True)


            columns = final_df.columns.values.tolist() + pixel_df.columns.values.tolist()


            final_df = pd.concat([final_df, pixel_df], ignore_index=True, axis=1)
            final_df = final_df.set_axis(columns, axis=1)


        return final_df

    def Load_Devices(self, info):
        global all_batches
        all_batches = info

        for batch in self.devices.info["Batches"].keys():
            b_parent = ui.BUI.Insert_Item(batch, "Batch", ui.BUI.batch_tree)
            b_parent.status = 0
            for device in self.devices.info["Batches"][batch].keys():
                item = ui.BUI.Insert_Item(device, "Device", b_parent)
                item.status = 0
        for device in self.devices.info["Unsorted Devices"].keys():
            ui.BUI.Insert_Item(device, "Unsorted Device", ui.BUI.batch_tree)
