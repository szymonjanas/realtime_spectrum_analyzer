import Convert
import ModelCorrection
import BarsAlgorithms
import numpy as np
import copy     
import math
import Volume

def process_spectrum(spectrum):
    y = ModelCorrection.correct_spectrum(spectrum)
    mn = 1*10**7
    mx = 2*10**11
    rangee = mx - mn 
    r = 200
  
    ty = []
    for i in y:
        sample = i
        while sample > mx:
            sample = sample/2
        sample = sample/rangee *r
        if sample > 100:
            sample = 70 + sample%30
        ty.append(sample)
    return Convert.convert_spectrum_to_bars(ty, BarsAlgorithms.maxN)

def process_spectrum_v2(spectrum):
    y = ModelCorrection.correct_spectrum(spectrum)
    return Convert.convert_spectrum_to_bars(y, BarsAlgorithms.maxN)
