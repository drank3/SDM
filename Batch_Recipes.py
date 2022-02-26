import tkinter as tk
from tkinter import filedialog
import csv
import json
import os
import JV_Importer as jvimp
import datetime
import numpy
import copy




#This class is primarily a data storage object, and as such, I've tried to keep is as simple as possible
#All higher-level logical functions are handled by Device_Manager
class Devices_Info(object):

    def __init__(self):
        self.info = {"Batches": {}, "Unsorted Devices": {}}

    """
    Add_Device and Add_Batch is only used for adding new devices that were not from a litos lite file.
    Devices and batches that were specified in the litos lite file are created in JV_Importer, and do not have to
    be created again

    """
    def Add_Batch(self, batch_name):
        self.info["Batches"][batch_name] = {}

    def Add_Device(self, device_name, batch_name):
        if not batch_name:
            self.info["Unsorted Devices"][device_name] = {}
        else:
            self.info["Batches"][batch_name][device_name] = {}

    def Set_Device_Structure(self, structure, device_name, batch_name):
        if not batch_name:
            if not self.info["Unsorted Devices"][device_name]:
                self.info["Unsorted Devices"][device_name] = {}
            self.info["Unsorted Devices"][device_name]['Structure'] = copy.deepcopy(structure.info)
        else:
            if not self.info["Batches"][batch_name][device_name]:
                self.info["Batches"][batch_name][device_name] = {}
            self.info["Batches"][batch_name][device_name]['Structure'] = copy.deepcopy(structure.info.copy())


    def Return_Structure_Info(self, device_name, batch_name):
        if batch_name:
            return self.info["Batches"][batch_name][device_name]['Structure']
        else:
            return self.info["Unsorted Devices"][device_name]['Structure']

    def Return_Device_Info(self, device_name, batch_name):
        if batch_name:
            return self.info["Batches"][batch_name][device_name]
        else:
            return self.info["Unsorted Devices"][device_name]



devices_info = Devices_Info()

class Device_Manager(object):

    def __init__(self, structure):
        self.devices = devices_info
        self.structure = structure

    def Import_New_Devices(self, path=None):
        raw_dev_info = []
        all_batches = {}
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        if path==None:
            try:
                folder_path = filedialog.askdirectory(initialdir = save_dir, title = "Import New Devices")
            except:
                print("Device Import Aborted")
                return False
        else:
            folder_path = path

        listed_data = jvimp.Importer(folder_path)
        devices_info.info = listed_data



    """
    def Import_New_Devices(self):
        raw_dev_info = []
        all_batches = {}
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        filename = filedialog.askopenfolder(initialdir = save_dir, title = "Import New Devices")
        try:
            with open(filename, 'r') as file:
                temp = csv.reader(file, delimiter=',')
                raw_dev_info = [row for row in temp]
            for device in raw_dev_info:
                batch_name = device[0]
                device_name = device[1]

                if not batch_name:
                    devices_info.Add_Device(device_name, None)
                else:
                    if batch_name in devices_info.info["Batches"]:
                        devices_info.Add_Device(device_name, batch_name)
                    else:
                        devices_info.Add_Batch(batch_name)
                        devices_info.Add_Device(device_name, batch_name)
            return True
        except:
            print("Devices import aborted")
            return False
    """

    def Set_Device_Structure_To_Current(self, device_name, batch_name):
        self.devices.Set_Device_Structure(self.structure, device_name, batch_name)

    def Save_All_Device_Data(self):
        root = tk.Tk()
        root.withdraw()
        save_dir = os.getcwd()
        filename = filedialog.asksaveasfilename(initialdir = save_dir, title = "Save Devices Data", filetypes = (("Device Recipe Files", "*.rcpd*"), ("All files", "*.*")))
        try:
            if filename[-5:] == ".rcpd":
                print("overwritten old file with filename:"+filename)
                with open(filename[:-5] + ".rcpd", 'w') as file:
                    json.dump(self.devices.info, file, cls=DumpEncoder)
            else:
                with open(filename + ".rcpd", 'w') as file:
                    json.dump(self.devices.info, file, cls=DumpEncoder)
            return True
        except Exception as e:
            print(e)
            return False

    def Export_Recipe(self, array):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.asksaveasfilename( title = "Export Structure", filetypes = (("CSV", "*.csv*"), ("All files", "*.*")))
        if filename:
            if not filename[-4:] == ".csv":
                filename = filename + '.csv'
                array.to_csv(filename, index=False)
            else:
                array.to_csv(filename, index=False)
        else:
            print("Export Structure Aborted")

#Had to make a custom encoder for json.dump because the numpy and datetime components
#don't convert well
class DumpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return (str(obj))
        if isinstance(obj, (numpy.int_, numpy.intc, numpy.intp, numpy.int8,
                            numpy.int16, numpy.int32, numpy.int64, numpy.uint8,
                            numpy.uint16, numpy.uint32, numpy.uint64)):
            return int(obj)
        elif isinstance(obj, (numpy.float_, numpy.float16, numpy.float32,
                              numpy.float64)):
            return float(obj)
        elif isinstance(obj, (numpy.ndarray,)):
            return obj.tolist()
        else:
            return super().default(z)
