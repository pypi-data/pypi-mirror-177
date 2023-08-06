import matplotlib.pyplot as plt
import numpy as np

import PlotUtils
from scipy.spatial import Delaunay as delaunay
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint

class Mesh:
    def __init__(self, x, y, conmat):
        self.x = x
        self.y = y
        self.conmat = conmat

    def getNeiElements(self):
        nn = len(self.x)
        ne = len(self.conmat[:,0])
        neiElements = []
        for i in range(nn):
            ele = []
            for j in range(ne):
                if self.conmat[j,0] == i or self.conmat[j,1] == i or self.conmat[j,2] == i:
                    ele.append(j)
            neiElements.append(ele)
        self.neiElements = neiElements

    def getNeiNodes(self):
        nn = len(self.x)
        neiNodes = []
        for i in range(nn):
            nod = []
            for j in self.neiElements[i]:
                for k in self.conmat[j]:
                    if k != i: 
                        nod.append(k)
            nod = np.unique(np.array(nod))
            nod = nod.tolist()
            neiNodes.append(nod)
        self.neiNodes = neiNodes
        
def prepareGeometryForMeshing(shapes):
    # Finding all child shapes
    for i in range(len(shapes)): # for all shapes,
        if shapes[i].isClosed: # if the current shape is closed, it may contain a child.
            for j in range(len(shapes)): # for all potential child shapes,
                if i != j: # skip current shape as potential child.
                    polygon = ShapelyPolygon(shapes[i].boundaryNodes) # consider current shape as polygon,
                    if shapes[j].shape == "point":
                        point = ShapelyPoint(shapes[j].boundaryNodes) # and take one point form potential child shape.
                    else:
                        point = ShapelyPoint(shapes[j].boundaryNodes[0]) # and take one point form potential child shape.
                    if polygon.contains(point): # if one point of potential child shape is inside current shape,
                        shapes[i].child.append(j) # potential child shape is a child of current shape. Note: all the shapes must be non-contacting.

    # Finding all parent shapes
    for i in range(len(shapes)): # for all shapes,
        for j in range(len(shapes)): # for all potential parent shapes,
            if i != j: # skip current shape as potential parent.
                if shapes[j].isClosed: # if the potential shape is closed, it may be a parent.
                    polygon = ShapelyPolygon(shapes[j].boundaryNodes) # consider potential parent shape as polygon,
                    if shapes[i].shape == "point":
                        point = ShapelyPoint(shapes[i].boundaryNodes) # and take one point from current shape.
                    else:
                        point = ShapelyPoint(shapes[i].boundaryNodes[0]) # and take one point from current shape.
                    if polygon.contains(point): # if one point of current shape is inside the potential parent shape,
                        shapes[i].parent.append(j) # potential parent shape is the parent of current shape. Note: all the shapes must be non-contacting.

    for i in range(len(shapes)):
        shapes[i].parent = np.array(shapes[i].parent)
        shapes[i].child = np.array(shapes[i].child)

    # Finding immediate child shapes
    listOfShapesToRemove = []
    for i in range(len(shapes)):
        shapesToRemove = []
        for j in range(len(shapes[i].child)):
            for k in range(len(shapes[shapes[i].child[j]].child)):
                shapesToRemove.append(shapes[shapes[i].child[j]].child[k])
        listOfShapesToRemove.append(shapesToRemove)

    for i in range(len(shapes)):
        for j in range(len(listOfShapesToRemove[i])):
            shapes[i].child = np.delete(shapes[i].child, np.where(shapes[i].child == listOfShapesToRemove[i][j]))#, axis=0)

    # Finding immediate parent shapes
    listOfShapesToRemove = []
    for i in range(len(shapes)):
        shapesToRemove = []
        for j in range(len(shapes[i].parent)):
            for k in range(len(shapes[shapes[i].parent[j]].parent)):
                shapesToRemove.append(shapes[shapes[i].parent[j]].parent[k])
        listOfShapesToRemove.append(shapesToRemove)
        
    for i in range(len(shapes)):
        for j in range(len(listOfShapesToRemove[i])):
            shapes[i].parent = np.delete(shapes[i].parent, np.where(shapes[i].parent ==listOfShapesToRemove[i][j]))#, axis=0)

    # Labelling if a shape is child or parent
    for i in range(len(shapes)):
        if len(shapes[i].child) == 0:
            shapes[i].isParent = False
        else:
            shapes[i].isParent = True

    for i in range(len(shapes)):
        if len(shapes[i].parent) == 0:
            shapes[i].isChild = False
        else:
            shapes[i].isChild = True

