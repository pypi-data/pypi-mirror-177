# Based on u6allio.c
#!python3

import sys
from datetime import datetime
import atexit
import os
import u6


class LabJackU6( ):
    numChannels = 8
    d = None
    differential = False
    resolutionIndex = 1
    gainIndex = 0
    settlingFactor = 0
    latestAinValues = None
    numIterations = 1

    def __init__(self, nbradc = 8, callBack=None):
        super().__init__()
        try:
            self.numChannels = int(8)
        except:
            print("Missing or invalid integer value argument that specifies the number of analog inputs.")
            print("Exiting.")
            sys.exit()


        self.latestAinValues = [0] * self.numChannels
        self.d = u6.U6()
        self.d.getCalibrationData()

        atexit.register(self.close)



    def ReadAdc(self):

        try:
            # Configure the IOs before the test starts

            FIOEIOAnalog = (2 ** self.numChannels) - 1

            fios = FIOEIOAnalog & 0xFF
            eios = FIOEIOAnalog // 256

            self.d.getFeedback(u6.PortDirWrite(Direction=[0, 0, 0], WriteMask=[0, 0, 15]))

            feedbackArguments = []

            feedbackArguments.append(u6.DAC0_8(Value=125))
            feedbackArguments.append(u6.PortStateRead())

            for i in range(self.numChannels):
                feedbackArguments.append(
                    u6.AIN24(i, self.resolutionIndex, self.gainIndex, self.settlingFactor, self.differential))

            start = datetime.now()
            # Call Feedback 1000 (default) times
            i = 0
            while i < self.numIterations:
                results = self.d.getFeedback(feedbackArguments)
                for j in range(self.numChannels):
                    self.latestAinValues[j] = self.d.binaryToCalibratedAnalogVoltage(self.gainIndex, results[2 + j])
                i += 1

            end = datetime.now()
            delta = end - start
         #   print("Time difference: %s" % delta)
         #   dm = delta / self.numIterations

#           print("Time per iteration: %s" % dm)
#           print("Time per iteration in millis: %s" % (dm.microseconds / 1000.0))
#           print("Last readings: %s" % self.latestAinValues)
#
        except :
            self.latestAinValues = [0] * self.numChannels

        return (self.latestAinValues)

    def close(self):
        if self.d is not None :
            self.d.close()
            self.d = None
