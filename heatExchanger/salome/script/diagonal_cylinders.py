#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.9.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'C:/Users/sasch/OneDrive/Desktop/MEPhI/Project_practice/FOAM_project/heatExchanger/salome/script')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


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
Cylinder_3 = geompy.MakeTranslation(Cylinder_1, 0, 20, 0)

geompy.TranslateDXDYDZ(Cylinder_2, 10, 0, 0)
geompy.TranslateDXDYDZ(Cylinder_3, 20, 0, 0)


fins = geompy.MakeFuseList([substrate, Cylinder_1, Cylinder_2, Cylinder_3], False, False)

fluid = geompy.MakeCutList(duct, [fins], True)


fluidHeaterFins = geompy.MakePartition([heater, fins, fluid], [], [], [], geompy.ShapeType["SOLID"], 0, [], 0)

fluid_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fluid_1, [113])

heater_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(heater_1, [2])

fins_1 = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["SOLID"])
geompy.UnionIDs(fins_1, [36])

walls_heater = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls_heater, [4, 24, 14, 32, 28])

base_fins = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(base_fins, [82])

walls_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(walls_fluid, [132, 142, 137, 125])

inlet_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(inlet_fluid, [115])

outlet_fluid = geompy.CreateGroup(fluidHeaterFins, geompy.ShapeType["FACE"])
geompy.UnionIDs(outlet_fluid, [146])

[fluid_1, heater_1, fins_1, walls_heater, base_fins, walls_fluid, inlet_fluid, outlet_fluid] = geompy.GetExistingSubObjects(fluidHeaterFins, False)


geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( heater, 'heater' )
geompy.addToStudy( substrate, 'substrate' )
geompy.addToStudy( Cylinder_1, 'Cylinder_1' )
geompy.addToStudy( Cylinder_2, 'Cylinder_2' )
geompy.addToStudy( Cylinder_3, 'Cylinder_3' )
geompy.addToStudy( fins, 'fins' )
geompy.addToStudy( duct, 'duct' )
geompy.addToStudy( fluid, 'fluid' )
geompy.addToStudy( fluidHeaterFins, 'fluidHeaterFins' )
geompy.addToStudyInFather( fluidHeaterFins, outlet_fluid, 'outlet_fluid' )
geompy.addToStudyInFather( fluidHeaterFins, fluid_1, 'fluid' )
geompy.addToStudyInFather( fluidHeaterFins, heater_1, 'heater' )
geompy.addToStudyInFather( fluidHeaterFins, fins_1, 'fins' )
geompy.addToStudyInFather( fluidHeaterFins, walls_heater, 'walls_heater' )
geompy.addToStudyInFather( fluidHeaterFins, walls_fluid, 'walls_fluid' )
geompy.addToStudyInFather( fluidHeaterFins, base_fins, 'base_fins' )
geompy.addToStudyInFather( fluidHeaterFins, inlet_fluid, 'inlet_fluid' )

import  SMESH, SALOMEDS
from salome.smesh import smeshBuilder

smesh = smeshBuilder.New()
#smesh.SetEnablePublish( False ) # Set to False to avoid publish in study if not needed or in some particular situations:
                                 # multiples meshes built in parallel, complex and numerous mesh edition (performance)

NETGEN_3D_Parameters_1 = smesh.CreateHypothesis('NETGEN_Parameters', 'NETGENEngine')
NETGEN_3D_Parameters_1.SetMaxSize( 20 )
NETGEN_3D_Parameters_1.SetMinSize( 1 )
NETGEN_3D_Parameters_1.SetSecondOrder( 0 )
NETGEN_3D_Parameters_1.SetOptimize( 1 )
NETGEN_3D_Parameters_1.SetFineness( 2 )
NETGEN_3D_Parameters_1.SetChordalError( -1 )
NETGEN_3D_Parameters_1.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_1.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_1.SetFuseEdges( 1 )
NETGEN_3D_Parameters_1.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(fins, 2)
NETGEN_3D_Parameters_1.SetLocalSizeOnShape(heater, 2)
NETGEN_3D_Parameters_1.SetCheckChartBoundary( 32 )
NETGEN_1D_2D_3D = smesh.CreateHypothesis('NETGEN_2D3D', 'NETGENEngine')
try:
  pass
except:
  print('ExportUNV() failed. Invalid file name?')
NETGEN_3D_Parameters_2 = smesh.CreateHypothesis('NETGEN_Parameters', 'NETGENEngine')
NETGEN_3D_Parameters_2.SetMaxSize( 20 )
NETGEN_3D_Parameters_2.SetMinSize( 1 )
NETGEN_3D_Parameters_2.SetSecondOrder( 0 )
NETGEN_3D_Parameters_2.SetOptimize( 1 )
NETGEN_3D_Parameters_2.SetFineness( 2 )
NETGEN_3D_Parameters_2.SetChordalError( -1 )
NETGEN_3D_Parameters_2.SetChordalErrorEnabled( 0 )
NETGEN_3D_Parameters_2.SetUseSurfaceCurvature( 1 )
NETGEN_3D_Parameters_2.SetFuseEdges( 1 )
NETGEN_3D_Parameters_2.SetQuadAllowed( 0 )
NETGEN_3D_Parameters_2.SetLocalSizeOnShape(fins, 2)
NETGEN_3D_Parameters_2.UnsetLocalSizeOnEntry("0:1:1:13")
NETGEN_3D_Parameters_2.SetLocalSizeOnShape(heater, 2)
NETGEN_3D_Parameters_2.SetCheckChartBoundary( 32 )
NETGEN_3D_Parameters_2.UnsetLocalSizeOnEntry("0:1:1:13")
Mesh_1 = smesh.Mesh(fluidHeaterFins,'Mesh_1')
status = Mesh_1.AddHypothesis(NETGEN_3D_Parameters_2)
status = Mesh_1.AddHypothesis(NETGEN_1D_2D_3D)
heater_2 = Mesh_1.GroupOnGeom(heater_1,'heater',SMESH.VOLUME)
fluid_2 = Mesh_1.GroupOnGeom(fluid_1,'fluid',SMESH.VOLUME)
fins_2 = Mesh_1.GroupOnGeom(fins_1,'fins',SMESH.VOLUME)
inlet_fluid_1 = Mesh_1.GroupOnGeom(inlet_fluid,'inlet_fluid',SMESH.FACE)
outlet_fluid_1 = Mesh_1.GroupOnGeom(outlet_fluid,'outlet_fluid',SMESH.FACE)
walls_fluid_1 = Mesh_1.GroupOnGeom(walls_fluid,'walls_fluid',SMESH.FACE)
walls_heater_1 = Mesh_1.GroupOnGeom(walls_heater,'walls_heater',SMESH.FACE)
base_fins_1 = Mesh_1.GroupOnGeom(base_fins,'base_fins',SMESH.FACE)
isDone = Mesh_1.Compute()
[ heater_2, fluid_2, fins_2, inlet_fluid_1, outlet_fluid_1, walls_fluid_1, walls_heater_1, base_fins_1 ] = Mesh_1.GetGroups()
try:
  Mesh_1.ExportUNV( r'C:/Users/sasch/OneDrive/Desktop/MEPhI/Project_practice/FOAM_project/heatExchanger/salome/mesh.unv') # написать про это
  pass
except:
  print('ExportUNV() failed. Invalid file name?')


## Set names of Mesh objects
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
