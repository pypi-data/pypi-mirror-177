import numpy as np
from . import Geometry

class Rectangle(Geometry.Geometry):
    def __init__(self, **kwargs):
        Geometry.Geometry.__init__(self, **kwargs)
        self.shape = "rect"
        self.x = kwargs['x']
        self.y = kwargs['y']
        self.rx = kwargs.get('rx', "0")
        self.ry = kwargs.get('ry', "0")
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.non = kwargs['non']
        self.isClosed = True

        w = self.width
        h = self.height
        non = self.non
        edge1x = np.arange(-w/2, w/2, w/non)
        edge1y = np.arange(len(edge1x))*0 - h/2
        edge2y = np.arange(-h/2, h/2, h/(non*h/w))
        edge2x = np.arange(len(edge2y))*0 + w/2
        
        edge3x = np.arange(w/2, -w/2, -w/non)
        edge3y = np.arange(len(edge3x))*0 + h/2
        edge4y = np.arange(h/2, -h/2, -h/(non*h/w))
        edge4x = np.arange(len(edge4y))*0 - w/2
        
        x = np.hstack([edge1x, edge2x, edge3x, edge4x])
        y = np.hstack([edge1y, edge2y, edge3y, edge4y])

        # list of points
        v0 = np.vstack([x, y])*float(self.scale)
        # Rotate the points around itself first
        thr = float(self.rotate)
        R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        vr = np.dot(R,v0)
        # Add Pivot if axis of rotation is not around itself
        if self.pivot != "itself":
            vr = vr + np.array([[self.x], [self.y]]) - np.array([[self.pivot[0]], [self.pivot[1]]])
            # Rotate around the pivot
            thr = float(self.pivotAngle)
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            vr = np.dot(R,vr)
        # Reposition the points
        if self.pivot == "itself":
            position = np.array([self.x, self.y])
        else:
            position = np.array(self.pivot)
        boundaryNodes = position +  np.transpose(vr)
        self.boundaryNodes = boundaryNodes
        segments = []
        for i in range(len(boundaryNodes)-1):
            segments.append([i, i+1])
        segments.append([len(boundaryNodes)-1, 0])
        self.segments = segments

    def show(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], color = self.stroke, lw = float(self.strokeWidth))
        plt.plot(v[[0,i+1],0], v[[0,i+1],1], color = self.stroke, lw = float(self.strokeWidth))

    def showNodes(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], ".", color = self.stroke, markersize = float(self.strokeWidth))
        plt.plot(v[[0,i+1],0], v[[0,i+1],1], ".", color = self.stroke, markersize = float(self.strokeWidth))





