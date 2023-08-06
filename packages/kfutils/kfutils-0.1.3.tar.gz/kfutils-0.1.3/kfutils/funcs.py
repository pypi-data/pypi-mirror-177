
import numpy as np 
from scipy.interpolate import RectBivariateSpline, InterpolatedUnivariateSpline
import os,shutil,subprocess,sys
from csaps import csaps
from tabulate import tabulate
import time


__all__ = ['showStats', 'smoothen', 'writeFile', 'write1DFile', 'repeat', 'mirror','PrepData','rectGridInt','lineGridInt']


def getSize(file):
    size = os.path.getsize(file)
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1000:
            return f"{round(size,3)} {unit}"
        size /= 1000



def showStats(fileName):
    '''
    Show stats about the file.
    '''
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
    '''
    Get details about the shape of the data
    '''
    for i in range(data.shape[1]):
        print(np.unique(data[:,i]).shape)



def writeShapedFile(file,data,fmt='%.8f'):
    ''' Write a Shaped file '''
    assert len(data.shape)==3, "A 3D data is required for this function"
    with open(file, 'w') as f:
        for i in data:
            np.savetxt(f,i,delimiter='\t', fmt=fmt)
            f.write('\n')
    



def write1DFile(file,dat,fmt='%.8f'):
    ''' Write a 1D file'''
    np.savetxt(file, dat, delimiter='\t', fmt=fmt)



def writeFile(file,dat,tc=0,fmt='%.8f'):
    '''Write a 2D file'''
    assert len(dat.shape)==2, "A 2D data is required for this function"

    with open(file,'w') as f:
        for i in np.unique(dat[:,tc]):
            np.savetxt(f,dat[dat[:,tc]==i],delimiter='\t', fmt=fmt)
            f.write('\n')



def lineGridInt(data,fc,newGrid):
    '''Interpolate a 1D data'''
    # make a rectangular data dense or vice versa
    g = data[:,fc]

    ng = np.linspace(g.min(),g.max(),newGrid)

    result = []
    for i in range(data.shape[1]):
        if i==fc:
            res = ng
        else:
            res = InterpolatedUnivariateSpline(g,data[:,i])(ng)
        result.append(res)
    return np.column_stack(result)



def rectGridInt(data, fc, sc, newGrid1, newGrid2):
    '''Interpolate a 2D data'''
    # make a rectangular data dense or vice versa
    g1 = np.unique(data[:,fc])
    g2 = np.unique(data[:,sc])
    c1 = g1.shape[0]
    c2 = g2.shape[0]

    ng1 = np.linspace(g1.min(),g1.max(),newGrid1)
    ng2 = np.linspace(g2.min(),g2.max(),newGrid2)
    ng1m, ng2m = np.meshgrid(ng1, ng2, indexing='ij')

    result = []
    for i in range(data.shape[1]):
        if i==fc:
            res = ng1m.reshape(-1)
        elif i==sc:
            res = ng2m.reshape(-1)
        else:
            res = RectBivariateSpline(g1,g2,data[:,i].reshape(c1,c2))(ng1, ng2).reshape(-1)
        result.append(res)
    return np.column_stack(result)





def mirror(data, fc=0, sc=1, pDiff=1):
    assert len(data.shape)==2, "A 2D array is required"
    # grid has to be in degree, for easy calculation
    data = data[data[:,sc]<=180]  # remove data after 180 phi
    new_ph = np.arange(0,360+pDiff,pDiff)

    res = []
    for th in np.unique(data[:,fc]):
        dat = data[data[:,fc]==th]
        dat = np.vstack([dat, np.flipud(dat[:-1])])  # mirror two times
        dat[:,sc] = new_ph
        res.append(dat)
    return np.vstack(res)



def repeat(data, fc=0, sc=1, pDiff=1):
    assert len(data.shape)==2, "A 2D array is required"

    # grid has to be in degree, for easy calculation
    data = data[data[:,sc]<=120]  # remove data after 120 phi
    new_ph = np.arange(0,360+pDiff,pDiff)

    res = []
    for th in np.unique(data[:,fc]):
        dat = data[data[:,fc]==th]
        dat = np.vstack([dat, dat[1:], dat[1:]])  # repeat three times
        dat[:,sc] = new_ph
        res.append(dat)
    return np.vstack(res)




class PrepData(object):
    # Prepare your data with object chaining
    def __init__(self,fileName):
        try:
            self.data = np.loadtxt(fileName)
        except:
            self.data = np.load(fileName)

    def useCols(self,*cols):
        self.data=self.data[:,cols]
        return self

    def toRad(self,*cols):
        self.data[:,cols] = np.deg2rad(self.data[:,cols])
        return self
    
    def interpTo(self,cols,grid):
        self.data = rectGridInt(self.data, cols[0],cols[1], grid[0], grid[1])
        return self

    def removeNegetive(self,cols=None):
        if cols:
            self.data[:,cols] = np.clip(self.data[:,cols], 0, np.inf)
        else:
            self.data = np.clip(self.data, 0, np.inf)
        return self


    def repeat(self,tC=0,pC=1,pDiff=1):
        self.data = repeat(self.data,fc=tC,sc=pC,pDiff=pDiff)
        return self


    def mirror(self,tC=0,pC=1,pDiff=1):
        self.data = mirror(self.data,fc=tC,sc=pC,pDiff=pDiff)
        return self


    def reshape(self,*shape):
        self.data.shape = shape


    def reshape3D(self,tc=0,pc=1):
        tShape = np.unique(self.data[:,tc]).shape[0]
        pShape = np.unique(self.data[:,pc]).shape[0]
        self.data.shape = (tShape,pShape,-1)
        print(f"Data Reshaped as {self.data.shape}")
        return self


    def getData(self):
        return self.data


    def writeFile(self,fileName,col=0,fmt='%.8f'):
        writeFile(fileName,self.data,tc=col,fmt=fmt) 
        return self
