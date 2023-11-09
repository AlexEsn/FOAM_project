#!/usr/bin/env python

###
# This file is generated automatically by SALOME v9.9.0 with dump python functionality
###

import SMESH
from salome.smesh import smeshBuilder
import SALOMEDS
import math
from salome.geom import geomBuilder
import GEOM
import salome_notebook
import sys
import salome

# Получаем аргументы из командной строки
shift_first_cylinder = int(sys.argv[1])
shift_second_cylinder = int(sys.argv[2])
shift_third_cylinder = int(sys.argv[3])
export_unv_path = sys.argv[4]

print(f"Args: {sys.argv}")

salome.salome_init()
notebook = salome_notebook.NoteBook()

###
# GEOM component
###


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)

duct = geompy.MakeBoxDXDYDZ(300, 50, 100)
geompy.TranslateDXDYDZ(duct, -150, -20, 10)

heater = geompy.MakeBoxDXDYDZ(10, 10, 10)

substrate = geompy.MakeBoxDXDYDZ(30, 30, 2)
geompy.TranslateDXDYDZ(substrate, -10, -10, 10)

Cylinder_1 = geompy.MakeCylinderRH(5, 10)
geompy.TranslateDXDYDZ(Cylinder_1, -5, -5, 12)

Cylinder_2 = geompy.MakeTranslation(Cylinder_1, 0, 10, 0)
Cylinder_3 = geompy.MakeTranslation(Cylinder_2, 0, 10, 0)

Cylinder_1 = geompy.MakeTranslation(Cylinder_1, shift_first_cylinder, 0, 0)
Cylinder_2 = geompy.MakeTranslation(Cylinder_2, shift_second_cylinder, 0, 0)
Cylinder_3 = geompy.MakeTranslation(Cylinder_3, shift_third_cylinder, 0, 0)


fins = geompy.MakeFuseList(
[substrate, Cylinder_1, Cylinder_2, Cylinder_3], False, False)

# fins = geompy.MakeFuseList(
#     [substrate, Cylinder_1, Cylinder_2], False, False)

fluid = geompy.MakeCutList(duct, [fins], True)

fluidHeaterFins = geompy.MakePartition(
    [heater, fins, fluid], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

fluid_1_id = geompy.SubShapeAllIDs(
    fluidHeaterFins, geompy.ShapeType["SOLID"])[2]

fluid_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fluid_1, [fluid_1_id])
# print(fluid_1_id)

heater_1_id = geompy.SubShapeAllIDs(
    fluidHeaterFins, geompy.ShapeType["SOLID"])[0]

heater_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(heater_1, [heater_1_id])
# print(heater_1_id)

fins_1_id = geompy.SubShapeAllIDs(
    fluidHeaterFins, geompy.ShapeType["SOLID"])[1]

fins_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fins_1, [fins_1_id])
# print(fins_1_id)

walls_heater_ids = geompy.GetShapesOnBoxIDs(
    heater, fluidHeaterFins, geompy.ShapeType["FACE"], GEOM.ST_ON)[0:-1]

walls_heater = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls_heater, walls_heater_ids)
# print(walls_heater_ids)

base_fins_id = geompy.GetShapesOnPlaneWithLocationIDs(fluidHeaterFins,
                                                      geompy.ShapeType["FACE"],
                                                      geompy.MakeVectorDXDYDZ(
                                                          0, 0, 1),
                                                      geompy.MakeVertex(
                                                          100, 0, 10),
                                                      GEOM.ST_ON)[1]

base_fins = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(base_fins, [base_fins_id])
# print(base_fins_id)

inlet_fluid_id = geompy.GetShapesOnPlaneWithLocationIDs(fluidHeaterFins,
                                                        geompy.ShapeType["FACE"],
                                                        geompy.MakeVectorDXDYDZ(
                                                            -1, 0, 0),
                                                        geompy.MakeVertex(
                                                            -150, 0, 50),
                                                        GEOM.ST_ON)

