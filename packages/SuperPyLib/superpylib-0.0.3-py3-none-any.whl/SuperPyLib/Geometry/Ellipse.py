import numpy as np
from . import Geometry

class Ellipse(Geometry.Geometry):
    def __init__(self, **kwargs):
        Geometry.Geometry.__init__(self, **kwargs)
        self.shape = "ellipse"
        self.cx = kwargs['cx']
        self.cy = kwargs['cy']
        self.rx = kwargs['rx']
        self.ry = kwargs['ry']
        self.non = kwargs['non']
        self.isClosed = True

        a = self.rx
        b = self.ry
        th = np.linspace(0,2*np.pi,self.non + 1)
        x = a*np.cos(th[0:-1])
        y = b*np.sin(th[0:-1])

        # list of points
        v0 = np.vstack([x, y])*float(self.scale)
        # Rotate the points around itself first
        thr = float(self.rotate)
        R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        vr = np.dot(R,v0)
        # Add Pivot if axis of rotation is not around itself
        if self.pivot != "itself":
            vr = vr + np.array([[self.cx], [self.cy]]) - np.array([[self.pivot[0]], [self.pivot[1]]])
            # Rotate around the pivot
            thr = float(self.pivotAngle)
            R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
            [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
            vr = np.dot(R,vr)
        # Reposition the points
        if self.pivot == "itself":
            position = np.array([self.cx, self.cy])
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
