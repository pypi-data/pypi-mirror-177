import numpy as np
from scipy.linalg import solve

class Solver():
    def __init__(self):
        pass

    def solveApproximateMatricesSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.ua = u.copy()
        self.u = u.copy()

    def solveApproximateMatricesScipy(self, A, b):
        self.ua = solve(A, b)
        self.u = self.ua.copy()

    def solveApproximateMatricesNumpy(self, A, b):
        self.ua = np.linalg.lstsq(A, b)[0]
        self.u = self.ua.copy()

    def solveNumericalMatricesSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.un = u.copy()
        self.u = u.copy()

    def solveNumericalMatricesScipy(self, A, b):
        self.un = solve(A, b)
        self.u = self.un.copy()

    def solveNumericalMatricesNumpy(self, A, b):
        self.un = np.linalg.lstsq(A, b)[0]
        self.u = self.un.copy()

    def solveApproximateBoundaryMatricesSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.uab = u.copy()
        self.u = u.copy()

    def solveApproximateBoundaryMatricesScipy(self, A, b):
        self.uab = solve(A, b)
        self.u = self.uab.copy()

    def solveApproximateBoundaryMatricesNumpy(self, A, b):
        self.uab = np.linalg.lstsq(A, b)[0]
        self.u = self.uab.copy()

    def solveNumericalMatricesApproxBoundSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.unab = u.copy()
        self.u = u.copy()

    def solveNumericalMatricesApproxBoundScipy(self, A, b):
        self.unab = solve(A, b)
        self.u = self.unab.copy()

    def solveNumericalMatricesApproxBoundNumpy(self, A, b):
        self.unab = np.linalg.lstsq(A, b)[0]
        self.u = self.unab.copy()

    def solveNumericalMatricesApproxIterBoundSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.unib = u.copy()
        self.u = u.copy()

    def solveNumericalMatricesApproxIterBoundScipy(self, A, b):
        self.unib = solve(A, b)
        self.u = self.unib.copy()

    def solveNumericalMatricesApproxIterBoundNumpy(self, A, b):
        self.unib = np.linalg.lstsq(A, b)[0]
        self.u = self.unib.copy()

    def solveIterBoundaryMatricesSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.uib = u.copy()
        self.u = u.copy()

    def solveIterBoundaryMatricesScipy(self, A, b):
        self.uib = solve(A, b)
        self.u = self.uib.copy()

    def solveIterBoundaryMatricesNumpy(self, A, b):
        self.uib = np.linalg.lstsq(A, b)[0]
        self.u = self.uib.copy()
    
    def solveminiScipy(self, A, b):
        self.miniu = solve(A, b)

    def solveminiNumpy(self, A, b):
        self.miniu = np.linalg.lstsq(A, b)[0]
        
    def solveminiSadiku(self, A, ui, b, target):
        u = ui.copy()
        error = 1

        while (error > target):
            up = u.copy()
            for i in range(len(u)):
                Az = A[i,:].copy()
                Az[i] = 0
                u[i] = (np.matmul(-Az,up)+b[i])/A[i,i]
                
            error = np.amax(np.absolute((u-up)/up*100))

        self.miniu = u.copy()