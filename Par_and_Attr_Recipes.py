from PySide2 import QtCore, QtGui, QtWidgets
import json
import tkinter as tk
from tkinter import filedialog
import csv
import numpy as np

"""
This file contains two classes, one(Path Manager) which is initialized by the other
These two classes together form most of the logic behind importing, exporting, and initializing data

"""


#Where the dict for all known pars/attrs for a recipe is stored
#A possible solution for the repeat name problem is to make it so that a parameter name is stored with its whole path




"""
This class contains sets what will be the variable para_path as a property and calls its bookkeeping functions every time that value (the path)
is changed. See the __init__ for the list of bookkeeping functions added

To change the value of an instance of Path_Manager, call (var name).value = (whatever value you want)
Note that value must be a list of strings
"""

#TODO: Split this file up, it's getting too big. One for batches, structures, and fabrication
#TODO: Redesign the save system so that the parameter name is Path+name
#TODO: Make the export feature export everything, instead of just the active Path
#TODO: Also export a variable decribing the path
#TODO: Figure out some way to change the icon of a tk window
#TODO: Track if the recipe has been saved or not
#TODO: Differentiate between save and save as

class Path_Manager():

    def __init__(self):
        self._value = []
        self._callbacks = []
        self.parameters = []
        self.attributes = []
        self.register_callback(self.par_check)
        self.register_callback(self.attr_check)

    #Block of code (don't touch, I don't understand well) to set the property conditions
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, new_path):
        #Removes any Par@ identifier if there is one
        if len(new_path) >= 1:
            if 'Par@' in new_path[-1]:
                new_path[-1] = new_path[-1][4:]
        self._value = new_path
        self._notify_observers(new_path)
    def return_val(self):
        if len(self._value) > 0:
            return self._value
        elif len(self._value) == 0:
            return ["@@primary"]
    def _notify_observers(self, new_path):
        for callback in self._callbacks:
            callback(new_path)
    def register_callback(self, callback):
        self._callbacks.append(callback)


    #Just prints the parameter path whenever param_path is updated
    def printer(self, new_path):
        print("Path:" + str(new_path))

    #Updates the parameters value if there are any stored under the param in lastest path under saved_info
    def par_check(self, new_path):
        list = []
        if len(new_path) >= 1:
            currentPos = new_path[-1]
        else:
            currentPos = "@@primary"
        try:
            self.parameters = saved_info.value[currentPos]["Parameters"]
        except:
            self.parameters = []

    #Does the same thing as par_check, but with attrs
    def attr_check(self, new_path):
        list = []
        if len(new_path) >= 1:
            currentPos = new_path[-1]
        else:
            currentPos = "@@primary"
        try:
            self.attributes = saved_info.value[currentPos]["Attributes"]
        except:
            self.attributes = []

    def Set_Structure(self, structure):
        self.structure = structure

    #TODO: Raise an error if the path is not completely selected
    def Update_Structure(self):
        if hasattr(self, "structure"):
            num = self.structure.current_layer_num
            material = self.structure.current_layer_material
            self.structure.info[num]["Path"] = self.value

class Info_Manager(object):

    def __init__(self):
        self._value = {}
        self._callbacks = []
        self.structure = None
        self.register_callback(self.Update_Structure)

    #Block of code (don't touch, I don't understand well) to set the property conditions
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, info):
        self._value = info
        self._notify_observers(info)

    def _notify_observers(self, info):
        for callback in self._callbacks:
            callback(info)
    def register_callback(self, callback):
        self._callbacks.append(callback)

    #Just prints the parameter path whenever param_path is updated
    def printer(self, info):
        print("Saved Info: " + str(info))


    def Set_Structure(self, structure):
        self.structure = structure

    def Update_Structure(self, info):
        print("str updated")
        num = self.structure.current_layer_num
        material = self.structure.current_layer_material
        if num and material:
            self.structure.info[num][material] = self.value


#This is the variable that is updated with the new parameter path every time some a new one is clicked

param_path = Path_Manager()
saved_info = Info_Manager()

#class Attribute_Path_Manager

"""
This class deals with everything having to do with saving, loading, editing, and exporting saved recipe Files
NOTE: Recipe files are just dicts saved as JSON files

"""


