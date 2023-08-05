try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None


import stdcomQt
import sys, getopt
import pyqtgraph as pg

from labjacku6gui import Ui_DialogLabjacku6

from PyQt5.QtWidgets import QDialog, QApplication, QTableWidgetItem, QMessageBox, QSizePolicy
from PyQt5.QtCore import QSettings, Qt, pyqtSlot, pyqtSignal, QEvent, QTimer
from PyQt5.QtGui import QColor


from stdcomQt.stdcomQt import *
from stdcomQt.stdcomvsettings import *

import u6allio




class Labjacku6guigeneric(QDialog):
    cBridge = None
    s1 = None
    timer = None
    timerSec = None
    timerRestart = None

    lastData = None

    project = "stec-python3"
    projectWhat = "LabjackU6"

    n = 0
    sumData = 0

    trendData = []
    currentAdc = 0

    XName = 'Time'
    XUnits = 'Seconds'

    YName = 'ADC'
    YUnits = 'Volts'
    graphWidget = None

    Subscription = None

    def __init__(self):

        super().__init__()
        self.ui = Ui_DialogLabjacku6()
        self.ui.setupUi(self)
        self.show()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.TimeOut)

        self.ui.tableWidget.cellClicked.connect(self.on_Active)
        self.cBridge = None

        self.ReadConfig()

        self.timerSec = QTimer(self)
        self.timerSec.timeout.connect(self.TimeOneSec)
        self.timerSec.setInterval(1000 * self.trendTimer)

        self.timerRestart  = QTimer(self)
        self.timerRestart.timeout.connect(self.RestartAttmepts)
        self.timerRestart.setInterval(7500)

        self.ui.pushButtonApply.clicked.connect(self.Apply)
        self.ui.pushButtonClose.clicked.connect(self.Exit)
        self.OpenAll()

    @staticmethod
    def utilisfloat(x):
        try:
            a = float(x)
        except (TypeError, ValueError):
            return False
        else:
            return True

    def graph(self ):
        """
        :param points:
        :param key:
        :return:
        """

        if self.currentAdc > len(self.trendData) :
            return

        sum = 0.0
        X = [sum]

        points = self.trendData[self.currentAdc]

        for i in range(1, len(points)) :
            sum = sum + float(self.trendTimer)
            X.append( sum)


        if len(X) < 2 or len(points) < 2 :
            return

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        Max = None
        Min = None

        Y = []
        for i in range(0, len(points)):

            if Max is None or points[i] > Max:
                Max = float(points[i])
            if Min is None or points[i] < Min:
                Min = float(points[i])

            Y.append(float(points[i]))

            if i > len(X) :
                break;

        if Max is not None and Min is not None:

            graphWidget = self.graphWidget
            if graphWidget is not None:
                graphWidget.clear()

            if graphWidget is None:
                graphWidget = pg.PlotWidget(self)
                self.graphWidget = graphWidget
                graphWidget.setLabel('bottom', self.XName, self.XUnits)
                graphWidget.setLabel('left', self.YName, self.YUnits)

                self.ui.horizontalLayout_9.addWidget(self.graphWidget)
                self.graphWidget.show()
            graphWidget.setYRange(Min,Max,.5)
            p1 = graphWidget.plot()
            p1.setPen(pg.mkPen(QColor(Qt.red)))
            p1.setData(X, Y)

    def CloseAll(self):
        if self.cBridge is not None :
            self.cBridge.quit
            self.cBridge = None
        if self.s1 is not None :
            self.s1.close()
            self.s1 = None

        self.timer.stop()


    def StartCBridge(self):

        if self.ui.checkBoxcBridge.isChecked():
            XHOST = self.ip
            XPORT = int(self.port)  # service port for NextStep plugin

            if self.cBridge is None :
                self.cBridge = stecQSocket(XHOST, XPORT)
            else :
                self.cBridge.SlotNewHost(XHOST, XPORT)

            if self.Subscription is not None :
                self.Subscription.deleteLater()

            self.Subscription = Subscriber(self.sub, self.cBridge)


        else:
            if self.Subscription is not None :
                self.Subscription.deleteLater()
                self.Subscription = None

            if self.cBridge is not None :
                self.cBridge.quit()




    def OpenAll(self):
        self.CloseAll()
        # this could be argv but we will weld it for now

        adcs = int(self.nbradc)
        self.ui.tableWidget.setRowCount(adcs)

        self.n = 0
        self.sumData = []
        self.trendData = []
        for i in range(0, int(self.nbradc)):
            record = []
            self.trendData.append(record)
            self.sumData.append( float(0))

        if self.ui.checkBoxcBridge.isChecked():
            self.StartCBridge()
            self.timerRestart.start()
        else:
            self.timerRestart.stop()

        try :
            self.s1 = u6allio.LabJackU6(adcs)
            self.timer.setInterval(int(self.freq))
            self.timer.start()
            self.timerSec.setInterval(1000 * self.trendTimer)
            self.timerSec.start()
        except :
            self.s1 = None
            QMessageBox.about(self, "labjacku6", "missing labjacku6 adaptor")


    def closeEvent(self, event: QEvent = None):

        self.CloseAll()
        if event is not None :
            event.accept()

    def readScreen(self):
        self.ip = self.ui.lineEditIpAddress.text()
        self.port = self.ui.lineEditPort.text()
        self.nbradc = int(self.ui.spinBoxNbrAdcs.value())
        self.freq = int(self.ui.spinBoxInterval.value())
        self.sub= self.ui.lineEditSubname.text()
        if self.ui.checkBoxcBridge.isChecked() :
            self.multiverseEnabled = "true"
        else :
            self.multiverseEnabled = "false"

        self.trendTimer = int(self.ui.spinBoxTrendUpdate.value())



    def writeScreen(self):
        self.ui.lineEditIpAddress.setText(self.ip )
        self.ui.lineEditPort.setText(self.port)
        self.ui.spinBoxNbrAdcs.setValue(int(self.nbradc))
        self.ui.spinBoxInterval.setValue(int(self.freq) )
        self.ui.lineEditSubname.setText(self.sub )

        if self.multiverseEnabled == "true" :
            self.ui.checkBoxcBridge.setChecked(True)
        else:
            self.ui.checkBoxcBridge.setChecked(False)

        self.ui.spinBoxTrendUpdate.setValue(int(self.trendTimer))


    def SaveConfig(self):
        self.readScreen()
        settings = VSettings("Labjack")

        settings.setValue("ipaddress", self.ip)
        settings.setValue("port", self.port)
        settings.setValue("sub", self.sub)
        settings.setValue("nbradc", self.nbradc)
        settings.setValue("freg", self.freq)
        settings.setValue("trendtime", self.trendTimer)
        settings.setValue("multiverse", self.multiverseEnabled)

    def ReadConfig(self):
        self.readScreen()
        settings = VSettings("Labjack")

        self.ip = settings.value("ipaddress", self.ip)
        self.port = settings.value("port", self.port)
        self.sub = settings.value("sub", self.sub)
        self.nbradc = settings.value("nbradc", self.nbradc)
        self.freq = settings.value("freg", self.freq)
        self.trendTimer = int(settings.value("trendtime", self.trendTimer))
        self.multiverseEnabled = settings.value("multiverse", self.multiverseEnabled)
        self.writeScreen()

    @pyqtSlot()
    def Apply(self):
        self.SaveConfig()
        self.CloseAll()
        self.OpenAll()

    @pyqtSlot()
    def TimeOut(self):
        if self.s1 is not None :
            values = self.s1.ReadAdc()
            self.lastData = values
            if self.cBridge is not None and self.Subscription is not None:
                self.Subscription.UpdateData(values)

            self.n = self.n + 1
            for i in range(0, self.ui.tableWidget.rowCount() ) :
                itm = self.ui.tableWidget.item(i,0)
                if itm == None :
                    itm = QTableWidgetItem()
                    self.ui.tableWidget.setItem(i, 0, itm)

                itm.setText(str(values[i]))
                if i < len(self.trendData) :
                  self.sumData[i] = self.sumData[i] + float(values[i])

    @pyqtSlot()
    def TimeOneSec(self):

        if self.n > 0 :
            for i in range(0, int(self.nbradc) ) :
                value = self.sumData[i] / float(self.n)
                self.sumData[i] = 0.0

                self.trendData[i].insert(0, value)
                if len(self.trendData[i]) > 100:
                    self.trendData[i].pop()

            self.n = 0
            self.graph()

    @pyqtSlot(int, int)
    def on_Active(self, row, col):
        self.currentAdc = row

    pyqtSlot()
    def RestartAttmepts(self):
        if self.cBridge is None or self.cBridge.isConnected() is False:
            self.StartCBridge()

    @pyqtSlot()
    def Exit(self):
        self.CloseAll()
        self.deleteLater()

if __name__ == "__main__":
    show = True

    app = QApplication(sys.argv)

    for i in range(1, len(sys.argv)):
        if sys.argv[i] in ['--hide']:
            show = False

    window = Labjacku6guigeneric()

    if '--hide' in sys.argv:
        print("Hidden Display")
        window.hide()
    else:
        window.show()  # IMPORTANT!!!!! Windows are hidden by default.

    # Start the event loop.
    app.exec_()

    window.CloseAll()


