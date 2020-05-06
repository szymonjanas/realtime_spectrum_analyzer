import pyaudio as pa
import struct
import numpy
from numpy import abs, array, fft, linspace

import time
import threading
import Config

class Signal:
    def __init__(self):
        self.samples_timeline = []
        self.samples = []
        self.spectrum_freq = []
        self.spectrum = []

#! zmienić to na ustawienia ładowane z pliku
#! automatyczne wykrywanie sterowników karty dźwiękowej
class Audio(threading.Thread):
    def __init__(self, index=1):
        threading.Thread.__init__(self)
        self.daemon = True
        self.is_on = True

        self.p = pa.PyAudio()
        self.FORMAT = pa.paInt16
        self.CHANNELS = int(self.p.get_device_info_by_index(index)['maxInputChannels'])
        self.RATE = int(self.p.get_device_info_by_index(index)['defaultSampleRate'])
        self.CHUNK = Config.get_settings('signal')['CHUNK']
        self.DELAY = 1/Config.get_settings('frequency')['Signal']
        self.window = numpy.blackman(self.CHUNK)  

        self.stream = self.p.open(  
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=index
        )

        self.signal = Signal()
        self.signal.samples_timeline = list(range(0,self.CHUNK))

        self.Nf21 = Config.get_settings('spectrum')['Nf21']
        self.signal.spectrum_freq = linspace(0, self.RATE/2, self.Nf21)

        self.start()

    def get_signal(self):
        '''
            return object of 'Signal' class
        '''
        return self.signal

    def __spectrum__(self):
        '''
            calculate spectrum
        '''
        w = abs(fft.fft(self.signal.samples, (self.Nf21-1)*2))
        self.signal.spectrum = w[:self.Nf21] 

    def run(self):
        while self.is_on:
            data = self.stream.read(self.CHUNK)
            decoded = struct.unpack(str(self.CHUNK)+'i', data)
            self.signal.samples = array(decoded)*self.window
            self.__spectrum__()
            time.sleep(self.DELAY)
        
    def __del__(self):
        self.is_on = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

def set_audio(index=-1):
    if index == -1:
        p = pa.PyAudio()
        count = p.get_device_count()
        for i in range(count):
            if (p.get_device_info_by_index(i)["name"] == Config.get_settings("device")):
                return Audio(i)
                
audio = set_audio()

def get_audio():
    return audio

def get_signal():
    '''
        return object of Signal class
        
    '''
    return audio.get_signal()

