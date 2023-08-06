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
    