import pyaudio as pa
import matplotlib.pyplot as plt
import struct
import numpy
from numpy import abs, array, fft, linspace
import time
import threading

FORMAT = pa.paInt16
CHANNELS = 2
RATE = 44100
INDEX = 1
CHUNK = 1024

DELAY = 0.001

threads = []

class Base(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.is_on = False

class Signal(Base):
    def __init__(self):
        super().__init__()
        self.p = pa.PyAudio()
        print(self.p.get_device_info_by_index(INDEX))
        self.stream = self.p.open(  format=FORMAT,
                                    channels=CHANNELS,
                                    rate=RATE,
                                    input=True,
                                    input_device_index=INDEX)
        self.audio_signal = []
    def run(self):
        window = numpy.blackman(CHUNK)
        while self.is_on:
            data = self.stream.read(CHUNK)
            decoded = struct.unpack(str(CHUNK)+'i', data)
            self.audio_signal = array(decoded)*window
            time.sleep(DELAY)

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

class Spectrum(Base):
    def __init__(self):
        super().__init__()
        self.spectrum_x = []
        self.spectrum_y = []
    def run(self):
        Nf = 2**10
        Nf21 = int(Nf/2 + 1)
        while self.is_on:
            w = abs(fft.fft(threads[0].audio_signal, Nf))
            self.spectrum_x = linspace(0, RATE/2, Nf21)
            self.spectrum_y = w[:(Nf21)] 
            time.sleep(DELAY)

class Loop(Base):
    def __init__(self):
        super().__init__()
        self.is_on = False
    def run(self):
        begin = time.time()
        WAIT_SEC = 240
        while self.is_on:
            if time.time() - begin > WAIT_SEC:
                self.stop()
            time.sleep(1)
    def stop(self):
        for t in threads:
            t.is_on = False

class Plot():
    def __init__(self):
        plt.ion()
        fig = plt.figure(figsize=(8,6))
        self.ax1 = fig.add_subplot(211)
        self.ax2 = fig.add_subplot(212)
        self.is_on = False

    def plot(self):
        sensivity_a = 10
        sensivity_b = 10
        while self.is_on:
            self.ax1.cla()
            self.ax1.axis([0,CHUNK,-9**sensivity_a,9**sensivity_a])
            self.ax1.grid()
            self.ax1.plot(threads[0].audio_signal)
            self.ax2.cla()
            self.ax2.grid()
            self.ax2.plot(threads[1].spectrum_x, threads[1].spectrum_y)
            self.ax2.axis([0,20000,0,11**sensivity_b])
            # plt.show()
            plt.pause(DELAY)
    
def start():
    t1 = Signal()
    threads.append(t1)
    t1.is_on = True
    t1.start()
    time.sleep(1)

    t2 = Spectrum()
    threads.append(t2)
    t2.is_on = True
    t2.start()

    t3 = Loop()
    threads.append(t3)
    t3.is_on = True
    t3.start()

    t0 = Plot()
    threads.append(t0)
    t0.is_on = True
    t0.plot()

if __name__ == "__main__":
    start()

