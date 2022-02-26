import os
from PySide2 import QtWidgets, QtCore, QtGui
import sys
import json
import Updater as updater
import ctypes, sys


parent_dir = os.path.dirname(__file__)
settings_dir = parent_dir+r'/System Settings'

svl = None


#Bit of a chonker class here, ui, logic, and everything else, all in one
class Initialization_Handler():

    def __init__(self, version):

        self.Ask_Permissions()

        settings_exist = os.path.isdir(settings_dir)
        self.version = version
        #This parameter tells whether or not the initializer window has been done or not
        self.Is_Done = False
        #A list of the reuiqred inputs for the initialization window to close
        self.required_input = []
        self.all_input = []

        #Will trigger if the software has already been set up
        if settings_exist :
            self.Check_Settings()
            #self.Check_For_Updates()
            self.Is_Done = True

        #Will trigger if the software has never been opened
        else:

            self.Create_Initialization_Window()



    def Ask_Permissions(self):
        admin_status = False
        try:
            admin_status = True
        except:
            print("Is user an admin command failed")
            return False

        if admin_status==True:
            print(admin_status)
            return True
        else:
        # Re-run the program with admin rights
            print("howdy partner")
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)




    def Create_Initialization_Window(self):
        window = Custom_QDialog()
        #connecting my custom signal to Initializer_Closed, to exit the while loop
        window.window_closed.connect(self.Initializer_Closed)

        window.setWindowIcon(QtGui.QIcon())
        window.setWindowTitle("Initialize Device Manager Settings")
        screen = QtGui.QGuiApplication.primaryScreen()

        dialog_width = 375
        dialog_height = 155
        #Ensures that that the dialog is created in the middle of the active screen
        dialog_x = screen.size().width()/2 -dialog_width/2
        dialog_y = screen.size().height()/2 - dialog_height/2
        window.setGeometry(QtCore.QRect(dialog_x, dialog_y, dialog_width, dialog_height))
        self.window = window

        """
        frame = QtWidgets.QFrame(window)
        frame.setGeometry(QtCore.QRect(15, 15, window.width()-50, window.height()*.4))
        frame.setLineWidth(1)
        frame.setFrameShape(QtWidgets.QFrame.Panel)
        """
        #The vertical space between each sequential item in the window
        item_spacer = 15

        font = QtGui.QFont()
        font.setPointSize(11)

        label_font = QtGui.QFont()
        label_font.setPointSize(10)
        #label_font.setBold(True)

        button_font = QtGui.QFont()
        button_font.setPointSize(11)

        note_font =QtGui.QFont()
        note_font.setPointSize(7)


        user = QtWidgets.QLineEdit(window)
        user.setObjectName("Username")
        user.setGeometry(QtCore.QRect(160, 20, 180, 28))
        user.setMaxLength(50)
        user.setFont(font)
        user.type = "LineEdit"
        self.required_input.append(user)
        self.all_input.append(user)

        user_label = QtWidgets.QLabel(window)
        user_label.setText("Full Name of User:")
        user_label.setFont(label_font)
        user_label.setGeometry(QtCore.QRect(125, 0, 15, 15))
        user_label.adjustSize()
        user_label.resize(user_label.width(), user.height())
        user_label.move(user.x() - 140, user.y()  )


        database = QtWidgets.QLineEdit(window)
        database.move(user.x(), user.y()+user.height()+item_spacer)
        database.setObjectName("Database Name")
        database.resize(user.width(), user.height())
        database.setFont(font)
        database.setMaxLength(100)
        database.setText("EML")
        database.type = "LineEdit"
        self.required_input.append(database)
        self.all_input.append(database)

        database_label = QtWidgets.QLabel(window)
        database_label.setText("Enter Database Name")
        database_label.setFont(label_font)
        database_label.adjustSize()
        database_label.resize(database_label.width(), database.height())
        database_label.move(database.x() - 140, database.y()  )

        database_note = QtWidgets.QLabel(window)
        database_note.setText("**Database name for general lab use is 'EML'")
        database_note.setFont(note_font)
        database_note.move(database.x(), database.y()+database.height() + 4)
        database_note.setStyleSheet("color: rgb(90,90,90)")





        #Here are the enter and cancel buttons
        cancel = QtWidgets.QPushButton(window)
        cancel.setGeometry(QtCore.QRect(30, 2, 10, 10))
        cancel.setText("Cancel")
        cancel.setFont(button_font)
        cancel.adjustSize()
        cancel.move(25, window.height() - cancel.height() - 15)

        enter = QtWidgets.QPushButton(window)
        enter.setGeometry(QtCore.QRect(30, 2, 10, 10))
        enter.setText(" Set Information ")
        enter.setFont(button_font)
        enter.adjustSize()
        enter.move(window.width() - enter.width() - 25, window.height()-enter.height() - 15)
        enter.pressed.connect(self.Setup_Completed)



        window.exec()



    def Initializer_Closed(self):
        self.Is_Done = True

    #Triggered when the set information button is hit
    #Creates the System Settings File, or prompts the user to add in all information
    def Setup_Completed(self):
        all_completed= True
        not_completed = []
        for item in self.required_input:
            if not item.text():
                all_completed=False
                not_completed.append(item)

        #Case for when all information has been entered
        if all_completed:
            inputted_information = {}
            for item in self.all_input:
                if item.type == "LineEdit":
                    inputted_information[item.objectName()] = item.text()

            os.mkdir(settings_dir)
            with open(settings_dir+r'/Settings.txt', 'w') as file:
                json.dump(inputted_information, file)

            self.window.close()

        else:
            self.Raise_Not_Completed_Message(not_completed)



    #Shoots a message boc if not all the information specified in self.required_input has been filled
    def Raise_Not_Completed_Message(self, not_completed):
        message = QtWidgets.QMessageBox()

        text = "Not all required values have been specified, please complete the following:"

        for item in not_completed:
            text+= "\n\n\t-{}".format(item.objectName())

        text+='\n'

        message.setWindowTitle("Error")


        pixmap = QtGui.QPixmap( 32, 32 )
        pixmap.fill( QtCore.Qt.transparent )
        message.setWindowIcon(QtGui.QIcon(pixmap))
        message.setIcon(QtWidgets.QMessageBox.Critical)
        message.setText(text)
        message.adjustSize()
        message.exec()

    #Creating an instance of the update manager to check the server for any Updates
    #and take action to complete them if necessary
    def Check_For_Updates(self):
        um = updater.Update_Manager(self.version)
        um.Check_For_Updates()
        if um.connection:
            um.connection.close()


    def Check_Settings(self):
        pass

#Quick little update to the QDialog class that emits an empty signal on a closeevent, which is window_closed
class Custom_QDialog(QtWidgets.QDialog):
    window_closed = QtCore.Signal()

    #Overwriting the dialog's closeEvent, event is a CloseEvent object, but not really important
    def closeEvent(self, event):
        super().closeEvent(event)
        self.window_closed.emit()
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Initialization_Handler()