def generateNodes(shapes, crse, meshingMethod):
    # Generate interior free nodes
    for i in range(len(shapes)):
        if shapes[i].isClosed:
            if meshingMethod == "ruppert":
                meshShapeRuppert(i, shapes, crse)
            elif meshingMethod == "triangle":
                meshShapeTriangle(i, shapes, crse)
        else:
            shapes[i].freeNodes = np.array([])

def meshShapeTriangle(ind, shapes):
    # Parent points
    parentPoints = shapes[ind].boundaryNodes
    # Child points
    childPoints = []
    for i in range(len(shapes[ind].child)):
        childPoints.append(shapes[shapes[ind].child[i]].boundaryNodes.tolist())
    
    vertices = parentPoints.append(childPoints)

    # Parent segments
    segments = []
    for i in range(len(parentPoints)-1):
        segments.append([i, i+1])
    segments.append([len(parentPoints)-1, 0])
    # Child segments
    segInd = len(parentPoints)
    for i in range(len(shapes[ind].child)):
        for j in range(len(childPoints[i])-1):
            if shapes[shapes[ind].child[i]].shape != "point":
                segments.append([segInd+j, segInd+j+1])
        if shapes[shapes[ind].child[i]].isClosed:
            segments.append([segInd+j+1, segInd])
        if shapes[shapes[ind].child[i]].shape == 'point':
            segInd = segInd + 1
        else:
            segInd = segInd + len(childPoints[i])

    regions = []


def meshShapeRuppert(ind, shapes, crse): # Consider skipping sengment initialisation in case of Point
    # Parent points
    parentPoints = shapes[ind].boundaryNodes
    # Child points
    childPoints = []
    for i in range(len(shapes[ind].child)):
        childPoints.append(shapes[shapes[ind].child[i]].boundaryNodes.tolist())
    
    # Parent polygon
    parentPolygon = ShapelyPolygon(parentPoints)
    # Child polygons
    childPolygons = []
    for i in range(len(shapes[ind].child)):
        if shapes[shapes[ind].child[i]].isClosed:
            childPolygons.append(ShapelyPolygon(childPoints[i]))

    # Parent segments
    segments = []
    for i in range(len(parentPoints)-1):
        segments.append([i, i+1])
    segments.append([len(parentPoints)-1, 0])
    # Child segments
    segInd = len(parentPoints)
    for i in range(len(shapes[ind].child)):
        for j in range(len(childPoints[i])-1):
            if shapes[shapes[ind].child[i]].shape != "point":
                segments.append([segInd+j, segInd+j+1])
        if shapes[shapes[ind].child[i]].isClosed:
            segments.append([segInd+j+1, segInd])
        if shapes[shapes[ind].child[i]].shape == 'point':
            segInd = segInd + 1
        else:
            segInd = segInd + len(childPoints[i])

    # Points
    points = parentPoints

    for i in range(len(childPoints)):
        points = np.vstack((points,childPoints[i]))

    dt = delaunay(points)
    cm = dt.simplices  # Connectivity matrix
    x = points[:, 0]
    y = points[:, 1]
    ix = x.copy()
    iy = y.copy()

    elementsToRemove = []
    for i in range(len(cm)):
        cot = ShapelyPoint((x[cm[i][0]]+x[cm[i][1]]+x[cm[i][2]])/3, (y[cm[i][0]]+y[cm[i][1]]+y[cm[i][2]])/3)
        if not parentPolygon.contains(cot):
            elementsToRemove.append(i)
        for childPolygon in childPolygons:
            if childPolygon.contains(cot):
                elementsToRemove.append(i)
    cm = np.delete(cm, elementsToRemove, 0)
    st = getSharpTriangles(x, y, cm, crse)

    while len(st) != 0:
        for element in st:
            ex = x[cm[element]]
            ey = y[cm[element]]
            cc = circumCenter(ex, ey)

            isNotEcroached = segmentsEncroached(points, segments, cc)
            cirCen = ShapelyPoint(cc[0], cc[1])
            if parentPolygon.contains(cirCen) and isNotEcroached:
                pointOutsideChild = True
                for i in range(len(childPolygons)):
                    if childPolygons[i].contains(cirCen):
                        pointOutsideChild = False
                        break
                if pointOutsideChild:
                    points = np.vstack([points, cc])
                    dt = delaunay(points)
                    cm = dt.simplices # Connectivity matrix
                    x = points[:,0]
                    y = points[:,1]

                    elementsToRemove = []
                    for i in range(len(cm)):
                        cot = ShapelyPoint((x[cm[i][0]]+x[cm[i][1]]+x[cm[i][2]])/3, (y[cm[i][0]]+y[cm[i][1]]+y[cm[i][2]])/3)
                        if not parentPolygon.contains(cot):
                            elementsToRemove.append(i)
                        for childPolygon in childPolygons:
                            if childPolygon.contains(cot):
                                elementsToRemove.append(i)
                    cm = np.delete(cm, elementsToRemove, 0)
                    break
        stNew = getSharpTriangles(x, y, cm, crse)
        if stNew == st:
            break
        else:
            st = stNew

    fx = x[len(ix):len(x)-1]
    fy = y[len(iy):len(y)-1]
    freeNodes = []
    for i in range(len(fx)):
        freeNodes.append([fx[i],fy[i]])
    freeNodes = np.array(freeNodes)
    shapes[ind].freeNodes = freeNodes

