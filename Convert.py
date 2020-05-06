import Config

bars_number = Config.get_settings('bars')
tones_range = Config.get_settings('tones')

#! Nf21 used here
bass_range   =   int((tones_range['bass']  /tones_range['max']) * Config.get_settings('spectrum')['Nf21'])
mid_range    =   int((tones_range['mid']   /tones_range['max']) * Config.get_settings('spectrum')['Nf21'])
treble_range =   int((tones_range['treble']/tones_range['max']) * Config.get_settings('spectrum')['Nf21'])


#! it is to upgrade probably - mean better dividing not 1:1:1 but 2:2:1 for eg
def __get_bars_numbers_for_tones__():
    div = bars_number/(len(tones_range)-1)
    bass_bars = int(div)
    mid_bars = int(div)
    treble_bars = int(div)

    bass_bars =int(bass_bars*0.45)
    mid_bars = int(mid_bars*0.4)
    treble_bars = int(treble_bars*0.15)

    if div % 1 != 0.0:
        if div % 1 < 0.5:
            mid_bars += 1 
        elif div % 1 >= 0.5:
            mid_bars += 1
            bass_bars += 1
    flag = True
    while bars_number != (bass_bars+mid_bars+treble_bars):
        if treble_bars == 0:
            treble_bars += 1
        elif flag:
            bass_bars+=1
            flag = False
        else:
            mid_bars+=1
            flag=True
    return [bass_bars+1, mid_bars+1, treble_bars+1]  
tones_bars_numbers = __get_bars_numbers_for_tones__()
print("tones bars numbers", tones_bars_numbers)

def convert_spectrum_to_bars(spectrum, algorithm):
    '''
        convert spectrum to bars, with configuration specified in config file,
        and given algorithm for calculate samples from 'BarsAlgorithms'.
        eg. maxN, meanN
    '''
    y = spectrum
    signals = [ y[0:bass_range], 
                y[bass_range:mid_range], 
                y[mid_range:treble_range]]
    signal = list()
    for i in range(3):
        signal += algorithm(signals[i], n=tones_bars_numbers[i])
    return signal
