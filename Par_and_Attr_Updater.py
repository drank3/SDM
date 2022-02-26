class Info_Filler():

    def __init__(self, AL, PL, param_path):
        self.AL = AL
        self.PL = PL
        self.param_path = param_path
        self._value = []
        self._callbacks = []
        self.register_callback(self.printer)
        self.register_callback(self.filler)


    #Block of code (don't touch, I don't understand well) to set the property conditions
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, saved_info):
        self._value = saved_info
        self._notify_observers(saved_info)

    def _notify_observers(self, saved_info):
        for callback in self._callbacks:
            callback(saved_info)
    def register_callback(self, callback):
        self._callbacks.append(callback)



    def printer(self, saved_info):
        pass
        #print("saved_info:" + str(saved_info))

    #Updates the parameters value if there are any stored under the param in lastest path under saved_info
    def filler(self, saved_info):
        self.AL.Clear_Attr_Window()
        #Since 0 is the lowest gNum for a grid, this deletes every grid
        self.PL.Clear_Par_Window(0)
        self.param_path.value = []
        self.PL.Fill_Pars(0)
        self.AL.Fill_Attrs()

    def Update_Path(self, path):
        self.PL.Path_Filler(path)

    def Clear_Par_and_Attr(self):
        self.AL.Clear_Attr_Window()
        self.PL.Clear_Par_Window(0)
        self.param_path.value = []