outlet_fluid_id = geompy.GetShapesOnPlaneWithLocationIDs(fluidHeaterFins,
                                                         geompy.ShapeType["FACE"],
                                                         geompy.MakeVectorDXDYDZ(
                                                             1, 0, 0),
                                                         geompy.MakeVertex(
                                                             150, 0, 50),
                                                         GEOM.ST_ON)

all_walls_fluid_ids = geompy.GetShapesOnBoxIDs(
    duct, fluidHeaterFins, geompy.ShapeType["FACE"], GEOM.ST_ON)

all_walls_fluid_ids.sort()

walls_fluid_ids = []
is_start_fluid = False
for i in all_walls_fluid_ids:
    if i == outlet_fluid_id[0]:
        break
    if is_start_fluid:
        walls_fluid_ids.append(i)
    if i == inlet_fluid_id[0]:
        is_start_fluid = True

walls_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls_fluid, walls_fluid_ids)
# print(walls_fluid_ids)

inlet_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet_fluid, inlet_fluid_id)
# print(inlet_fluid_id)

outlet_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet_fluid, outlet_fluid_id)
# print(outlet_fluid_id)

[fluid_1, heater_1, fins_1, walls_heater, base_fins, walls_fluid, inlet_fluid,
    outlet_fluid] = geompy.GetExistingSubObjects(fluidHeaterFins, False)


geompy.addToStudy(O, 'O')
geompy.addToStudy(OX, 'OX')
geompy.addToStudy(OY, 'OY')
geompy.addToStudy(OZ, 'OZ')
geompy.addToStudy(heater, 'heater')
geompy.addToStudy(substrate, 'substrate')
geompy.addToStudy(Cylinder_1, 'Cylinder_1')
geompy.addToStudy(Cylinder_2, 'Cylinder_2')
geompy.addToStudy(Cylinder_3, 'Cylinder_3')
geompy.addToStudy(fins, 'fins')
geompy.addToStudy(duct, 'duct')
geompy.addToStudy(fluid, 'fluid')
geompy.addToStudy(fluidHeaterFins, 'fluidHeaterFins')
geompy.addToStudyInFather(fluidHeaterFins, outlet_fluid, 'outlet_fluid')
geompy.addToStudyInFather(fluidHeaterFins, fluid_1, 'fluid')
geompy.addToStudyInFather(fluidHeaterFins, heater_1, 'heater')
geompy.addToStudyInFather(fluidHeaterFins, fins_1, 'fins')
geompy.addToStudyInFather(fluidHeaterFins, walls_heater, 'walls_heater')
geompy.addToStudyInFather(fluidHeaterFins, walls_fluid, 'walls_fluid')
geompy.addToStudyInFather(fluidHeaterFins, base_fins, 'base_fins')
geompy.addToStudyInFather(fluidHeaterFins, inlet_fluid, 'inlet_fluid')


smesh = smeshBuilder.New()
# smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
# multiples meshes built in parallel, complex and numerous mesh edition (performance)

NETGEN_3D_Parameters_1 = smesh.CreateHypothesis(
    'NETGEN_Parameters', 'NETGENEngine')
NETGEN_3D_Parameters_1.SetMaxSize(20)
NETGEN_3D_Parameters_1.SetMinSize(1)
NETGEN_3D_Parameters_1.SetSecondOrder(0)
NETGEN_3D_Parameters_1.SetOptimize(1)
NETGEN_3D_Parameters_1.SetFineness(2)
NETGEN_3D_Parameters_1.SetChordalError(-1)
NETGEN_3D_Parameters_1.SetChordalErrorEnabled(0)
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature(1)
NETGEN_3D_Parameters_1.SetFuseEdges(1)
NETGEN_3D_Parameters_1.SetQuadAllowed(0)
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(fins, 2)
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(heater, 2)
NETGEN_3D_Parameters_1.SetCheckChartBoundary(32)
NETGEN_1D_2D_3D = smesh.CreateHypothesis('NETGEN_2D3D', 'NETGENEngine')
try:
    pass
