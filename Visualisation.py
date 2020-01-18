import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

import struct
import pyaudio
from scipy.fftpack import fft

import sys
import time

from Signal import Audio, Signal
from SignalProcessing import SignalProcessing

class AudioStream(object):
    def __init__(self):

        self.signal = Audio()
        self.algorithms = SignalProcessing()

        # pyqtgraph stuff
        pg.setConfigOptions(antialias=True)
        self.traces = dict()
        self.app = QtGui.QApplication([])
        title='Spectrum Analyzer'
        self.win = pg.GraphicsWindow(title=title)
        self.win.setGeometry(400, 250, 600, 300)    

        self.signalPlot = self.win.addPlot(
            title='WAVEFORM', row=1, col=1
        )
        sensivity = 8
        self.signalPlot.setYRange(-10**sensivity, 10**sensivity, padding=0.05)
        self.signalPlot.setXRange(0, 2048-1, padding=0.05)
        self.plotSignal = self.signalPlot.plot(pen='c', width=3)
        
        self.spectrumPlot = self.win.addPlot(
            title='SPECTRUM', row=2, col=1
        )
        self.spectrumPlot.setYRange(0, 10**(sensivity+2))
        self.spectrumPlot.setXRange(0, 20000)
        self.plotSpectrum = self.spectrumPlot.plot(pen='m', width=3)

        self.spectrumPlotBar = self.win.addPlot(
            title='SPECTRUM BARS', row=3, col=1
        )
        self.spectrumPlotBar.setYRange(0, 10**(sensivity+1))
        self.plotSpectrumBar = self.spectrumPlotBar.plot(pen='r', width=3, stepMode=True)

        self.item = pg.PlotDataItem()
        

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def convert_to_qt__bar_chart(self, y):
        yy = []
        yy.append(0)
        yy.append(0)
        for i in y:
            yy.append(i)
            yy.append(i)
            yy.append(0)
            yy.append(0)
        x = range(0, len(yy)+1)
        return [x, yy]

    def set_plotdata(self):
        sig = self.signal.get_signal()
        self.plotSignal.setData(sig.signal_timeline, sig.signal_data)
        self.plotSpectrum.setData(sig.fourier_freq, sig.fourier_data)
        data = self.convert_to_qt__bar_chart(self.algorithms.convert_spectrum_to_bars_v2(sig.fourier_data.tolist()))
        self.plotSpectrumBar.setData(data[0], data[1])

    def update(self):
        self.set_plotdata()

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(20)
        self.start()

if __name__ == '__main__':

    audio_app = AudioStream()
    audio_app.animation()
