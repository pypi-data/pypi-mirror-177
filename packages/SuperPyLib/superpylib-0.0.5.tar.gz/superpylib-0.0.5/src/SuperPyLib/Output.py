# Import packages
import joblib
from . import PlotUtils
from . import Mesh
from .Solvers import Solve

def mesh(par, crse = 1, dpi = 300, meshingMethod = "ruppert"):
    if par == []:
        geometry = joblib.load("Data/geometry.sav")
    else:
        stri = f'Data/geometry{par}.sav'
        geometry = joblib.load(stri)

    Mesh.prepareGeometryForMeshing(geometry)
    Mesh.generateNodes(geometry, crse, meshingMethod)
    mesh = Mesh.createMesh(geometry)

    if dpi < 300:
        dpi = 300

    if par == []:
        joblib.dump(geometry, "Data/geometry.sav")
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotMesh(geometry, mesh, "Figures/2_Mesh.png", dpi)
    else: 
        stri = f'Data/geometry{par}.sav'
        joblib.dump(geometry, stri)
        stri = f'Data/mesh{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/2_Mesh{par}.png'
        PlotUtils.plotMesh(geometry, mesh, stri, dpi)


def assigedSources(par, dpi):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver{par}.sav'
        solver = joblib.load(stri)

    Mesh.assignSources(shapes, mesh)

    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotSources(mesh, solver, "Figures/3_Sources.png", dpi)
    else:
        stri = f'Data/mesh{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/3_Sources{par}.png'
        PlotUtils.plotSources(mesh, solver, stri, dpi)
    

def assigedMaterials(par, dpi):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver{par}.sav'
        solver = joblib.load(stri)

    Mesh.assignMaterials(shapes, mesh)
    
    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        PlotUtils.plotMaterials(mesh, solver, "Figures/4_Materials.png", dpi)
    else:
        stri = f'Data/mesh{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Figures/4_Materials{par}.png'
        PlotUtils.plotMaterials(mesh, solver, stri, dpi)

def solution(par, solutionName = "numerical", solverMethod = "Scipy", withDifference = False, withField = False, dpi = 300):
    if par == []:
        shapes = joblib.load("Data/geometry.sav")
        mesh = joblib.load("Data/mesh.sav")
        solver = joblib.load("Data/solver.sav")
    else:
        stri = f'Data/geometry{par}.sav'
        shapes = joblib.load(stri)
        stri = f'Data/mesh{par}.sav'
        mesh = joblib.load(stri)
        stri = f'Data/solver{par}.sav'
        solver = joblib.load(stri)

    Solve.getMatrices(shapes, mesh, solver, solutionName)
    Solve.solve(shapes, mesh, solver, solutionName, solverMethod)
    if dpi < 300:
        dpi = 300
        
    showSolution(mesh, solver, solutionName, withField, dpi)
    if withDifference:
        showDifference(mesh, solver, solutionName, dpi)

    if par == []:
        joblib.dump(mesh, "Data/mesh.sav")
        joblib.dump(solver, "Data/solver.sav")
    else:
        stri = f'Data/mesh{par}.sav'
        joblib.dump(mesh, stri)
        stri = f'Data/solver{par}.sav'
        joblib.dump(solver, stri)


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
    pass
