import numpy as np

class Geometry:

    def __init__(self, **kwargs):
        self.stroke = kwargs.get('stroke', "black")
        self.strokeWidth = kwargs.get('strokeWidth', "1")
        self.fill = kwargs.get('fill', "transparent")
        self.non = kwargs.get('non', "0")
        self.relativeDensity = kwargs.get('relativeDensity', "[1, 1]")
        self.scale = kwargs.get('scale', "1")
        self.rotate = kwargs.get('rotate', "0")
        self.pivot = kwargs.get('pivot', "itself")
        self.pivotAngle = kwargs.get('pivotAngle', "0")
        self.parent = []
        self.child = []
        self.isParent = True
        self.isChild = True
        self.isHole = kwargs.get('isHole', False) # Work on it later
        self.source = 0
        self.material = 1




class Circle(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
        self.shape = "circle"
        self.cx = kwargs['cx']
        self.cy = kwargs['cy']
        self.r = kwargs['r']
        self.non = kwargs['non']
        self.isClosed = True

        r = self.r
        th = np.linspace(0,2*np.pi,self.non +1)
        x = r*np.cos(th[0:-1])
        y = r*np.sin(th[0:-1])

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




class Ellipse(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
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




class Line(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
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




class Point(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
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




class Polygon(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
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




class Polyline(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
        self.shape = "polyline"
        self.points = kwargs['points']
        self.isClosed = False

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
        self.segments = segments

    def show(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], color = self.stroke, lw = float(self.strokeWidth))

    def showNodes(self, plt):
        v = self.boundaryNodes
        for i in range(len(v)-1):
            plt.plot(v[[i,i+1],0], v[[i,i+1],1], ".", color = self.stroke, markersize = float(self.strokeWidth))
        
        


class Rectangle(Geometry):

    def __init__(self, **kwargs):
        Geometry.__init__(self, **kwargs)
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