except:
    print('ExportUNV() failed. Invalid file name?')
NETGEN_3D_Parameters_2 = smesh.CreateHypothesis(
    'NETGEN_Parameters', 'NETGENEngine')
NETGEN_3D_Parameters_2.SetMaxSize(20)
NETGEN_3D_Parameters_2.SetMinSize(1)
NETGEN_3D_Parameters_2.SetSecondOrder(0)
NETGEN_3D_Parameters_2.SetOptimize(1)
NETGEN_3D_Parameters_2.SetFineness(2)
NETGEN_3D_Parameters_2.SetChordalError(-1)
NETGEN_3D_Parameters_2.SetChordalErrorEnabled(0)
NETGEN_3D_Parameters_2.SetUseSurfaceCurvature(1)
NETGEN_3D_Parameters_2.SetFuseEdges(1)
NETGEN_3D_Parameters_2.SetQuadAllowed(0)
NETGEN_3D_Parameters_2.SetLocalSizeOnShape(fins, 2)
NETGEN_3D_Parameters_2.UnsetLocalSizeOnEntry("0:1:1:13")
NETGEN_3D_Parameters_2.SetLocalSizeOnShape(heater, 2)
NETGEN_3D_Parameters_2.SetCheckChartBoundary(32)
NETGEN_3D_Parameters_2.UnsetLocalSizeOnEntry("0:1:1:13")
Mesh_1 = smesh.Mesh(fluidHeaterFins, 'Mesh_1')
status = Mesh_1.AddHypothesis(NETGEN_3D_Parameters_2)
status = Mesh_1.AddHypothesis(NETGEN_1D_2D_3D)
heater_2 = Mesh_1.GroupOnGeom(heater_1, 'heater', SMESH.VOLUME)
fluid_2 = Mesh_1.GroupOnGeom(fluid_1, 'fluid', SMESH.VOLUME)
fins_2 = Mesh_1.GroupOnGeom(fins_1, 'fins', SMESH.VOLUME)
inlet_fluid_1 = Mesh_1.GroupOnGeom(inlet_fluid, 'inlet_fluid', SMESH.FACE)
outlet_fluid_1 = Mesh_1.GroupOnGeom(outlet_fluid, 'outlet_fluid', SMESH.FACE)
walls_fluid_1 = Mesh_1.GroupOnGeom(walls_fluid, 'walls_fluid', SMESH.FACE)
walls_heater_1 = Mesh_1.GroupOnGeom(walls_heater, 'walls_heater', SMESH.FACE)
base_fins_1 = Mesh_1.GroupOnGeom(base_fins, 'base_fins', SMESH.FACE)
isDone = Mesh_1.Compute()
[heater_2, fluid_2, fins_2, inlet_fluid_1, outlet_fluid_1,
    walls_fluid_1, walls_heater_1, base_fins_1] = Mesh_1.GetGroups()
try:
    # написать про это
    Mesh_1.ExportUNV(export_unv_path)
    pass
except:
    print('ExportUNV() failed. Invalid file name?')


# Set names of Mesh objects
smesh.SetName(NETGEN_1D_2D_3D, 'NETGEN 1D-2D-3D')
smesh.SetName(NETGEN_3D_Parameters_2, 'NETGEN 3D Parameters_2')
smesh.SetName(heater_2, 'heater')
smesh.SetName(fluid_2, 'fluid')
smesh.SetName(NETGEN_3D_Parameters_1, 'NETGEN 3D Parameters_1')
smesh.SetName(fins_2, 'fins')
smesh.SetName(Mesh_1.GetMesh(), 'Mesh_1')
smesh.SetName(base_fins_1, 'base_fins')
smesh.SetName(walls_heater_1, 'walls_heater')
smesh.SetName(walls_fluid_1, 'walls_fluid')
smesh.SetName(outlet_fluid_1, 'outlet_fluid')
smesh.SetName(inlet_fluid_1, 'inlet_fluid')


if salome.sg.hasDesktop():
    salome.sg.updateObjBrowser()
