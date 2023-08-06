from Solvers.Solver import Solver
import numpy as np

class Thermostatic(Solver):
    def __init__(self):
        Solver.__init__(self)
        self.name = "thermoostatic"
        self.family = "thermal"
        self.physicalConstant = 1
        self.proportionalityConstant = self.physicalConstant/(2*np.pi)

    def getApproximateMatrices(self, mesh, shapes):
        x = mesh.x
        y = mesh.y
        tri = mesh.conmat
        nn = len(x)
        ne = len(tri[:,0])
        pc = self.proportionalityConstant
        A = np.zeros((nn,nn))
        b = np.zeros((nn,1))
        nodeSource = mesh.nodeSource
        for i in range(ne):
            print("Percentage of elements covered", i/ne*100, end='\r')
            # 0-1 edge
            k = 0
            l = 1
            Ex = 0
            Ey = 0
            for shape in shapes:
                if not shape.isClosed:
                    nodes = shape.boundaryList
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
                else:
                    nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
            rx = x[tri[i,l]] - x[tri[i,k]]
            ry = y[tri[i,l]] - y[tri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[tri[i,k], tri[i,k]] = A[tri[i,k], tri[i,k]] +1
            A[tri[i,k], tri[i,l]] = -1
            b[tri[i,k]]           = b[tri[i,k]] + Er*np.sqrt(rx**2+ry**2)

            # 1-2 edge
            k = 1
            l = 2
            Ex = 0
            Ey = 0
            for shape in shapes:
                if not shape.isClosed:
                    nodes = shape.boundaryList
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
                else:
                    nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
            rx = x[tri[i,l]] - x[tri[i,k]]
            ry = y[tri[i,l]] - y[tri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[tri[i,k], tri[i,k]] = A[tri[i,k], tri[i,k]] +1
            A[tri[i,k], tri[i,l]] = -1
            b[tri[i,k]]           = b[tri[i,k]] + Er*np.sqrt(rx**2+ry**2)

            # 2-0 edge
            k = 2
            l = 0
            Ex = 0
            Ey = 0
            for shape in shapes:
                if not shape.isClosed:
                    nodes = shape.boundaryList
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
                else:
                    nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[tri[i,k]] + x[tri[i,l]])/2 - px
                            Ry = (y[tri[i,k]] + y[tri[i,l]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
            rx = x[tri[i,l]] - x[tri[i,k]]
            ry = y[tri[i,l]] - y[tri[i,k]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[tri[i,k], tri[i,k]] = A[tri[i,k], tri[i,k]] +1
            A[tri[i,k], tri[i,l]] = -1
            b[tri[i,k]]           = b[tri[i,k]] + Er*np.sqrt(rx**2+ry**2)

        print()
        self.Aa = A
        self.ba = b

    def getLinNumericalMatrix(self, mesh):
        x = mesh.x
        y = mesh.y
        tri = mesh.conmat
        nn = len(x)
        A = np.zeros((nn,nn))

        count = 0
        ne = len(tri[:,0])
        for i in range(ne):
            print("percentage of linear elements covered", count/ne*100, end='\r')
            count = count +1
            ex = np.array([x[tri[i,0]], x[tri[i,1]], x[tri[i,2]]])
            ey = np.array([y[tri[i,0]], y[tri[i,1]], y[tri[i,2]]])
            p = np.array([ey[1]-ey[2], ey[2]-ey[0], ey[0]-ey[1]])
            q = np.array([ex[2]-ex[1], ex[0]-ex[2], ex[1]-ex[0]])
            ea = 0.5*abs(p[1]*q[2]-q[1]*p[2])
            P = np.zeros([len(p),len(p)])
            Q = P.copy()
            for j in range(len(p)):
                P[j] = p*p[j]
                Q[j] = q*q[j]

            a = (P+Q)/(4*ea)
            for k in range(3):
                for j in range(3):
                    A[tri[i,k],tri[i,j]] = A[tri[i,k],tri[i,j]].copy() + a[k,j]

        print()
        self.AnLin = A.copy()

    def getNumericalMatrix(self, mesh):
        x = mesh.x
        y = mesh.y
        tri = mesh.conmat
        nn = len(x)
        A = np.zeros((nn,nn))
        ur = mesh.elementMaterial

        count = 0
        ne = len(tri[:,0])
        for i in range(ne):
            print("percentage of non-linear elements covered", count/ne*100, end='\r')
            count = count +1
            ex = np.array([x[tri[i,0]], x[tri[i,1]], x[tri[i,2]]])
            ey = np.array([y[tri[i,0]], y[tri[i,1]], y[tri[i,2]]])
            p = np.array([ey[1]-ey[2], ey[2]-ey[0], ey[0]-ey[1]])
            q = np.array([ex[2]-ex[1], ex[0]-ex[2], ex[1]-ex[0]])
            ea = 0.5*abs(p[1]*q[2]-q[1]*p[2])
            P = np.zeros([len(p),len(p)])
            Q = P.copy()
            for j in range(len(p)):
                P[j] = p*p[j]
                Q[j] = q*q[j]

            a = (P+Q)/(4*ea*ur[i])
            for k in range(3):
                for j in range(3):
                    A[tri[i,k],tri[i,j]] = A[tri[i,k],tri[i,j]].copy() + a[k,j]

        print()
        self.An = A.copy()

    def getApproximateBoundaryMatrices(self, mesh, shapes):
        x = mesh.x
        y = mesh.y
        tri = mesh.conmat
        pc = self.proportionalityConstant

        # Boundary nodes
        for i in range(len(shapes)):
            if len(shapes[i].parent) == 0:
                gs = i
                break

        lbn = shapes[gs].boundaryList
        lbn = lbn.astype(int)
        nbn = len(lbn)

        # Initializing matrices
        A = np.zeros([nbn,nbn])
        b = np.zeros([nbn,1])

        nodeSource = mesh.nodeSource

        for i in range(nbn):
            
            Ex = 0
            Ey = 0
            for shape in shapes:
                if not shape.isClosed:
                    nodes = shape.boundaryList
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[lbn[i-1]] + x[lbn[i]])/2 - px
                            Ry = (y[lbn[i-1]] + y[lbn[i]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
                else:
                    nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[lbn[i-1]] + x[lbn[i]])/2 - px
                            Ry = (y[lbn[i-1]] + y[lbn[i]])/2 - py
                            Ex = Ex + nodeSource[node]*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2

            # Forward Segment
            rx = x[lbn[i]] - x[lbn[i-1]]
            ry = y[lbn[i]] - y[lbn[i-1]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[i-1, i-1] = A[i-1, i-1] +1
            A[i-1, i] = -1
            b[i-1]           = b[i-1] + Er*np.sqrt(rx**2+ry**2)

            # Backward Segment
            rx = x[lbn[i-1]] - x[lbn[i]]
            ry = y[lbn[i-1]] - y[lbn[i]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[i, i] = A[i, i] +1
            A[i, i-1] = -1
            b[i]           = b[i] + Er*np.sqrt(rx**2+ry**2)

        self.Aab = A
        self.bab = b

    def getIterBoundaryMatrices(self, mesh, shapes, bt):
        x = mesh.x
        y = mesh.y
        u0 = self.physicalConstant
        pc = self.proportionalityConstant

        # Boundary nodes
        for i in range(len(shapes)):
            if len(shapes[i].parent) == 0:
                gs = i
                break

        lbn = shapes[gs].boundaryList
        lbn = lbn.astype(int)
        nbn = len(lbn)

        # Initializing matrices
        A = np.zeros([nbn,nbn])
        b = np.zeros([nbn,1])

        nodeSource = bt.copy()
        nodeSource[lbn] = 0
        for i in range(nbn):
            
            Ex = 0
            Ey = 0
            for shape in shapes:
                if not shape.isClosed:
                    nodes = shape.boundaryList
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[lbn[i-1]] + x[lbn[i]])/2 - px
                            Ry = (y[lbn[i-1]] + y[lbn[i]])/2 - py
                            Ex = Ex + nodeSource[node]/u0*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]/u0*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2
                else:
                    nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
                    for node in nodes:
                        if nodeSource[node] != 0:
                            px = x[node]
                            py = y[node]
                            Rx = (x[lbn[i-1]] + x[lbn[i]])/2 - px
                            Ry = (y[lbn[i-1]] + y[lbn[i]])/2 - py
                            Ex = Ex + nodeSource[node]/u0*pc*Rx/(np.sqrt(Rx**2 + Ry**2))**2
                            Ey = Ey + nodeSource[node]/u0*pc*Ry/(np.sqrt(Rx**2 + Ry**2))**2

            # Forward Segment
            rx = x[lbn[i]] - x[lbn[i-1]]
            ry = y[lbn[i]] - y[lbn[i-1]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[i-1, i-1] = A[i-1, i-1] +1
            A[i-1, i] = -1
            b[i-1]           = b[i-1] + Er*np.sqrt(rx**2+ry**2)

            # Backward Segment
            rx = x[lbn[i-1]] - x[lbn[i]]
            ry = y[lbn[i-1]] - y[lbn[i]]
            Er = np.dot([Ex[0], Ey[0]], [rx, ry]/np.sqrt(rx**2+ry**2))
            A[i, i] = A[i, i] +1
            A[i, i-1] = -1
            b[i]           = b[i] + Er*np.sqrt(rx**2+ry**2)

        self.Aib = A
        self.bib = b

    def getMiniLinNumericalMatrix(self, minix, miniy, miniTri):
        x = minix
        y = miniy
        tri = miniTri
        nn = len(x)
        A = np.zeros((nn,nn))

        count = 0
        ne = len(tri[:,0])
        for i in range(ne):
            print("percentage of linear elements covered", count/ne*100, end='\r')
            count = count +1
            ex = np.array([x[tri[i,0]], x[tri[i,1]], x[tri[i,2]]])
            ey = np.array([y[tri[i,0]], y[tri[i,1]], y[tri[i,2]]])
            p = np.array([ey[1]-ey[2], ey[2]-ey[0], ey[0]-ey[1]])
            q = np.array([ex[2]-ex[1], ex[0]-ex[2], ex[1]-ex[0]])
            ea = 0.5*abs(p[1]*q[2]-q[1]*p[2])
            P = np.zeros([len(p),len(p)])
            Q = P.copy()
            for j in range(len(p)):
                P[j] = p*p[j]
                Q[j] = q*q[j]

            a = (P+Q)/(4*ea)
            for k in range(3):
                for j in range(3):
                    A[tri[i,k],tri[i,j]] = A[tri[i,k],tri[i,j]].copy() + a[k,j]

        # print()
        self.miniAn = A.copy()

    def findVectorFields(self, mesh, solver):
        x = mesh.x
        y = mesh.y
        u = solver.u.copy()

        Ex = np.zeros([len(x),1])
        Ey = np.zeros([len(x),1])
        neiNodes = mesh.neiNodes

        for i in range(len(x)):
            nNodes = neiNodes[i]
            for node in nNodes:
                rx = x[node]-x[i]
                ry = y[node]-y[i]
                Ex[i] = Ex[i] + (u[i] - u[node]) * rx / (np.sqrt(rx**2 + ry**2))**2
                Ey[i] = Ey[i] + (u[i] - u[node]) * ry / (np.sqrt(rx**2 + ry**2))**2

        # thr = 90
        # R = np.array([[np.cos(np.radians(thr)), -np.sin(np.radians(thr))],
        # [np.sin(np.radians(thr)), np.cos(np.radians(thr))]])
        
        # for i in range(len(Ex)):
        #     Ex[i], Ey[i] = np.dot(R,np.array([Ex[i], Ey[i]]))[0], np.dot(R,np.array([Ex[i], Ey[i]]))[1]
        
        solver.Ex = Ex
        solver.Ey = Ey
