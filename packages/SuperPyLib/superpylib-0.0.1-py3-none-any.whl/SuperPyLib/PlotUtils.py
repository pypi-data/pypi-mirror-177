from matplotlib import rcParams
rcParams['font.family'] = 'Times New Roman'
import matplotlib.pyplot as plt

# import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import numpy as np
from matplotlib.ticker import FormatStrFormatter

def plotGeometry(shapes, filename, dpi):
    plt.close("all")
    # fig, ax=plt.subplots(dpi=dpi)
    for shape in shapes:
        shape.show(plt)
    plt.gca().set_aspect("equal")
    plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
    plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
    plt.xticks(fontsize= 10, fontweight='bold')
    plt.yticks(fontsize= 10, fontweight='bold')
    plt.savefig(filename, dpi=dpi)

def plotGeometryNodes(shapes, filename, dpi):
    plt.close("all")
    # fig, ax=plt.subplots(dpi=dpi)
    for shape in shapes:
        shape.showNodes(plt)
    plt.gca().set_aspect("equal")
    plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
    plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
    plt.xticks(fontsize= 10, fontweight='bold')
    plt.yticks(fontsize= 10, fontweight='bold')
    plt.savefig(filename, dpi=dpi)

def plotMesh(shapes, mesh, filename, dpi):
    plt.close("all")
    # fig, ax=plt.subplots(dpi=dpi)
    # for shape in shapes:
    #     shape.show(plt)
    plt.triplot(mesh.x, mesh.y, mesh.conmat, c = 'k', lw = 100/dpi)
    plt.gca().set_aspect("equal")
    plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
    plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
    plt.xticks(fontsize= 10, fontweight='bold')
    plt.yticks(fontsize= 10, fontweight='bold')
    plt.savefig(filename, dpi=dpi)

def closeFigure():
    plt.close()

def showPartialMesh(x, y, cm, ms = 1000):
    plt.close("all")
    fig = plt.figure()
    timer = fig.canvas.new_timer(interval = ms) #creating a timer object and setting an interval of 3000 milliseconds
    timer.add_callback(closeFigure)
    plt.triplot(x, y, cm, c = 'k')
    plt.gca().set_aspect("equal")
    timer.start()
    plt.show()

def plotSources(mesh, solver, filename, dpi):
    plt.close("all")
    # fig, ax=plt.subplots(dpi=dpi)
    triang = mtri.Triangulation(mesh.x, mesh.y, mesh.conmat)
    if solver.family == "thermal":
        cmap = "hot"
    else:
        cmap = "viridis"
    plt.tricontourf(triang, mesh.nodeSource[:,0], 900, cmap = cmap)
    plt.gca().set_aspect("equal")
    plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
    plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
    plt.xticks(fontsize= 10, fontweight='bold')
    plt.yticks(fontsize= 10, fontweight='bold')
    plt.savefig(filename, dpi=dpi)

def plotMaterials(mesh, solver, filename, dpi):
    plt.close("all")
    # fig, ax=plt.subplots(dpi=dpi)
    triang = mtri.Triangulation(mesh.x, mesh.y, mesh.conmat)
    if solver.family == "thermal":
        cmap = "hot"
    else:
        cmap = "viridis"
    plt.tricontourf(triang, mesh.nodeMaterial[:,0], 900, cmap = cmap)
    plt.gca().set_aspect("equal")
    plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
    plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
    plt.xticks(fontsize= 10, fontweight='bold')
    plt.yticks(fontsize= 10, fontweight='bold')
    plt.savefig(filename, dpi=dpi)

def plotSolution(mesh, solver, solution, solutionName, withField, dpi):
    plt.close("all")
    
    if solver.family == "thermal":
        cmap = "hot"
    else:
        cmap = "viridis"
    
    if withField:
        triang = mtri.Triangulation(mesh.x, mesh.y, mesh.conmat)
        plt.tricontourf(triang, solution[:,0]-solution[:,0][0], 900, cmap = cmap)
        # plt.tricontourf(triang, np.sqrt(solver.Ex**2+solver.Ey**2), 900, cmap = cmap)
        plt.quiver(mesh.x, mesh.y, solver.Ex, solver.Ey, scale = 2)
        plt.gca().set_aspect("equal")
        plt.xlabel("x-axis [m]", fontsize= 10, fontweight='bold')
        plt.ylabel("y-axis [m]", fontsize= 11, fontweight='bold')
        plt.xticks(fontsize= 10, fontweight='bold')
        plt.yticks(fontsize= 10, fontweight='bold')
    else:
        ax = plt.axes(projection='3d')
        ax.plot_trisurf(mesh.x, mesh.y, np.transpose(solution)[0]-np.transpose(solution)[0][0], cmap = cmap, edgecolor = 'grey', linewidth=0, antialiased=False)
        ax.view_init(30, -110)
        ax.set_xlabel("x-axis [m]")
        ax.set_ylabel("y-axis [m]")
        ax.zaxis.set_label_position("top")
        if solver.name == "electrostatic":
            ax.set_zlabel("Potential [Volt]") #, format='%.0e'
        elif solver.name == "magnetostatic":
            ax.set_zlabel("Potential [Tesla meter]")
    
    filename = "Figures/5_Solution_"+solutionName
    plt.savefig(filename, dpi=dpi)