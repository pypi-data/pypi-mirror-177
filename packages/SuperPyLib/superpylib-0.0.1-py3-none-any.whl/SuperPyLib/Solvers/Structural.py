from Solvers.Solver import Solver
import numpy as np

class Structural(Solver):
    def __init__(self):
        Solver.__init__(self)
        self.name = "structural"
        self.physicalConstant = 0
        self.proportionalityConstant = 0

    def getStressMatrices(self, mesh, initialDomains):

        x = mesh.rx
        y = mesh.ry
        tri = mesh.tri