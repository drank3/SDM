saved_info = None

class Parameter_Path_Manager():

    def __init__(self, saved_infox):
        global saved_info
        saved_info = saved_infox
        self._value = []
        self._callbacks = []
        self.parameters = []
        self.attributes = []
        self.register_callback(self.printer)
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
        return self._value
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
        print(saved_info.keys())
        if len(new_path) >= 1:
            currentPos = new_path[-1]
        else:
            currentPos = "@@primary"
        try:
            self.parameters = saved_info[currentPos]["Parameters"]
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
            self.attributes = saved_info[currentPos]["Attributes"]
        except:
            self.attributes = []


class Attribute_Path_Manager(object):
    pass

class Structure_Path_Manager(object):
    pass
