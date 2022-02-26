from PySide2 import QtCore, QtGui, QtWidgets
global all_batches
import pandas as pd
import os
import tkinter as tk

ui, RL = [None, None]

class Devices_Main_Logic(object):

    def __init__(self, uix, RLx):
        global ui
        global RL
        ui = uix
        RL = RLx
        self.info = None
        ui.DUI.devices_tree.itemSelectionChanged.connect(self.Item_Selected)


    def Load_Devices(self, info):
        self.info = info

        for batch in self.info["Batches"].keys():
            b_parent = ui.DUI.Insert_Item(batch, "Group", ui.DUI.devices_tree)
            b_parent.info = self.info['Batches'][batch]
            for device in self.info["Batches"][batch].keys():
                item = ui.DUI.Insert_Item(device, "Device", b_parent)
                item.info = self.info['Batches'][batch][device]
                for pixel in self.info['Batches'][batch][device].keys():
                    item_p = ui.DUI.Insert_Item(pixel, "Pixel", item)
                    item_p.info = self.info['Batches'][batch][device][pixel]

        for device in self.info["Unsorted Devices"].keys():
            item = ui.BUI.Insert_Item(device, "Unsorted Device", ui.DUI.devices_tree)
            item.info = self.info["Unsorted Devices"][device]

        ui.DUI.devices_tree.clearSelection()
        self.Item_Selected()

    def Unload_Devices(self):
        self.info = None
        ui.DUI.devices_tree.clear()

    def Item_Selected(self):
        RL.Clear_Graphs()

        if len(ui.DUI.devices_tree.selectedItems()) >= 1:
            selected_item = ui.DUI.devices_tree.selectedItems()[0]

            if selected_item.type == "Pixel":
                #print(selected_item.info)
                RL.Pixel_Selected(selected_item.info)

            if selected_item.type == "Device":
                device_df = self.Generate_Device_DF(selected_item.info)
                for item in ['Jsc[mA/cm2] Rv',
                'Jsc[mA/cm2] Fw', 'Voc[V] Rv', 'Voc[V] Fw', 'FF[%] Rv', 'FF[%] Fw', 'Stabilized_MPP [%]']:

                    device_df = device_df.drop(item, axis=1)
                ui.RUI.Create_Bar_Graph(device_df, "Device")

            if selected_item.type == "Group":
                batch_dict = self.Generate_Batch_Dict(selected_item.info)
                RL.Group_Selected(batch_dict)



        else:
            total_dict = self.Generate_Total_Dict()
            RL.None_Selected(total_dict)


    def Generate_Device_DF(self, data):
        device_df = pd.DataFrame()
        for key in data.keys():
            if key.__contains__("pixel"):
                pixel_data = data[key]
                pixel_df = pd.DataFrame([[pixel_data['PCE[%] Rv'], pixel_data['PCE[%] Fw'],
                    pixel_data['Jsc[mA/cm2] Rv'], pixel_data['Jsc[mA/cm2] Fw'],
                    pixel_data['Voc[V] Rv'], pixel_data['Voc[V] Fw'],
                    pixel_data['FF[%] Rv'], pixel_data['FF[%] Fw'],
                    pixel_data['Stabilized_MPP [%]']]], columns = ['PCE[%] Rv', 'PCE[%] Fw', 'Jsc[mA/cm2] Rv',
                    'Jsc[mA/cm2] Fw', 'Voc[V] Rv', 'Voc[V] Fw', 'FF[%] Rv', 'FF[%] Fw', 'Stabilized_MPP [%]'],
                    index=[key])
                device_df = device_df.append(pixel_df)
        device_df = device_df.fillna(0)
        return device_df

    #Generates a dict with devices as keys and device_dfs as attributes for each device in a batche
    #Takes the batch_df (found in the tree item .info attribute, or nested within self.info) as an input
    def Generate_Batch_Dict(self, batch_data):
        batch_dict = {}
        for device in batch_data.keys():
            device_data = batch_data[device]
            device_df = self.Generate_Device_DF(device_data)
            batch_dict[device] = device_df

        return batch_dict



    def Generate_Total_Dict(self):
        total_dict = {}
        for batch_name in self.info["Batches"].keys():
            batch_dict = self.Generate_Batch_Dict(self.info['Batches'][batch_name])
            total_dict[batch_name] = batch_dict


        return total_dict
