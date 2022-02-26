from PySide2 import QtCore, QtGui, QtWidgets
global all_batches
import pandas as pd
import os
import tkinter as tk

ui = None

class Results_Main_Logic(object):

    def __init__(self, uix):
        global ui
        ui = uix

    def Pixel_Selected(self, data):
        self.Clear_Graphs()
        light_rv, light_fw, dark_rv, dark_fw = self.Generate_Fw_Rv_JV(data)
        ui.RUI.Create_JV_Plot(light_rv, light_fw, dark_rv, dark_fw)

    def Group_Selected(self, batch_dict):
        self.Clear_Graphs()
        df_to_show = self.Choose_Target_DF(batch_dict, "PCE[%] Rv", "Group")
        ui.RUI.Create_Box_Plot(df_to_show, "Group")

    def None_Selected(self, total_dict):
        df_to_show = self.Choose_Target_DF(total_dict, "PCE[%] Rv", "Total" )
        ui.RUI.Create_Box_Plot(df_to_show, "Total")

    #Convernience function that will sift through a dict and produce a box plottable df for a group or total input
    def Choose_Target_DF(self, dict, target, type):
        if type == "Group":
            target_df = pd.DataFrame()
            for key in dict.keys():
                target_data = dict[key][target]
                target_df[key] = target_data
            target_df = target_df.fillna(0)

        if type == "Total":
            target_df = pd.DataFrame()
            for batch_name in dict.keys():
                batch_df = pd.DataFrame()
                for device_name in dict[batch_name].keys():
                    device_target_df = pd.DataFrame(dict[batch_name][device_name][target].values, columns=[batch_name])
                    device_target_df = device_target_df.fillna(0)
                    batch_df = pd.concat([batch_df, device_target_df], ignore_index=True)

                column_names = list(target_df.columns.values)+[batch_name]
                target_df = pd.concat([target_df, batch_df], ignore_index=True, axis=1)

                target_df.columns = column_names





        return target_df

    def Clear_Graphs(self):
        if hasattr(ui.RUI, 'graph_1'):
            ui.RUI.graph_1.setParent(None)
        if hasattr(ui.RUI, 'graph_2'):
            ui.RUI.graph_2.setParent(None)
        if hasattr(ui.RUI, 'graph_3'):
            ui.RUI.graph_3.setParent(None)
        if hasattr(ui.RUI, 'graph_4'):
            ui.RUI.graph_4.setParent(None)

    def Generate_Fw_Rv_JV(self, data):
        #print(data['Jv Data'].keys())
        #print(data['Jv Data']['Measurements'])
        light_rv, light_fw, dark_rv, dark_fw = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for mes in data['Jv Data']['Measurements']:
            if int(mes['Light Intensity']) == 100:
                if 'Fw' in mes['Sweep'].keys():
                    light_fw = mes['Sweep']['Fw']
                if 'Rv' in mes['Sweep'].keys():
                    light_rv = mes['Sweep']['Rv']

            if int(mes['Light Intensity']) == 0:
                if 'Fw' in mes['Sweep'].keys():
                    dark_fw = mes['Sweep']['Fw']
                if 'Rv' in mes['Sweep'].keys():
                    dark_rv = mes['Sweep']['Rv']

        return light_rv, light_fw, dark_rv, dark_fw
