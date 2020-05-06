import csv 

class Model:
    model = None

model = Model()

def read(path="here is no path", mapping='f'):
    '''
        return list of data contained in csv file.
        Path to file require - in Windows must be full path eg. "c:/user/xxx/file.csv"
        Mapping options:
        - 'f' - float - by default
        - 'i' - int
    '''
    l = list()
    with open(path, 'r') as f:
        reader = csv.reader(f)
        l = list(reader)
        l = l[0]
        if mapping=='i':
            l = list(map(int, l))
        elif mapping=='f':
            l = list(map(float, l))
    return l

def write(data, path : str):
    '''
        writing data to csv file with given path.
        Path must be full eg. "c:/user/xxx/file.csv"
    '''
    with open("Models/correctionModel.csv", mode='w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(data)

def calculate_model(signal):
    '''
        return model
        calculate given signal on model to correct signal,
        it is for making signal high - lower, and low-higher
    '''
    value = int(max(signal))
    model = list()
    for i in signal:
        x = round(1-i/value, 2)
        if x == 1.0:
            x = 0.0
        model.append(x)
    return model

#! zabezpiecznia dostępu do plików 
def load_model(path="Models/correctionModel.csv"):
    '''
        load model from given path
    '''
    model.model = read(path)

if model.model is None:
    load_model()

def correct_spectrum(spectrum):
    '''
        correct spectrum with model which has been loaded
    '''
    spect = list()
    for i in range(len(spectrum)):
        spect.append(int(spectrum[i]*model.model[i]))
    return spect

#! change it
def create_model(signal_path, model_path):
    '''
        create model from given signal and write it as csv file in given path
    '''
    signal = read("Signals/signal.csv", 'i')
    model = calculate_model(signal)  
    save(model)
    model = read("Models/correctionModel.csv")
0