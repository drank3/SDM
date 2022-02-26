rp = None
import os
import json
import tkinter as tk
from tkinter import filedialog

parent_dir = os.path.dirname(__file__)

class Material_Manager(object):

    def __init__(self, rpx, updater):
        global rp
        rp = rpx
        self.updater = updater

        self.full_info = {"Materials": {}}

        #Checks for and creates a folder for default materials if it doesnt exist
        materials_path = parent_dir + r'/Default Materials'
        if not os.path.isdir(materials_path):
            os.mkdir(materials_path)

    def Save(self):
        pass

    def Return_Materials(self):
        all_mats = []
        for material in self.full_info["Materials"].keys():
            all_mats = all_mats + [material]

        return all_mats

    def Create_Material(self, mat):
        self.full_info["Materials"][mat] = {"Parameters": {}, "Options": {}}


    def Load_Material(self, material):
        if material:
            filename = material + ".rcp"
            full_path = parent_dir +"\\"+"Default Materials"+"\\"+filename
            try:
                with open(full_path, 'r') as file:
                    saved_info = json.load(file)
            except:
                saved_info = {}

        else:
            saved_info = {}
            rp.Set_No_Info_Loaded()

        if saved_info:
            print("Material Loaded Successfully")
        elif not saved_info and material:
            print("No such file located (or file was empty), new one created")
            with open(full_path, 'w') as file:
                json.dump({}, file)
        elif not material:
            pass

        return saved_info

    def Set_Existing_Material_Info(self, info, path):

        rp.Set_Existing_Info(info)
        self.updater.value = info
        if info:
            self.updater.Update_Path(path)


    def Load_Default_Materials(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(initialdir = os.getcwd() + r'Default Materials', title = "Load Materials List", filetypes = (("Recipe Materials", "*.rcpm*"),  ("All files", "*.*")))
        try:
            with open(filename, 'r') as file:
                dict = json.load(file)
            self.full_info = dict
        except:
            print("Materials Load Aborted")

    def Save_Default_Materials(self, ST):
        root = tk.Tk()
        root.withdraw()
        save_dir = parent_dir + "\\" +"Default Materials" + "\\"
        filename = "default_materials.rcpm"
        list_path = save_dir + filename
        try:
            with open(list_path, 'w') as file:
                json.dump(self.full_info, file)
        except Exception as e:
            print("Def Mat save failed with code: " + str(e))



        for info in ST.info:
            if info:
                material = [key for key in info.keys() if key != "Path"][-1]
                mat_path = save_dir + material + ".rcp"
                print(mat_path)
                with open(mat_path, 'w') as file:
                    json.dump(info[material], file)

    def Initialize_Materials(self):

        filename = parent_dir + "\\" + "Default Materials" + "\\" + "default_materials.rcpm"
        try:
            with open(filename, 'r') as file:
                dict = json.load(file)
                self.full_info = dict
        except:
            print("Materials list initialization failed. Check that default materials file exists and is in the correct directory")
