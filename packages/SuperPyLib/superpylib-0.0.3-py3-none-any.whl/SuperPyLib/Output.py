# Import packages
import joblib
from . import PlotUtils
from . import Mesh
from .Solvers import Solve

def mesh(crse = 1, dpi = 300, meshingMethod = "ruppert"):
    print("Generating mesh")
    geometry = joblib.load("Data/geometry.sav")
    Mesh.prepareGeometryForMeshing(geometry)
    Mesh.generateNodes(geometry, crse, meshingMethod)
    mesh = Mesh.createMesh(geometry)
    joblib.dump(geometry, "Data/geometry.sav")
    joblib.dump(mesh, "Data/mesh.sav")
    if dpi < 300:
        dpi = 300
        print("Value of dpi too low. Resetting dpi to 300.")
    PlotUtils.plotMesh(geometry, mesh, "Figures/2_Mesh.png", dpi)

def assigedSources(dpi):
    shapes = joblib.load("Data/geometry.sav")
    mesh = joblib.load("Data/mesh.sav")
    solver = joblib.load("Data/solver.sav")
    Mesh.assignSources(shapes, mesh)
    joblib.dump(mesh, "Data/mesh.sav")
    PlotUtils.plotSources(mesh, solver, "Figures/3_Sources.png", dpi)

def assigedMaterials(dpi):
    shapes = joblib.load("Data/geometry.sav")
    mesh = joblib.load("Data/mesh.sav")
    solver = joblib.load("Data/solver.sav")
    Mesh.assignMaterials(shapes, mesh)
    joblib.dump(mesh, "Data/mesh.sav")
    PlotUtils.plotMaterials(mesh, solver, "Figures/4_Materials.png", dpi)
    
def solution(solutionName = "numerical", solverMethod = "Scipy", withDifference = False, withField = False, dpi = 300):
    shapes = joblib.load("Data/geometry.sav")
    mesh = joblib.load("Data/mesh.sav")
    solver = joblib.load("Data/solver.sav")
    Solve.getMatrices(shapes, mesh, solver, solutionName)
    Solve.solve(shapes, mesh, solver, solutionName, solverMethod)
    if dpi < 300:
        dpi = 300
        print("Value of dpi too low. Resetting dpi to 300.")
    showSolution(mesh, solver, solutionName, withField, dpi)
    if withDifference:
        showDifference(mesh, solver, solutionName, dpi)
    joblib.dump(mesh, "Data/mesh.sav")
    joblib.dump(solver, "Data/solver.sav")

def showSolution(mesh, solver, solutionName, withField, dpi):
    if (solutionName == "approximate"):
        solution = solver.ua
        PlotUtils.plotSolution(mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numerical"):
        solution = solver.un
        PlotUtils.plotSolution(mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numericalApproxBound"):
        solution = solver.unab
        PlotUtils.plotSolution(mesh, solver, solution, solutionName, withField, dpi)
    elif (solutionName == "numericalIterBound"):
        solution = solver.unib
        PlotUtils.plotSolution(mesh, solver, solution, solutionName, withField, dpi)

def showDifference(mesh, solver, solutionName, dpi):
    print()