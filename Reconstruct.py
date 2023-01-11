from csv import reader
import csv
from operator import matmul
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
from copy import deepcopy


def csvreadline(file, outputfilename):
    '''
    Reads the imported csv line by line and groups them into bactches of 3 rows
    The batches of 3 rows are then called with sort() to sort them into the finalized array
    '''
    rows = 0
    triplerow = []
    count = 0
    totalRows = 1
    with open(file, 'r') as read_obj1:
        csv_reader1 = reader(read_obj1)  #  read line by line so only one line is in emmory at a time
        header1 = next(csv_reader1)  # skips the header row at the top of the csv
        if header1 != None:
            for row1 in csv_reader1:
                totalRows +=1
    
    #  Opens the csv file in read mode
    with open(file, 'r') as read_obj:
        csv_reader = reader(read_obj)  #  read line by line so only one line is in emmory at a time
        header = next(csv_reader)  # skips the header row at the top of the csv
        if header != None:
            for row in csv_reader:
                progress_bar(count,totalRows,40)
                triplerow.append(row)  # appends row in memory to 'triple row'
                rows += 1
                if rows == 3:  #  if three rows are in it calls sort() and resets the triplerow container and row counter
                    sort(triplerow, outputfilename)
                    triplerow = []
                    rows = 0
                count +=1
def progress_bar(current, total, bar_length):
    fraction = current / total
    arrow = int(fraction * bar_length - 1) * '-' + '>'
    padding = int(bar_length - len(arrow)) * ' '

    ending = '\n' if current == total else '\r'
    print(f'Progress: [{arrow}{padding}] {int(fraction*100)}%', end=ending)
                        
def sort(rows, outputfilename):
    '''
    This sorts the recieved 'triple row' into its repsective spot in the sorted array list
    For example sorted[10][42] represents the 11th aquisition at the (42+30) 72 m/z
    '''
    sorted_row = [0]*1200  #  makes the empty list of 0s for array
    count = 0
    row1 = rows[0]
    for item in rows[0]:
        if count > 1:
            if item != '':
                position = round(float(item)) - 30
                index = row1.index(item)
                value = rows[1][index]
                sorted_row[position] = value
        count += 1
    writeline(sorted_row, outputfilename)
    del(sorted_row)
        
def writeline(sorted_row, outputfilename):
    with open(outputfilename, 'a', newline= '') as f:
        writer = csv.writer(f)
        writer.writerow(sorted_row)
        
def reconstruct1D(matrixfile, modulation, acqusition,outName):
    mod = int(acqusition*modulation)
    mat = []
    mat = pd.read_csv(matrixfile).to_numpy()
    tl = np.mod(np.size(mat, axis=0), mod)
    tl = np.ceil(tl).astype(int)
    mat = mat[:-tl, :]
    tnsr = mat.reshape(int(np.size(mat, axis=0) / mod), mod, np.size(mat, axis=1))
    mat2 = np.sum(np.sum(tnsr, axis=1), axis=1)
    del(tnsr)
    plt.plot(mat2, linewidth=0.75) #aspect='auto'
    plt.xlabel('Retention Time')
    plt.ylabel('Abundance')
    depart = outName.rsplit('\\',1)
    outputP = depart[0]
    outputName = depart[1]
    outputPath = outputP+'\\output\\'+outputName+'.png'
    num = 0
    while os.path.isfile(outputPath):
        outputPath = outputP+'\\output\\'+outputName+str(num)+'.png'
        num = num+1
    plt.savefig(outputPath)
    plt.figure().clear()

def process(inputfilename, modulation, acquisition_rate):
    
    outputfilename = inputfilename[:-4]
    outputfilename = outputfilename + 'MatrixOutput.csv'
    # Reads raw data and converts to readable matrix
    csvreadline(inputfilename, outputfilename)
    # Reads matrix and reconstucts 1D
    reconstruct1D(outputfilename, modulation, acquisition_rate,inputfilename[:-4])  
    os.remove(outputfilename)

    
def runReconstruct(inputfilename,modulation,acquisition_rate):
    # inputfilename = 'small_test.csv' # Example: '202200506_DL_1_Hex_BL_70eV.csv'
    # modulation = 2.2  # Change this value to the modulation period in seconds
    # acquisition_rate = 100  # Change this value to the acquisition rate in Hz
    try:
        process(inputfilename, float(modulation), float(acquisition_rate))    
        return 'success'
    except Exception as e:
        return str(e)