def circumCenter(ex, ey):
    Ax, Ay, Bx, By, Cx, Cy = ex[0], ey[0], ex[1], ey[1], ex[2], ey[2]
    D = 2*(Ax*(By-Cy)+Bx*(Cy-Ay)+Cx*(Ay-By))
    cx = ((Ax*Ax+Ay*Ay)*(By-Cy)+(Bx*Bx+By*By)*(Cy-Ay)+(Cx*Cx+Cy*Cy)*(Ay-By))/D
    cy = ((Ax*Ax+Ay*Ay)*(Cx-Bx)+(Bx*Bx+By*By)*(Ax-Cx)+(Cx*Cx+Cy*Cy)*(Bx-Ax))/D
    return cx, cy

def circumRadiusToMinSideRatio(ex, ey):
    a, b, c = np.sqrt((ex[1]-ex[0])**2+(ey[1]-ey[0])**2), np.sqrt((ex[2]-ex[1])**2+(ey[2]-ey[1])**2), np.sqrt((ex[2]-ex[0])**2+(ey[2]-ey[0])**2)
    minSide = min([a, b, c])
    cr = (a*b*c)/(np.sqrt((a + b + c)*(b + c - a)*(c + a - b)*(a + b - c))) # Circumradius
    return cr/minSide

def getSharpTriangles(x, y, cm, B):
    st = []
    for i in range(len(cm)):
        element = cm[i]
        ex = x[element]
        ey = y[element]
        circumRatio = circumRadiusToMinSideRatio(ex, ey)
        if circumRatio > B:
            st.append(i)
    return st

def encroached(p1, p2, p):
    m = (np.array(p1)+np.array(p2))/2
    r = np.sqrt((p1[0]-m[0])**2+(p1[1]-m[1])**2)
    d = np.sqrt((p[0]-m[0])**2+(p[1]-m[1])**2)
    if d > r:
        return False
    else:
        return True

def segmentsEncroached(points, segments, cc):
    isNotEncroached = True
    for i in range(len(segments)):
        segmentCentre = [(points[segments[i][0]][0]+points[segments[i][1]][0])/2 ,(points[segments[i][0]][1]+points[segments[i][1]][1])/2]
        segmentRadius = np.sqrt((points[segments[i][0]][0]-points[segments[i][1]][0])**2+(points[segments[i][0]][1]-points[segments[i][1]][1])**2)/2
        distanceFromCentre = np.sqrt((cc[0]-segmentCentre[0])**2+(cc[1]-segmentCentre[1])**2)
        if distanceFromCentre < segmentRadius:
            isNotEncroached = False
            break
    return isNotEncroached