class Recipe_Manager():
    def __init__(self):
        self.saved_info = saved_info

    def Parameter_Init(self, name):
        if len(param_path.value) == 0:
            if not saved_info.value:
                saved_info.value['@@primary'] = {'Parameters': [name]}
                saved_info.value[name] = {}
            elif 'Parameters' not in saved_info.value['@@primary']:
                saved_info.value['@@primary']['Parameters'] = [name]
                saved_info.value[name] = {}
            else:
                saved_info.value['@@primary']['Parameters'] += [name]
                saved_info.value[name] = {}

        elif len(param_path.value) > 0:
            lastPath = param_path.return_val()[-1]
            if lastPath not in saved_info.value:
                saved_info.value[lastPath] = {'Parameters': [name]}
                saved_info.value[name] = {}
            elif 'Parameters' not in saved_info.value[lastPath]:
                saved_info.value[lastPath]['Parameters'] = [name]
                saved_info.value[name] = {}
            else:
                saved_info.value[lastPath]['Parameters'] += [name]
                saved_info.value[name] = {}
        saved_info.value = saved_info.value


    #Creates a new attribute within the saved_dict, with the name, value, and group path specified (directory of attribute groups)
    def Attribute_Init(self, name, value, path):
        lastPar = param_path.return_val()[-1]
        if lastPar not in saved_info.value:
            saved_info.value[lastPar] = {'Attributes': {name: value}}
        elif 'Attributes' not in saved_info.value[lastPar]:
            saved_info.value[lastPar]['Attributes'] = {name: value}
        else:
            location = self.Find_Attr_Child(saved_info.value[lastPar]['Attributes'], path)
            location[name] = value
        saved_info.value = saved_info.value

    #Does the same thing as attribute_init,
    def Group_Init(self, name, path):


        lastPar = param_path.return_val()[-1]
        if lastPar not in saved_info.value:
            saved_info.value[lastPar] = {'Attributes': {name: {}}}
        elif 'Attributes' not in saved_info.value[lastPar]:
            saved_info.value[lastPar]['Attributes'] = {name: {}}
        else:
            location = self.Find_Attr_Child(saved_info.value[lastPar]['Attributes'], path)
            location[name] = {}
        saved_info.value = saved_info.value


    def Rename_Attribute(self, old_name, new_name, path):
        location = self.Find_Attr_Child(saved_info.value[param_path.return_val()[-1]]['Attributes'], path)
        data = location[old_name]
        location[new_name] = data
        self.Delete_Attribute(old_name, path)
        saved_info.value = saved_info.value

    def Fix_Spaces(self, vals, type):
        if type == 1:
            vals = vals.replace(' ', '_')
            return vals
        elif type == 0:
            vals = vals.replace('_', ' ')
            return vals

    def Set_Existing_Info(self, info):
        saved_info.value = info


    """
    This function controls the process of exporting the attributes associated with a certain path to a comma-delimeted csv files
    The name of the the attribute and the name of the parameter it is under are combined to form the name of that variable (separated by a '.')

    """
    def Export(self):
        array = [["Name", "Value"]]
        for attr in saved_info.value["@@primary"]["Attributes"]:
            value = saved_info.value["@@primary"]["Attributes"][attr]
            name = self.Fix_Spaces("Main", 1)+"."+self.Fix_Spaces(attr, 1)
            array += [[name, value]]

        for step in param_path.value:
            par_info = saved_info.value[step]
            try:
                for attr in saved_info.value[step]["Attributes"].keys():
                    value = saved_info.value[step]["Attributes"][attr]
                    name = self.Fix_Spaces(step, 1)+"."+self.Fix_Spaces(attr, 1)
                    array += [[name, value]]


                root = tk.Tk()
                root.withdraw()
                filename = filedialog.asksaveasfilename(initialdir = "/", title = "Export", filetypes = (("CSV", "*.csv*"), ("All files", "*.*")))
                filename = filename + ".csv"

                with open(filename, 'w', newline='') as csvfile:
                    file = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
                    for line in array:
                        file.writerow(line)

            except Exception as e:
                print(e)
                pass


    """
    The Save and Load functions can be called whenever you want to save a current saved_info as a JSON file or load an existing one
    NOTE: Load will not actually fill in the window with the saved data, better_Logic does all of that stuff after a call to Load
    """
    def Save(self):
        root = tk.Tk()
        root.withdraw()
        save_dir = "C:/Users/Daniel/Documents/College/Georgia Tech/Research/Codes and More/Device Manager/New Codes"
        filename = filedialog.asksaveasfilename(initialdir = save_dir, title = "Save Framework", filetypes = (("Recipe Files", "*.rcp*"), ("All files", "*.*")))
        if filename[-4:] == ".rcp":
            print("overwritten old file with filename:"+filename)
            with open(filename[:-4] + ".rcp", 'w') as file:
                json.dump(saved_info.value, file)
        else:
            with open(filename + ".rcp", 'w') as file:

                json.dump(saved_info.value, file)

    def Load(self, file_path):
        # So the global instance of saved_info is loaded, instead of creating a new local instance (caused much frustration)
        root = tk.Tk()
        root.withdraw()
        #filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Recipe Files", "*.rcp*"),  ("All files", "*.*")))
        filename = file_path
        try:
            with open(filename, 'r') as file:
                dict = json.load(file)
            saved_info.value = dict

            return saved_info.value
        except Exception as e:
            print(e)
            return False

    """

    This part handles deleting attributes and parameters from the saved_dict

    """

    def Delete_Attribute(self, name, path):
        parameter = param_path.return_val()[-1]
        location = self.Find_Attr_Child(saved_info.value[parameter]["Attributes"], path)
        del location[name]

        param_path.value = param_path.value

    def Find_Attr_Child(self, original, path):
        if not path:
            target = original
        else:
            target = original
            for step in path:
                #As a record of my pain, this next line was once written as original[step] and was breaking everything, hours of debugging to find it...
                target = target[step]
        return target

    def Delete_Parameter(self, name):

        try:
            if len(param_path.return_val()) == 0:
                parameter = "@@primary"
                saved_info.value[parameter]["Parameters"].remove(name)
            else:
                saved_info.value[param_path.return_val()[-1]]["Parameters"].remove(name)

        except Exception as e:
            pass

        try:
            pars_to_delete = saved_info.value[name]["Parameters"]
            for par in pars_to_delete:
                self.Delete_Parameter(par)
            del saved_info.value[name]
        except:

            del saved_info.value[name]


    def Set_No_Info_Loaded(self):

        saved_info = {}

if __name__ == "__main__":
    print("This does nothing!")
