import numpy as np
from shapely.geometry.polygon import Polygon as ShapelyPolygon
from shapely.geometry import Point as ShapelyPoint
from .Polygon import Polygon

def add(shape1, shape2):

    if shape1.isClosed and shape2.isClosed: # Add only if both are closed
        points1, points2 = shape1.boundaryNodes, shape2.boundaryNodes
        points1io, points2io = [], []
        
        polygon = ShapelyPolygon(points2) # separating interior and exterior points of shape 1
        for i in range(len(points1)):
            point = ShapelyPoint(points1[i])
            if polygon.contains(point):
                points1io.append(1)
            else:
                points1io.append(0)
        npo1 = len(points1) - sum(points1io)

        polygon = ShapelyPolygon(points1) # separating interior and exterior points of shape 2
        for i in range(len(points2)):
            point = ShapelyPoint(points2[i])
            if polygon.contains(point):
                points2io.append(1)
            else:
                points2io.append(0)
        npo2 = len(points2) - sum(points2io)

        if (npo1 == len(points1) and npo2 == len(points2)) or (npo1 == 0 and npo2 == len(points2)) or (npo1 == len(points1) and npo2 == 0):
            raise ValueError("Cannot add non overlapping or completely inclusive shapes.")
        else:
            segmentLengths = []
            for i in range(len(points1)-1):
                segmentLengths.append(np.sqrt((points1[i][0]-points1[i+1][0])**2+(points1[i][1]-points1[i+1][1])**2))
            for i in range(len(points2)-1):
                segmentLengths.append(np.sqrt((points2[i][0]-points2[i+1][0])**2+(points2[i][1]-points2[i+1][1])**2))

            # Rotate index
            for i in range(len(points1)):
                if points1io[i] == 1 and points1io[i+1] == 0:
                    rotationIndex = i+1
                    break
            points1 = np.roll(points1, (-rotationIndex,-rotationIndex))

            for i in range(len(points2)):
                if points2io[i] == 1 and points2io[i+1] == 0:
                    rotationIndex = i+1
                    break
            points2 = np.roll(points2, (-rotationIndex,-rotationIndex))

            # vstack outside points
            boundaryNodes = np.vstack([points1[0:npo1], points2[0:npo2]])

            # remove short segments from the union
            minSeglength = min(segmentLengths)
            pointsToRemove = []
            i = npo1-1
            if np.sqrt((boundaryNodes[i][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[i][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i)
            i = npo1+npo2-2
            if np.sqrt((boundaryNodes[0][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[0][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i+1)

            boundaryNodes = np.delete(boundaryNodes, pointsToRemove, axis=0)
            return Polygon(points = boundaryNodes, stroke = shape1.stroke)
    else:
        raise ValueError("Cannot add open shapes.")

def intersect(shape1, shape2):

    if shape1.isClosed and shape2.isClosed: # Intersect only if both are closed
        points1, points2 = shape1.boundaryNodes, shape2.boundaryNodes
        points1io, points2io = [], []
        
        polygon = ShapelyPolygon(points2) # separating interior and exterior points of shape 1
        for i in range(len(points1)):
            point = ShapelyPoint(points1[i])
            if polygon.contains(point):
                points1io.append(1)
            else:
                points1io.append(0)
        npi1 = sum(points1io)
        npo1 = len(points1) - sum(points1io)

        polygon = ShapelyPolygon(points1) # separating interior and exterior points of shape 2
        for i in range(len(points2)):
            point = ShapelyPoint(points2[i])
            if polygon.contains(point):
                points2io.append(1)
            else:
                points2io.append(0)
        npi2 = sum(points2io)
        npo2 = len(points2) - sum(points2io)

        if (npo1 == len(points1) and npo2 == len(points2)) or (npo1 == 0 and npo2 == len(points2)) or (npo1 == len(points1) and npo2 == 0):
            raise ValueError("Cannot intersect non overlapping or completely inclusive shapes.")
        else:
            segmentLengths = []
            for i in range(len(points1)-1):
                segmentLengths.append(np.sqrt((points1[i][0]-points1[i+1][0])**2+(points1[i][1]-points1[i+1][1])**2))
            for i in range(len(points2)-1):
                segmentLengths.append(np.sqrt((points2[i][0]-points2[i+1][0])**2+(points2[i][1]-points2[i+1][1])**2))

            # Rotate index
            for i in range(len(points1)):
                if points1io[i] == 0 and points1io[i+1] == 1:
                    rotationIndex = i+1
                    break
            points1 = np.roll(points1, (-rotationIndex,-rotationIndex))

            for i in range(len(points2)):
                if points2io[i] == 0 and points2io[i+1] == 1:
                    rotationIndex = i+1
                    break
            points2 = np.roll(points2, (-rotationIndex,-rotationIndex))

            # vstack inside points
            boundaryNodes = np.vstack([points1[0:npi1], points2[0:npi2]])

            # remove short segments from the intersection
            minSeglength = min(segmentLengths)
            pointsToRemove = []
            i = npi1-1
            if np.sqrt((boundaryNodes[i][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[i][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i)
            i = npi1+npi2-2
            if np.sqrt((boundaryNodes[0][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[0][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i+1)

            boundaryNodes = np.delete(boundaryNodes, pointsToRemove, axis=0)
            return Polygon(points = boundaryNodes, stroke = shape1.stroke)
    else:
        raise ValueError("Cannot intersect open shapes.")

def subtract(shape1, shape2):

    if shape1.isClosed and shape2.isClosed: # Subtract only if both are closed
        points1, points2 = shape1.boundaryNodes, shape2.boundaryNodes
        points1io, points2io = [], []
        
        polygon = ShapelyPolygon(points2) # separating interior and exterior points of shape 1
        for i in range(len(points1)):
            point = ShapelyPoint(points1[i])
            if polygon.contains(point):
                points1io.append(1)
            else:
                points1io.append(0)
        npi1 = sum(points1io)
        npo1 = len(points1) - sum(points1io)

        polygon = ShapelyPolygon(points1) # separating interior and exterior points of shape 2
        for i in range(len(points2)):
            point = ShapelyPoint(points2[i])
            if polygon.contains(point):
                points2io.append(1)
            else:
                points2io.append(0)
        npo2 = len(points2) - sum(points2io)

        if (npo1 == len(points1) and npo2 == len(points2)) or (npo1 == 0 and npo2 == len(points2)) or (npo1 == len(points1) and npo2 == 0):
            raise ValueError("Cannot subtract non overlapping or completely inclusive shapes.")
        else:
            segmentLengths = []
            for i in range(len(points1)-1):
                segmentLengths.append(np.sqrt((points1[i][0]-points1[i+1][0])**2+(points1[i][1]-points1[i+1][1])**2))
            for i in range(len(points2)-1):
                segmentLengths.append(np.sqrt((points2[i][0]-points2[i+1][0])**2+(points2[i][1]-points2[i+1][1])**2))

            # Rotate
            for i in range(len(points1)):
                if points1io[i] == 0 and points1io[i+1] == 1:
                    rotationIndex = i+1
                    break
            points1 = np.roll(points1, (-rotationIndex,-rotationIndex))

            for i in range(len(points2)):
                if points2io[i] == 1 and points2io[i+1] == 0:
                    rotationIndex = i+1
                    break
            points2 = np.roll(points2, (-rotationIndex,-rotationIndex))

            # vstack flipped inside points with unflipped outside points 
            boundaryNodes = np.vstack([np.flip(points1[0:npi1], 0), points2[0:npo2]])

            # remove short segments from the subtraction
            minSeglength = min(segmentLengths)
            pointsToRemove = []
            i = npi1-1
            if np.sqrt((boundaryNodes[i][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[i][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i)
            i = npi1+npo2-2
            if np.sqrt((boundaryNodes[0][0]-boundaryNodes[i+1][0])**2+(boundaryNodes[0][1]-boundaryNodes[i+1][1])**2) < 0.5*minSeglength:
                pointsToRemove.append(i+1)

            boundaryNodes = np.delete(boundaryNodes, pointsToRemove, axis=0)
            return Polygon(points = boundaryNodes, stroke = shape2.stroke)
    else:
        raise ValueError("Cannot subtract open shapes.")

# def split(shape1, shape2): # Provide provision to split with multiple shapes and domain tags for each segment.