def createMesh(shapes):

    x = np.array([])
    y = np.array([])
    nn = -1

    for shape in shapes:
        if shape.shape == "point":
            shape.boundaryList = np.array([nn+1])
            nn = nn+1
            shape.freeList = np.array([])
            x =  np.concatenate((x, [shape.boundaryNodes[0]]))
            y =  np.concatenate((y, [shape.boundaryNodes[1]]))

        elif shape.shape == "line" or shape.shape == "polyline":
            shape.boundaryList = np.arange(nn+1, nn+len(shape.boundaryNodes[:, 0])+1, 1)
            nn = shape.boundaryList[-1]
            shape.freeList = np.array([])
            x =  np.concatenate((x, shape.boundaryNodes[:, 0]))
            y =  np.concatenate((y, shape.boundaryNodes[:, 1]))

        else:
            # print(shape.boundaryNodes)
            # print(shape.freeNodes)
            shape.boundaryList = np.arange(nn+1, nn+len(shape.boundaryNodes)+1, 1)
            nn = shape.boundaryList[-1]
            if len(shape.freeNodes) == 0:
                shape.freeList = np.array([])
            else:
                shape.freeList = np.arange(nn+1, nn+len(shape.freeNodes)+1, 1)
                nn = shape.freeList[-1]
            x =  np.concatenate((x, shape.boundaryNodes[:, 0], shape.freeNodes[:, 0]))
            y =  np.concatenate((y, shape.boundaryNodes[:, 1], shape.freeNodes[:, 1]))

    xy = np.transpose([x, y])
    dt = delaunay(xy)
    mesh = Mesh(x, y, dt.simplices)
    
    # Generate element list in each shape
    ne = len(dt.simplices[:,0])
    parentPolygons = []
    childPolygons = []
    for shape in shapes:
        shape.elementList = []
        if shape.isClosed:
            parentPolygons.append(ShapelyPolygon(shape.boundaryNodes))
            childPolygon = []
            for i in range(len(shape.child)):
                if shapes[shape.child[i]].shape == "point":
                    childPolygon.append([])
                else:
                    childPolygon.append(ShapelyPolygon(shapes[shape.child[i]].boundaryNodes))
            childPolygons.append(childPolygon)
        else:
            parentPolygons.append([])
            childPolygons.append([])

    cm = dt.simplices
    for i in range(ne):
        ex = x[cm[i]]
        ey = y[cm[i]]
        cc = circumCenter(ex, ey)
        point = ShapelyPoint(cc[0], cc[1])

        for j in range(len(shapes)):
            if shapes[j].isClosed:
                parentPolygon = parentPolygons[j]
                childPolygon = childPolygons[j]
                if parentPolygon.contains(point):
                    pointOutsideChild = True
                    for k in range(len(childPolygon)):
                        if shapes[shapes[j].child[k]].shape != 'point':
                            if childPolygon[k].contains(point):
                                pointOutsideChild = False
                                break

                    if pointOutsideChild:
                        shapes[j].elementList.append(i)

    # Elements
    mesh.getNeiElements()
    # Nodes
    mesh.getNeiNodes()

    return mesh

def assignSources(shapes, mesh):
    x = mesh.x
    y = mesh.y
    nn = len(x)
    # nodeSource is for both plotting and matrix assignment
    # elementSource may serve some purpose in different physics
    nodeSource = np.zeros((nn,1))
    ne = len(mesh.conmat[:,0])
    elementSource = np.zeros((ne,1))
    print("Assigning sources")
    for shape in shapes:
        if not shape.isClosed:
            nodes = shape.boundaryList
            for node in nodes:
                nodeSource[node] = shape.source/len(nodes)
                elements = mesh.neiElements[node]
                for element in elements:
                    elementSource[element] = elementSource[element] + shape.source/len(elements)
        else:
            elements = shape.elementList
            for element in elements:
                ex = []
                ey = []
                for node in mesh.conmat[element]:
                    ex.append(x[node])
                    ey.append(y[node])
                p = [ey[1]-ey[2], ey[2]-ey[0], ey[0]-ey[1]]
                q = [ex[2]-ex[1], ex[0]-ex[2], ex[1]-ex[0]]
                ea = 0.5*abs(p[1]*q[2]-q[1]*p[2])
                # if ea == 0:
                #     print("element area is zero at: ", element)
                elementSource[element] = shape.source*ea
            for element in elements:
                for node in mesh.conmat[element]:
                    nodeSource[node] = nodeSource[node] + elementSource[element]/3
    mesh.elementSource = elementSource            
    mesh.nodeSource = nodeSource
    
def assignMaterials(shapes, mesh):
    # nodeMaterial may be used for plotting
    # elementMaterial is for matrix computation
    x = mesh.x
    nn = len(x)
    nodeMaterial = np.ones((nn,1))
    ne = len(mesh.conmat[:,0])
    elementMaterial = np.ones((ne,1))
    print("Assigning material properties")
    for shape in shapes:
        if not shape.isClosed:
            nodes = shape.boundaryList
            for node in nodes:
                nodeMaterial[node] = shape.material
        else:
            nodes = np.concatenate((shape.boundaryList, shape.freeList)).astype(int)
            for node in nodes:
                nodeMaterial[node] = shape.material
        elements = shape.elementList
        for element in elements:
            elementMaterial[element] = shape.material
    mesh.nodeMaterial = nodeMaterial
    mesh.elementMaterial = elementMaterial

