from Config import Config
import math
import statistics
import copy

class SignalProcessing:
    def __init__(self):
        self.config = Config()
        self.set()

        self.tones_bars_numbers = self.get_bars_numbers_for_tones()
        self.bars_resolutions = self.get_resolution_numbers_for_tones()
        print("BARS tones", self.tones_bars_numbers)
        print("BARS resol", self.bars_resolutions)
        print ("CHECK:", self.bass, self.mid, self.treble)

    def set(self):
        self.bars = self.config.get_settings('bars')
        self.tones = self.config.get_settings('tones')
        self.bass   =   int((self.tones['bass']  /self.tones['max']) * self.config.get_settings('spectrum')['Nf21'])
        self.mid    =   int((self.tones['mid']   /self.tones['max']) * self.config.get_settings('spectrum')['Nf21'])
        self.treble =   int((self.tones['treble']/self.tones['max']) * self.config.get_settings('spectrum')['Nf21'])

    # def convert_spectrum_to_bars(self, y):
    #     yy = []
    #     resolution = int(len(y)/self.bars)
    #     if resolution == 0:
    #         resolution = 1
    #     start_counter = 1
    #     counter = start_counter

    #     sample = 0
    #     for i in y:
    #         if counter < resolution:
    #             sample += i
    #             counter += 1
    #         else:
    #             counter = start_counter
    #             sample = sample/resolution
    #             yy.append(sample)
    #             sample = i
    #             counter += 1              
    #     return yy

    def get_bars_numbers_for_tones(self):
        div = self.bars/(len(self.tones)-1)
        bass_bars = int(div)
        mid_bars = int(div)
        treble_bars = int(div)

        if div % 1 != 0.0:
            if div % 1 < 0.5:
                mid_bars += 1 
            elif div % 1 >= 0.5:
                mid_bars += 1
                bass_bars += 1
        return [bass_bars, mid_bars, treble_bars]  

    def get_resolution_numbers_for_tones(self):
        tab = []
        tab.append(self.get_resolution(self.tones_bars_numbers[0], self.bass))
        tab.append(self.get_resolution(self.tones_bars_numbers[1], self.mid-self.bass))
        tab.append(self.get_resolution(self.tones_bars_numbers[2], self.treble-self.mid))
        while self.bass/tab[0] < self.tones_bars_numbers[0]:
            self.bass += 1
        while (self.mid-self.bass)/tab[1] < self.tones_bars_numbers[1]:
            self.mid += 1
        while (self.treble-self.mid)/tab[2] < self.tones_bars_numbers[2]:
            self.treble += 1
        return tab

    def get_resolution(self, bars_num, signal_length):
        resolution = self.round_down(signal_length/bars_num, 1)
        resolution = math.ceil(resolution)
        if resolution == 0:
            resolution = 1
        return resolution

    def convert_spectrum_to_bars_v2(self, y):
        y = self.make_chart_flatten(y)
        # * signals
        signals = [ y[0:self.bass], 
                    y[self.bass:self.mid], 
                    y[self.mid:self.treble] ]
        signal = self.get_bars_from_signal_part(signals[0], self.bars_resolutions[0])
        signal += self.get_bars_from_signal_part(signals[1], self.bars_resolutions[1])
        signal += self.get_bars_from_signal_part(signals[2], self.bars_resolutions[2])
        return signal

    def get_bars_from_signal_part(self, signal, resolution):
        x = []
        counter = 1
        sample = 0
        for i in signal:
            if counter < resolution:
                sample += i
                counter += 1
            else:
                sample = sample/resolution
                x.append(sample)
                sample = 0
                counter = 1
        if sample != 0:
            sample = sample/counter
            x.append(sample)
        return x      

    def round_down(self, n, decimals=0):
        multiplier = 10 ** decimals
        return math.floor(n * multiplier) / multiplier

    def make_chart_flatten(self, y):
        yy = []
        # yc = copy.deepcopy(y)
        # yc = sorted(yc)
        # xav = statistics.mean(yc)
        # xm = statistics.median(yc)
        for x in y:
            # if x > 1.5*xm and x > xav:
            #     x = x/10
            # i = 2**math.sqrt(1/i) * i**2 - math.sqrt(1/i)
            # i = i - 0.001*i
            x = -1* (1/math.sqrt(2*math.pi)) * (-1*int(x)^2)/2
            yy.append(int(x))
        return yy 
