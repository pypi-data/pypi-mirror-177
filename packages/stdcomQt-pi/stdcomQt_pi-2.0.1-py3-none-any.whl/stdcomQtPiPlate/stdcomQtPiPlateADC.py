#!
import os

try:
    from PyQt5.QtSvg import QSvgWidget
except ImportError:
    QSvgWidget = None

from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5.QtCore import QElapsedTimer


""" local """
from stdcomQtpi import *

import stdcomQt

from stdcomQt.stdcomQtPjanice import *

from stdcomQt.stdcomQt import *
from stdcomQt.stdcomutilitywidgets import *
from stdcomQt.stdcomvsettings import *

realpi = True

if realpi is True :
    try:
        import piplates.ADCplate as ADC
    except:
        print("Not Reel Pi")
        realpi = False
        import random
else:
    import random


class pjanice(QMainWindow):

    ipW = None

    host = "localhost"
    port = 4897

    pjanice = None
    timer =  QTimer()
    elapsed = QElapsedTimer()
    led = True
    cBridge = None

    SubscriptionAdc = None
    SubscriptionName = "PiPlateAdc"
    address = {}
    timerIntervals = 100



    def __init__(self, parent = None):

        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()

        settings = VSettings("Stec.PJanice")
        self.port = settings.value("pjanice.port", int(self.port))
        self.host = settings.value("pjanice.host", str(self.host))

        self.ui.action_PJanice.triggered.connect(self.slotPjanice)
        self.ui.action_Multiverse.triggered.connect(self.Click)
        self.ui.action_Board.triggered.connect(self.showDialogHelp)
        self.ui.action_About.triggered.connect(self.showDialogAbout)
        self.ui.action_Exit.triggered.connect(self.deleteLater)

        self.ui.tableWidgetValues.setHorizontalHeaderLabels(["0x00","0x1","0x02","0x03", "0x04","0x05", "0x06","0x07" ])

        self.cBridge = stecQSocket(self.host, self.port)
        self.ipW = StecIPconfigDialog(self.callBack, self.cancel, self.host, self.port)
        self.ipW.hide()

        self.ui.pushButtonSave.clicked.connect(self.SaveAdc)
        self.LoadAdc()
        self.readDisplay()

        self.timer.setInterval(self.timerIntervals)
        self.timer.timeout.connect(self.timeOut)

        self.SubscriptionAdc = stdcomQt.Subscriber("piplate.adc.quickandeasy", self.cBridge)
        self.SubscriptionAdc.UpdateDesc("Quick and Easy ADC Example")
        self.timer.start()
        if realpi is False :
            self.showDialog()

        self.elapsed.start()

    def showDialog(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Oh Crap Not Real PiPlate")
        msgBox.setText("Must Set Correct Address, \n or Have PiPlate ADCs \nEntering Emulation Mode")
     #   msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
   #     msgBox.buttonClicked.connect(msgButtonClick)
        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    @pyqtSlot()
    def showDialogAbout(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("Stec PiPlate For ADC")
        msgBox.setText("OPEN SOURCE Stec PiPlate Configureation")

        msgBox.setStandardButtons(QMessageBox.Ok)

        returnValue = msgBox.exec()
        if returnValue == QMessageBox.Ok:
            print('OK clicked')

    @pyqtSlot()
    def showDialogHelp(self):
        try :
            import showHelp
            showHelp.readPdf()
        except :
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("Error")
            msgBox.setText("No Manual, or missing pyPDF2 Package")

            msgBox.setStandardButtons(QMessageBox.Ok)

            returnValue = msgBox.exec()
            if returnValue == QMessageBox.Ok:
                print('OK clicked')



    def readDisplay(self):

        self.SubscriptionName = self.ui.lineEditTagname.text()

        names = { }
        for i in range(0,7) :
            name = "checkBox" + str(i)
            names.update( {name:i} )

        oldSubs = self.address.values()
        for sub in oldSubs :
            sub.deleteLater()

        self.address.clear()

        for checkstate in self.findChildren(QCheckBox):
            name = checkstate.objectName()
            print(f'get check state:{checkstate.checkState()}', "....", name)
            if name in names.keys() :
                state = checkstate.checkState()
                if state == Qt.Checked :
                    adx = names.get(name)
                    if adx is not None :
                        subName = self.SubscriptionName + ".ADC" + str(adx)
                        SubscriptionAdc = stdcomQt.Subscriber(subName, self.cBridge)
                        SubscriptionAdc.UpdateDesc("Quick and Easy ADC Address : " + str(adx))
                        self.address.update ( {int(adx) : SubscriptionAdc} )

        self.timerIntervals = int(self.ui.spinBoxInterval.value())
        self.timer.setInterval(self.timerIntervals)

    @pyqtSlot()
    def SaveAdc(self):
        self.readDisplay()
        settings = VSettings("Stec.PJanice")
        keys = self.address.keys()
        keys = list(keys)
        settings.setValue("addresses", keys )
        settings.setValue("interval", self.timerIntervals)
        settings.setValue("tagname", self.SubscriptionName)


    def LoadAdc(self):

        settings = VSettings("Stec.PJanice")

        self.timerIntervals = int(settings.value("interval", self.timerIntervals))
        self.ui.spinBoxInterval.setValue(self.timerIntervals)

        self.SubscriptionName = settings.value("tagname", self.SubscriptionName)
        self.ui.lineEditTagname.setText(self.SubscriptionName)

        listAddress = list(settings.value("addresses", [0] ))

        for i in range(0, len(listAddress) ) :
            listAddress[i] = int(listAddress[i])


        names = {}
        for i in range(0, 7):
            name = "checkBox" + str(i)
            names.update({name: i})

        for checkstate in self.findChildren(QCheckBox):
            name = checkstate.objectName()
            print(f'get check state:{checkstate.checkState()}', "....", name)
            if name in names.keys():
                address = names.get(name)
                if address in listAddress :
                    checkstate.setCheckState(Qt.Checked)
                else:
                    checkstate.setCheckState(Qt.Unchecked)




    def callBack(self, ip, port):
        print("Address: ", ip, " Service Port: ", port)
        self.ipW.hide()
        self.host = ip
        self.port = port
        settings = VSettings("Stec.PJanice")
        settings.setValue("pjanice.port", self.port)
        settings.setValue("pjanice.host", self.host)
        if self.pjanice is not None :
            self.pjanice.reset(self.host, self.port)


    def cancel(self):
        print("Cancel")
        self.ipW.hide()

    @pyqtSlot()
    def Click(self):
        self.ipW.show()

    @pyqtSlot()
    def slotPjanice(self):
         if self.pjanice is  None:
            self.pjanice = pjanicesimpleGeneric(self.cBridge)

         self.pjanice.show()


    @pyqtSlot()
    def timeOut(self):

        ledChange = False
        if self.elapsed.hasExpired(1000) :
            self.elapsed.restart()
            ledChange = True
            if self.led is True :
                self.led = False
            else :
                self.led = True


        for address in self.address.keys() :
            sub = self.address.get(address)
            col = int(address)

            if realpi is True:
                try:
                    values = list(ADC.getADCall(address))
                    if ledChange:
                        if self.led is True:
                            ADC.setLED(address)
                        else:
                            ADC.clrLED(address)
                except:
                    values = ["Error"] * 12
            else:
                values = []
                for i in range(0, 12):
                    n = random.randint(1, 30)
                    n = (n / 100) + address
                    values.append(n)


            for i in range(0,len(values)) :
                itm = self.ui.tableWidgetValues.item(i,col)
                if itm is None :
                    itm = QTableWidgetItem( str(values[i]))
                    self.ui.tableWidgetValues.setItem(i,col,itm)

                itm.setText(str(values[i]))


            print(values)
            sub.UpdateData(values)


if __name__=="__main__":
    my_parser = argparse.ArgumentParser(description="Version :" + stdcomQt.stdcomQtVersion + " Stec Pjanice2 Python Version")
    current = os.path.dirname(os.path.realpath(__file__))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.
    sys.path.append(parent)
    app = QApplication(sys.argv)
    w = pjanice()
    w.show()

    sys.exit(app.exec_())
