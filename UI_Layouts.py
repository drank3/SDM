"""
This file maintains everything with relation to the window layout of the Recipe Manager applet. All Resizing
logic, default frame ratios, window initialization, and eventually layout design (pretty UI stuff) is located
here.


"""

from PySide2 import QtCore, QtGui, QtWidgets

#Window size values for the importer mode
attributes_default_width = .33
attribute_default_height = .65
batch_viewer_default_width = .22


#Window size values for the viewer option
devices_viewer_default_width = .25
results_viewer_default_height = .6



class Layouts:

    def __init__(self, parent):
        self.parent = parent
        self.MainWindow = parent.MainWindow
        self.parent.central_layout = QtWidgets.QGridLayout(self.parent.centralwidget)
        self.parent.centralwidget.setLayout(self.parent.central_layout)

        self.parent.central_layout.setColumnStretch(0, 2)
        self.parent.central_layout.setColumnStretch(1, 4)
        self.parent.central_layout.setColumnStretch(2, 3)

        self.parent.central_layout.setRowStretch(0, 13)
        self.parent.central_layout.setRowStretch(1, 7)

        self.Default_Window_Initialization()
        self.Resizing(self.MainWindow)
        self.MainWindow.resizeEvent = self.Resizing

    def Default_Window_Initialization(self):

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)


        self.parent.parameter_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.central_layout.addWidget(self.parent.parameter_viewer, 1, 1, 1, 2)

        self.parent.parameter_viewer.setWidgetResizable(True)
        self.parent.parameter_viewer.setObjectName("parameter_viewer")
        self.parent.parameter_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.parameter_viewer_widget_contents.setGeometry(QtCore.QRect((batch_viewer_default_width)*self.MainWindow.width()+1, attribute_default_height*self.MainWindow.height(), (1-batch_viewer_default_width)*self.MainWindow.width(), (1-attribute_default_height)*self.MainWindow.height()))
        self.parent.parameter_viewer_widget_contents.setObjectName("parameter_viewer_widget_contents")
        self.parent.parameter_viewer.setWidget(self.parent.parameter_viewer_widget_contents)

        self.parent.attribute_viewer = QtWidgets.QFrame(self.parent.centralwidget)
        self.parent.central_layout.addWidget(self.parent.attribute_viewer, 0, 2, 1, 1)
        self.parent.attribute_viewer.layout = QtWidgets.QGridLayout(self.parent.attribute_viewer)
        self.parent.attribute_viewer.setGeometry(QtCore.QRect((1-attributes_default_width)*self.MainWindow.width(), 0, attributes_default_width*self.MainWindow.width(), (attribute_default_height)*self.MainWindow.height()))
        self.parent.attribute_viewer.setObjectName("attribute_viewer")



        self.parent.batch_viewer = QtWidgets.QFrame(self.parent.centralwidget)
        self.parent.central_layout.addWidget(self.parent.batch_viewer, 0, 0, 2, 1)

        self.parent.batch_viewer.setGeometry(QtCore.QRect(0, 0, batch_viewer_default_width*self.MainWindow.width(), self.MainWindow.height()))
        self.parent.batch_viewer.setObjectName("batch_viewer")
        self.parent.batch_viewer.layout = QtWidgets.QGridLayout(self.parent.batch_viewer)


        self.parent.structure_viewer = QtWidgets.QFrame(self.parent.centralwidget)
        self.parent.central_layout.addWidget(self.parent.structure_viewer, 0, 1, 1, 1)
        self.parent.structure_viewer.setGeometry(QtCore.QRect(1, 1, 1, 1))
        self.parent.structure_viewer.setObjectName("structure_viewer")
        self.parent.structure_viewer.layout = QtWidgets.QGridLayout(self.parent.structure_viewer)

        self.parent.devices_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.devices_viewer.setGeometry(QtCore.QRect(1, 1, 1000, 1000))
        self.parent.devices_viewer.setWidgetResizable(True)
        self.parent.devices_viewer.setObjectName("devices_viewer")
        self.parent.devices_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.devices_viewer_widget_contents.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.parent.devices_viewer_widget_contents.setObjectName("devices_viewer_widget_contents")
        self.parent.devices_viewer.setWidget(self.parent.devices_viewer_widget_contents)

        self.parent.info_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.info_viewer.setGeometry(QtCore.QRect(1, 1, 100, 100))
        self.parent.info_viewer.setWidgetResizable(True)
        self.parent.info_viewer.setObjectName("info_viewer")
        self.parent.info_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.info_viewer_widget_contents.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.parent.info_viewer_widget_contents.setObjectName("info_viewer_widget_contents")
        self.parent.info_viewer.setWidget(self.parent.info_viewer_widget_contents)

        self.parent.results_viewer = QtWidgets.QScrollArea(self.parent.centralwidget)
        self.parent.results_viewer.setGeometry(QtCore.QRect(1, 1, 100, 100))
        self.parent.results_viewer.setWidgetResizable(True)
        self.parent.results_viewer.setObjectName("results_viewer")
        self.parent.results_viewer_widget_contents = QtWidgets.QWidget()
        self.parent.results_viewer_widget_contents.setGeometry(QtCore.QRect(0, 0, 100, 100))
        self.parent.results_viewer_widget_contents.setObjectName("results_viewer_widget_contents")
        self.parent.results_viewer.setWidget(self.parent.results_viewer_widget_contents)





    """
    This function is triggered whenever the mainWindow is resized and adjusts the two main scroll area sizes

    There are inbuilt functions to deal with these kind of scaling resizing events in Qt, but rather than
    spend the 30 minutes to figure out how to use them I thought coding them from scratch would be easier

    """
    def Resizing(self, event):

        mw_width = event.size().width()-1
        mw_height = event.size().height()-42

        if self.parent.mode == "Importer":
            #Everything in here is now managed by a layout, no need to manuslly resize anymore
            pass

        elif self.parent.mode == "Viewer":
            #Windows ---------------------------------------------------------
            devices_viewer_x = 1
            devices_viewer_y = 0
            devices_viewer_width = devices_viewer_default_width*mw_width
            devices_viewer_height = mw_height
            self.parent.devices_viewer.resize(devices_viewer_width, devices_viewer_height)
            self.parent.devices_viewer_widget_contents.resize(devices_viewer_width, devices_viewer_height)
            self.parent.devices_viewer.move(devices_viewer_x, devices_viewer_y)

            results_viewer_x = devices_viewer_width
            results_viewer_y = 0
            results_viewer_width = mw_width - devices_viewer_width
            results_viewer_height = results_viewer_default_height*mw_height
            self.parent.results_viewer.resize(results_viewer_width, results_viewer_height)
            self.parent.results_viewer_widget_contents.resize(results_viewer_width, results_viewer_height)
            self.parent.results_viewer.move(results_viewer_x, results_viewer_y)

            info_viewer_x = devices_viewer_width
            info_viewer_y = results_viewer_y+results_viewer_height-1
            info_viewer_width = mw_width - devices_viewer_width
            info_viewer_height = mw_height-info_viewer_y+1
            self.parent.info_viewer.resize(info_viewer_width, info_viewer_height)
            self.parent.info_viewer_widget_contents.resize(info_viewer_width, info_viewer_height)
            self.parent.info_viewer.move(info_viewer_x, info_viewer_y)
            #------------------------------------------------------------------

            #Applets
            #--------------------------------------------------------
            self.parent.DUI.Resize()
            self.parent.RUI.Resize()
