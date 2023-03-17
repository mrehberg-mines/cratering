import pandas as pd 
import numpy as np
import os
import matplotlib.pyplot as plt
import random
from sklearn.preprocessing import normalize

global dimension, materialStartHeight

def normalize_2d(matrix):
    # Only this is changed to use 2-norm put 2 instead of 1
    norm = np.linalg.norm(matrix, 1)
    # normalized matrix
    matrix = matrix/norm 
    return matrix



def createBase(materialStartHeight):
    # This function just creates an array    
    base = np.zeros((dimension, dimension))
    base.fill(materialStartHeight)
    return base

def determineCraterShape(cx, cy, D,  regolith):
    # Right now this does not do anything
    if regolith[cx, cy] > 0.26 *D:
        shape = 'Normal'
    elif regolith[cx, cy] < 0.26*D and regolith[cx, cy] > 0.11*D:
        shape = 'Flat Bottomed'
    elif regolith[cx, cy] < 0.11*D and regolith[cx, cy] > 0.02*D:
        shape = 'Concentric'
    else:
        shape = 'Hardrock'
    return shape

def createCraterDepth(cx, cy, D, rings, shape, base, regolith, proto):
    # this funciton creates the crater on the base/regolith/proto map
    # It will first do the base map by setting the crater area to the center point (contact point)
    # and then subrating a crater shape
    # The mass loss is first taken from the regolith
    # Regolith cannot be negative though
    # So anything that is negative is taken from the proto
    x = np.arange(0, dimension)
    y = np.arange(0, dimension)
    baseMask = np.zeros((y.size, x.size))

    maxDepth = D/3.7
    rangeRings = max(1, int(D/rings))
    # create crater decrease
    for d in range(0,D,rangeRings):
        temp = np.zeros((y.size, x.size))
        d_new = D-d
        r = d_new/2
        mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < (r)**2
        temp[mask] = -1 * (d/D)**.3
        baseMask = baseMask + temp
        # normalize
    baseMask = normalize_2d(baseMask)
    craterMask = baseMask * maxDepth
    
    # define crater
    startHeight = base[cx, cy]
    startingVolume = np.sum(base)
    base[mask] = startHeight
    base += craterMask
    
    # subtract the regolith
    regolith+= craterMask 
    # if the regolith is below zero, subtrack the proto
    protoMask = regolith < 0
    proto[protoMask] = proto[protoMask] + regolith[protoMask]
    regolith[protoMask] = 0
    
    endingVolume = np.sum(base)
    volume = startingVolume - endingVolume
    return volume, base, regolith, proto

def createCraterEjecta(cx, cy, D, rings, volume):
    # This takes the volume of regolith removed from the crater
    # and maps it in a 2.5x circle aronud the crater
    x = np.arange(0, dimension)
    y = np.arange(0, dimension)
    baseMask = np.zeros((y.size, x.size))

    maxD = int(D*2.5)
    # create crater increase
    for d in range(D,maxD,rings):
        temp = np.zeros((y.size, x.size))
        r = d/2
        mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < (r)**2
        temp[mask] = ((d-D)/D)**.333
        baseMask = baseMask + temp
    # Erase the crater
    mask = (x[np.newaxis,:]-cx)**2 + (y[:,np.newaxis]-cy)**2 < (D/2)**2
    baseMask[mask] = 0
    # normalize
    baseMask = normalize_2d(baseMask)
    craterEjectaMask = baseMask * volume / np.sum(baseMask)
    return craterEjectaMask

def craterParams(maxCraterDiameter):
    # Randomly generates a crater size and contact point
    cx = int(random.random()*dimension)
    cy = int(random.random()*dimension)  
    D  = int(random.random()*maxCraterDiameter)+10
    return cx, cy, D

def graph(base, title):
    # Makes the color plots
    plt.figure(figsize=(6, 6))
    plt.pcolormesh(base)
    plt.colorbar()
    plt.title(title)
    plt.savefig(f'Figures\\{title}')
    plt.show()
    return

def plotOutputs(outputs, title):
    fig, ax = plt.subplots(figsize=(10,6))
    ax.plot(outputs)
    ax.set_xlabel('Number of Craters')
    ax.set_ylabel(title)
    ax.set_title(title)
    plt.savefig( f'Figures\\{title}')
    plt.show()
    return

def main(numCraters, maxCraterDiameter, materialStartHeight, rings):
    base = createBase(0)
    regolith = createBase(0)
    proto = createBase(0)
    outputs = []
    for crater in range(numCraters):
        # Create a random crater size
        cx, cy, D = craterParams(maxCraterDiameter)
        # Determine if the crater has landed in fresh protolith, or if it only impacted regolith
        shape = determineCraterShape(cx, cy, D, regolith)
        # TODO use the shape parameter to calculate an actual volume
        # Right now volume is just set to a rough calculation
        # This function creates a mask for the amount of material that is subtracted from the protolith
        # and a mask for the displaced regolith
        volume, base, regolith, proto = createCraterDepth(cx, cy, D, rings, shape, base, regolith, proto)
        # This function adds thes subtracted regolith to the surrounding area
        # The rings variable is a degree of granularity
        regolithMask = createCraterEjecta(cx, cy, D, rings, volume)
        regolith += regolithMask 
        base += regolithMask
        outputs.append(np.mean(regolith))
        # outputs.append(newRegolithRatio)
    graph(base, 'Surface Height')
    graph(regolith, 'Regolith Height')
    graph(proto, 'Protolith Height')
    # Check to make sure there is minimal difference in the total mass
    print(np.sum(regolith+proto))
    outputs = pd.DataFrame(outputs)
    plotOutputs(outputs, 'Mean Regolith Height')
    return 


if __name__ == "__main__":
    dimension = 1000
    numCraters = 800
    maxCraterDiameter = 300
    materialStartHeight = 0
    # the ring variable is the granularity of calcing the craters
    # If it is too high, it tends to break some divide by 0 stuff
    rings = 10
    random.seed(43)
    main(numCraters, maxCraterDiameter, materialStartHeight, rings)

