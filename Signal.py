import pyaudio as pa
import struct
import numpy
from numpy import abs, array, fft, linspace

import time
import threading

class Signal:
    def __init__(self):
        self.signal_timeline = []
        self.signal_data = []
        self.fourier_freq = []
        self.fourier_data = []

class Audio(threading.Thread):
    def __init__(self, freq=200, index=1):
        threading.Thread.__init__(self)
        self.daemon = True
        self.is_on = True

        self.FORMAT = pa.paInt16
        self.CHANNELS = 2
        self.RATE = 44100
        self.CHUNK = 2048
        self.DELAY = 1/freq
        self.window = numpy.blackman(self.CHUNK)

        self.p = pa.PyAudio()
        print(self.p.get_device_info_by_index(index))

        self.stream = self.p.open(  
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=index
        )

        self.signal = Signal()
        self.signal.signal_timeline = list(range(0,self.CHUNK))

        self.Nf = 2**11
        self.Nf21 = int(self.Nf/2 + 1)
        self.signal.fourier_freq = linspace(0, self.RATE/2, self.Nf21)

        self.start()

    def get_signal(self):
        '''
            return object of 'Signal' class
        '''
        return self.signal

    def fourier(self):
        w = abs(fft.fft(self.signal.signal_data, self.Nf))
        self.signal.fourier_data = w[:self.Nf21] 

    def run(self):
        while self.is_on:
            data = self.stream.read(self.CHUNK)
            decoded = struct.unpack(str(self.CHUNK)+'i', data)
            self.signal.signal_data = array(decoded)*self.window
            self.fourier()
            time.sleep(self.DELAY)

    def __del__(self):
        self.is_on = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
