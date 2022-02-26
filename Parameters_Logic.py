from PySide2 import QtCore, QtGui, QtWidgets

ui, rp, param_path, AL = [None, None, None, None]

#TODO: Replace those garbage label params with toggling pushbuttons
class Parameters_Main_Logic(object):

    def __init__(self, uix, rpx, param_pathx, ALx):
        global ui, rp, param_path, AL
        ui = uix
        rp = rpx
        param_path = param_pathx
        AL = ALx


    #Removes every par grid after and including the one specified by gNum (see the number at the end of the grid's object name)
    def Clear_Par_Window(self, gNum):

        rmvCond = False
        rmvdChildren = []
        childList = ui.parameter_viewer.children()


        #Locating all frames after button click
        for child in childList:
            if str(type(child)) == "<class 'PySide2.QtWidgets.QFrame'>":
                try:
                    locater = int((child.objectName())[-1])
                except:
                    pass
                if rmvCond:
                    rmvdChildren.append(child)
                elif locater == gNum:
                    rmvCond = True
                    rmvdChildren.append(child)

        #Removing extra frames after the loops completion because of unbased paranoia
        for child in rmvdChildren:
            child.setParent(None)



    """
    This functions takes the current an int gNum as a grid number (that locator at the end of the grid name) and fills a that grid with all the parameters
    attributed to the last value in param_path (which is stores in param_path.parameters)


    """
    def Fill_Pars(self, gNum):

        try:
            if not param_path.parameters:
                raise TypeError("No parameters")
            else:
                plusP = ui.PUI.Create_Grid(gNum, "Par", ui.parameter_viewer)
                grid = plusP.parent()


                for par_line in param_path.parameters:
                    xPos = plusP.x()
                    yPos = plusP.y()
                    oldPlus = plusP
                    plusP = ui.PUI.Create_Plus(xPos, yPos + ui.PUI.VSpacer + ui.PUI.VHeight, "Par", grid)
                    oldPlus.setParent(None)
                    ui.PUI.Create_Cell(xPos, yPos, "Par", par_line, grid)

                grid.adjustSize()
                grid.setVisible(True)
                param_path.parameters = []


        except Exception as e:
            print(e)
            grid = ui.PUI.Create_Grid(gNum, "Par", ui.parameter_viewer).parent()

            #HERE: Make a convert button

            newX = grid.width()/2
            yPos = grid.y()+10

            pos = QtCore.QPoint(newX, yPos)

            grid.adjustSize()



    # Will hide all plusses except for the one on the active parameter frame
    def Clear_and_Set_Active_Plusses(self, gNum):
        childList = ui.parameter_viewer.children()


        for child in childList:
            if child.objectName().__contains__("frame"):
                try:
                    child.findChild(QtWidgets.QLabel, "Add@Par").setVisible(False)
                    if str(gNum) == child.objectName()[-1]:
                        child.findChild(QtWidgets.QLabel, "Add@Par").setVisible(True)
                except Exception as e:
                    print(["Plusses visibility setting failed with an error:" + e])



    def Parameter_Creation(self, event):
        #Case is triggered if any key but enter button is pressed, will expand this later
        if event.key() != 16777220:

            #Condition so that backspace works correctly
            if event.key() != 16777219:
                ui.PUI.lineEdit.setText(ui.PUI.lineEdit.text() + event.text())
            else:
                currentWords =ui.PUI.lineEdit.text()
                ui.PUI.lineEdit.setText(currentWords[0:(len(currentWords)-1)])
        else:
            #I don't really know how the event inheritance works, so I am rebuilding all of these variables (instead of inheriting them)
            #TODO: make this also trigger on outside click
            parent = ui.PUI.lineEdit.parent()
            line = ui.PUI.lineEdit.text()
            xPos = ui.PUI.lineEdit.x()
            yPos = ui.PUI.lineEdit.y()
            ui.PUI.lineEdit.setParent(None)
            ui.PUI.Create_Cell(xPos, yPos, "Par", line, parent)
            rp.Parameter_Init(line)

            #Spaces out the new plus according to the VSpacer and VHeight parameters from the ui
            ui.PUI.Create_Plus(xPos, yPos + ui.PUI.VSpacer + ui.PUI.VHeight, "Par", parent)
            parent.adjustSize()




    def Delete(self, trigger):
        print(trigger)
        gNum = int(trigger.parent().objectName()[-1])
        #If the parameter was clicked (is in the path)
        if trigger.status == 1:
            #Fixing the param_path so in case deletion changes it
            param_path.value = param_path.return_val()[0:gNum]
            rp.Delete_Parameter(trigger.objectName()[4:])
            self.Clear_Par_Window(gNum)
            AL.Clear_Attr_Window()
            AL.Fill_Attrs()
            self.Fill_Pars(gNum)

        #If the parameter wasn't clicked
        elif trigger.status == 0:
            param_path.value = param_path.return_val()[0:gNum]
            rp.Delete_Parameter(trigger.objectName()[4:])
            self.Clear_Par_Window(gNum)
            AL.Clear_Attr_Window()
            AL.Fill_Attrs()
            self.Fill_Pars(gNum)


    def Left_Click(self, select_btn):
        if select_btn.objectName() == "Add@Par":

            frameParent = select_btn.parent().parent()
            #just some number to tell the buttons apart if there is a need to
            num = len(select_btn.parent().parent().children())
            xPos = select_btn.parent().x()
            yPos = select_btn.parent().y()
            #Deleting the old plus object
            select_btn.parent().setParent(None)

            name_editor = ui.PUI.Create_TextEdit(xPos, yPos, num, frameParent)
            ui.PUI.lineEdit.keyPressEvent = self.Parameter_Creation



        #Case: If one of the parameters is clicked
        elif select_btn.objectName().__contains__("Par"):
            #Index of the grid
            gNum = int((select_btn.parent().objectName())[-1])

            #Case: If the button is already pressed (unchecking it)
            if select_btn.status == 1:
                select_btn.status = 0

                select_btn.setStyleSheet('''background-color: rgb(248,248,248);''')
                select_btn.setFrameShadow(QtWidgets.QFrame.Raised)

                #Using +1 because I don't want to remove the current grid, and Clear_Par_Window removes every grid including the current gNum
                self.Clear_Par_Window(gNum+1)

                #also resetting the param_path to the current position
                param_path.value = param_path.return_val()[0:gNum]
                #Setting parameters to nothing(despite the fact that it is untrue, to avoid later param filling issues)
                param_path.parameters = []
                AL.Fill_Attrs()
                self.Clear_and_Set_Active_Plusses(gNum)

            #Case: If No buttons are pressed yet
            elif select_btn.status == 0:
                for child in select_btn.parent().children():
                    if child.objectName().__contains__("Par"):
                        if child.status == 1:
                            child.status = 0
                            child.setFrameShadow(QtWidgets.QFrame.Raised)
                            child.setStyleSheet('''background-color: rgb(248,248,248);''')
                            param_path.value = param_path.return_val()[:gNum]
                self.Clear_Par_Window(gNum+1)
                select_btn.setFrameShadow(QtWidgets.QFrame.Sunken)
                select_btn.status = 1

                select_btn.setStyleSheet('''background-color: rgb(225,225,255);''')
                param_path.value += [select_btn.objectName()]

                AL.Fill_Attrs()
                self.Fill_Pars(gNum+1)

                self.Clear_and_Set_Active_Plusses(len(param_path.return_val()))

            param_path.Update_Structure()

    def Path_Filler(self, path):
        count = 1

        for step in path:
            children = ui.PUI.frame.children()
            pressed_button = [child for child in children if child.objectName().__contains__(step)][-1]

            pressed_button.setFrameShadow(QtWidgets.QFrame.Sunken)
            pressed_button.status = 1
            pressed_button.setStyleSheet('''background-color: rgb(225,225,255);''')

            param_path.value += [step]
            self.Fill_Pars(count)
            AL.Fill_Attrs()
            count = count +1



        self.Clear_and_Set_Active_Plusses(count-1)


    def Right_Click(self, select_btn, event):

        if select_btn.objectName().__contains__("Par@"):
            ui.PUI.Context_Menu(select_btn, event)


        try:
            ui.PUI.actionDelete.triggered.connect(lambda: self.Delete(select_btn))
        except Exception as e:
            print(["Context Menu Action Failed with log:" + e])
