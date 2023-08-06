
import numpy as np 
from scipy.interpolate import RectBivariateSpline
import os,shutil,subprocess,sys
from csaps import csaps
from tabulate import tabulate
import time


def getSize(file):
    size = os.path.getsize(file)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1000:
            return f"{round(size,3)} {unit}"
        size /= 1000



def showStats(fileName):
    data = np.loadtxt(fileName)
    table = [
        ["File Name",fileName],
        ["File Size",getSize(fileName)],
        ["Last Modified", time.ctime(os.path.getmtime(fileName))]
    ]


    print("File Info:\n"+"="*55)
    print(tabulate(table,tablefmt="github",floatfmt=".3f"))


    print("\n\nData Shape:\n"+"="*55)
    print(tabulate([data.shape],headers=["Row","Column"],tablefmt="github"))


    headers = ["Sl. No.", "Unique Values", "Minimum", "Maximum"]
    stats = [[i,np.unique(d).shape[0],np.min(d),np.max(d)] for i,d in enumerate(data.T,start=1)]


    print("\n\nData Statistics:\n"+"="*55)
    print(tabulate(stats, headers, tablefmt='github'))



def smoothen(data, shape, tc, pc, cols, sm=0.95):
    data.shape = shape

    grid = [data[:,0,tc], data[0,:, pc]]

    res = np.copy(data)

    for c in cols:
        res[...,c] = csaps(grid, data[...,c], grid, smooth=sm)
    return res




def getShape(data):
    for i in range(data.shape[1]):
        print(np.unique(data[:,i]).shape)



def writeShapedFile(file,data,fmt='%.8f'):
    assert len(data.shape)==3, "A 3D data is required for this function"
    with open(file, 'w') as f:
        for i in data:
            np.savetxt(f,i,delimiter='\t', fmt=fmt)
            f.write('\n')
    


def write2DFile(file,dat,tc=0,fmt='%.8f'):
    with open(file,'w') as f:
        for i in np.unique(dat[:,tc]):
            np.savetxt(f,dat[dat[:,tc]==i],delimiter='\t', fmt=fmt)
            f.write('\n')


def write1DFile(file,dat,fmt='%.8f'):
    np.savetxt(file, dat, delimiter='\t', fmt=fmt)


