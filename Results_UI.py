from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtCharts import QtCharts
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import seaborn as sb

class Results_Window(object):

    def __init__(self, results_viewer):

        self.results_viewer = results_viewer
        self.Create_Frames()

    #Creates some neat frames for the graphs to fit in
    def Create_Frames(self):
        #spacer on the left and right side of all the graphs
        self.h_spacer = 15

        #spacer on the top and bottom
        self.v_spacer = 30

        self.frame = QtWidgets.QFrame(self.results_viewer)
        self.frame.setGeometry(QtCore.QRect(self.h_spacer, self.v_spacer, self.results_viewer.width()-2*self.h_spacer, self.results_viewer.height()-2*self.v_spacer))
        self.frame_layout = QtWidgets.QHBoxLayout(self.results_viewer)



        """
        #spacer between graphs
        self.inter_spacer = 10

        #spacer on the left and right side of all the graphs
        self.h_spacer = 15

        #spacer on the top and bottom
        self.v_spacer = 30

        graph_width = (self.results_viewer.width()-2*self.h_spacer-2*self.inter_spacer)/3
        graph_height = (self.results_viewer.height() - 2*self.v_spacer)

        #Graphs 1-3 are equal sized and next to each other
        self.frame_1 = QtWidgets.QLabel(self.results_viewer)
        self.frame_1.setObjectName("Results@self.frame_1")
        self.frame_2 = QtWidgets.QLabel(self.results_viewer)
        self.frame_2.setObjectName("Results@self.frame_2")
        self.frame_3 = QtWidgets.QLabel(self.results_viewer)
        self.frame_3.setObjectName("Results@self.frame_3")

        #Graph 4 is long and for boxplots
        self.frame_4 = QtWidgets.QLabel(self.results_viewer)
        self.frame_4.setObjectName("Results@self.frame_4")
        #self.frame_4.setFrameShape(QtWidgets.QFrame.Box)


        self.frame_1.setGeometry(self.h_spacer, self.v_spacer, graph_width, graph_height)
        self.frame_2.setGeometry(self.h_spacer+graph_width+self.inter_spacer, self.v_spacer, graph_width, graph_height)
        self.frame_3.setGeometry(self.h_spacer+2*graph_width+2*self.inter_spacer, self.v_spacer, graph_width, graph_height)

        self.frame_4.setGeometry(self.h_spacer, self.v_spacer, self.results_viewer.width()-2*self.h_spacer, self.results_viewer.height()-2*self.v_spacer)
        """



    def Create_JV_Plot(self, light_rv, light_fw, dark_rv, dark_fw):

        self.graph_1 = MplCanvas()
        self.graph_1.axes.plot(light_rv[:, 0], light_rv[:, 1])
        self.graph_1.axes.plot(light_fw[:, 0], light_fw[:, 1])

        self.graph_2 = MplCanvas()
        self.graph_2.axes.plot(dark_rv[:, 0], dark_rv[:, 1])
        #self.graph_1.axes.plot(dark_fw[:, 0], dark_fw[:, 1])


        #self.graph_1.axes.set_title("Light JV")
        self.graph_1.axes.set_xlabel("Voltage (V)")
        self.graph_1.axes.set_ylabel("Current Density (mA/cm\u00b2)")
        self.graph_1.axes.set_title("Light JV")

        self.graph_2.axes.set_xlabel("Voltage (V)")
        self.graph_2.axes.set_ylabel("Current Density (mA/cm\u00b2)")
        self.graph_2.axes.set_title("Dark JV")

        #FigureCanvas.updateGeometry(self.graph_1)
        self.graph_1.fig.set_tight_layout(True)
        self.graph_2.fig.set_tight_layout(True)
        self.frame_layout.addWidget(self.graph_1)
        self.frame_layout.addWidget(self.graph_2)




    def Create_MPP_Plot(self, data, name):
        parent = self.frame_3
        self.graph_3 = QtCharts.QLineSeries(parent)

    def Create_Bar_Graph(self, data_df, name):

        self.graph_4 = QtCharts.QChartView()
        self.graph_4.series = QtCharts.QBarSeries()
        """
        self.graph_4 = QtCharts.QChartView(self.frame_4)
        self.graph_4.series = QtCharts.QBarSeries(self.frame_4)
        """
        for column in data_df.columns:
            bar_set = QtCharts.QBarSet(column)
            bar_set.append(list(data_df[column].values))
            self.graph_4.series.append(bar_set)
        self.graph_4.chart().setTitle("Device Summary")
        self.graph_4.chart().addSeries(self.graph_4.series)

        #self.graph_4.setGeometry(0, 0, self.frame_4.width(), self.frame_4.height())
        axis = QtCharts.QBarCategoryAxis()
        axis.append(["Pixels"])
        self.graph_4.chart().createDefaultAxes()
        self.graph_4.chart().addAxis(axis, QtCore.Qt.AlignBottom)
        self.frame_layout.addWidget(self.graph_4)
        self.Resize()

    def Create_Box_Plot(self, data_df, type):
        if type=="Group":
            self.graph_4 = MplCanvas()
            self.graph_4.axes.boxplot(data_df)
            self.graph_4.axes.set_xticklabels(list(data_df.columns.values))
            self.frame_layout.addWidget(self.graph_4)

        elif type=="Total":
            self.graph_4 = MplCanvas()
            boxes = []
            for column in data_df.columns:
                box_data = data_df[column].dropna()
                boxes = boxes + [box_data]
            self.graph_4.axes.boxplot(boxes)    
            self.graph_4.axes.set_xticklabels(list(data_df.columns.values))
            self.frame_layout.addWidget(self.graph_4)

    #This function resizes anything that needs to be resized in the event that the window size is changed
    def Resize(self):

        self.frame.setGeometry(QtCore.QRect(self.h_spacer, self.v_spacer, self.results_viewer.width()-2*self.h_spacer, self.results_viewer.height()-2*self.v_spacer))


        """
        graph_width = (self.results_viewer.width()-2*self.h_spacer-2*self.inter_spacer)/3
        graph_height = (self.results_viewer.height() - 2*self.v_spacer)

        self.frame_1.setGeometry(self.h_spacer, self.v_spacer, graph_width, graph_height)
        self.frame_2.setGeometry(self.h_spacer+graph_width+self.inter_spacer, self.v_spacer, graph_width, graph_height)
        self.frame_3.setGeometry(self.h_spacer+2*graph_width+2*self.inter_spacer, self.v_spacer, graph_width, graph_height)

        self.frame_4.setGeometry(self.h_spacer, self.v_spacer, self.results_viewer.width()-2*self.h_spacer, self.results_viewer.height()-2*self.v_spacer)

        if hasattr(self, 'graph_1'):
            self.graph_1.setGeometry(self.frame_1.geometry())
            MplCanvas.updateGeometry(self.graph_1)
        """
class MplCanvas(FigureCanvas):

    def __init__(self, width=5, height=5, dpi=100):

        self.fig = Figure()
        self.fig.tight_layout(rect =(5, 0.1, 0.95, 2))
        self.fig.set_tight_layout(True)

        super(MplCanvas, self).__init__(self.fig)
        #self.setParent(parent)
        self.axes = self.fig.add_subplot(111)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.resize(self.width()-50, self.height())
        MplCanvas.updateGeometry(self)
