import numpy as np
from . import Geometry

class Polygon(Geometry.Geometry):
    def __init__(self, **kwargs):
        Geometry.Geometry.__init__(self, **kwargs)
        self.shape = "polygon"
        self.points = kwargs['points']
        self.isClosed = True

        # Scale the points
        v0 = (np.array(self.points)-np.array(self.points[0]))*float(self.scale)
        v0 = np.transpose(v0)
        # Rotate the points around itself first
        thr = float(self.rotate)
        R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        vr = np.dot(R,v0)
        # Add Pivot if axis of rotation is not around itself
        if self.pivot != "itself":
            vr = vr + np.array([[self.points[0][0]], [self.points[0][1]]]) - np.array([[self.pivot[0]], [self.pivot[1]]])
            # Rotate around the pivot
            thr = float(self.pivotAngle)
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            vr = np.dot(R,vr)
        # Reposition the points
        if self.pivot == "itself":
            position = np.array(self.points[0])
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
