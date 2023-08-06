import numpy as np
from . import Geometry

class Point(Geometry.Geometry):
    def __init__(self, **kwargs):
        Geometry.Geometry.__init__(self, **kwargs)
        self.shape = "point"
        self.point = kwargs['point']
        self.isClosed = False

        # Scale the points
        v0 = (np.array(self.point)-np.array(self.point))*float(self.scale)
        v0 = np.transpose(v0)
        # Rotate the points around itself first
        thr = float(self.rotate)
        R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        vr = np.dot(R,v0)
        # Add Pivot if axis of rotation is not around itself
        if self.pivot != "itself":
            vr = vr + np.array([[self.point[0]], [self.point[1]]]) - np.array([[self.pivot[0]], [self.pivot[1]]])
            # Rotate around the pivot
            thr = float(self.pivotAngle)
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            vr = np.dot(R,vr)
        # Reposition the points
        if self.pivot == "itself":
            position = np.array(self.point)
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
        plt.plot(v[0], v[1], "*", color = self.stroke, markersize = float(self.strokeWidth))

    def showNodes(self, plt):
        v = self.boundaryNodes
        plt.plot(v[0], v[1], ".", color = self.stroke, markersize = float(self.strokeWidth))