import numpy as np
from . import Geometry

class Line(Geometry.Geometry):
    def __init__(self, **kwargs):
        Geometry.Geometry.__init__(self, **kwargs)
        self.shape = "line"
        self.x1 = kwargs['x1']
        self.x2 = kwargs['x2']
        self.y1 = kwargs['y1']
        self.y2 = kwargs['y2']
        self.non = kwargs['non']
        self.isClosed = False

        non = self.non
        if self.x1 == self.x2:
            x = np.arange(int(non))*0 + self.x1
            y = np.arange(self.y1, self.y2, (self.y2-self.y1)/(non-1))
            y = np.hstack([y, self.y2])
        elif self.y1 == self.y2:
            x = np.arange(self.x1, self.x2, (self.x2-self.x1)/(non-1))
            x = np.hstack([x, self.x2])
            y = np.arange(int(non))*0 + self.y1
        else:
            x = np.arange(self.x1, self.x2, (self.x2-self.x1)/(non-1))
            x = np.hstack([x, self.x2])
            y = np.arange(self.y1, self.y2, (self.y2-self.y1)/(non-1))
            y = np.hstack([y, self.y2])

        x = x-x[0]
        y = y-y[0]
        # list of points
        v0 = np.vstack([x, y])*float(self.scale)
        # Rotate the points around itself first
        thr = float(self.rotate)
        R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        vr = np.dot(R,v0)
        # Add Pivot if axis of rotation is not around itself
        if self.pivot != "itself":
            vr = vr + np.array([[self.x1], [self.y1]]) - np.array([[self.pivot[0]], [self.pivot[1]]])
            # Rotate around the pivot
            thr = float(self.pivotAngle)
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            vr = np.dot(R,vr)
        # Reposition the points
        if self.pivot == "itself":
            position = np.array([self.x1, self.y1])
        else:
            position = np.array(self.pivot)
        boundaryNodes = position +  np.transpose(vr)
        self.boundaryNodes = boundaryNodes
        segments = []
        for i in range(len(boundaryNodes)-1):
            segments.append([i, i+1])
        self.segments = segments

    def show(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], color = self.stroke, lw = float(self.strokeWidth))
        
    def showNodes(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], ".", color = self.stroke, markersize = float(self.strokeWidth))