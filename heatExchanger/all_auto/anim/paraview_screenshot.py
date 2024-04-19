from paraview.simple import *
import os

file_path = '/home/alexesn/FOAM_project/heatExchanger/all_auto/'
file_name = 'view.foam'
post = '/postProcessing/fins/cellMaxFinT/0/volFieldValue.dat'
i = 0
max = 1000

data = {}
for root, dirs, files in os.walk(file_path):
    if i > max:
        break
    for dir_name in dirs:
        i += 1
        if i > max:
            break
        if "case" in dir_name.lower():
            file_full = f'{file_path}{dir_name}'
            try:
                with open(f'{file_full}/postProcessing/fins/cellMaxFinT/0/volFieldValue.dat', 'r') as file:
                    lines = file.readlines()
                    for line in reversed(lines):
                        if line.strip():
                            last_value = float(line.split()[-1])
                            data[f'{file_full}/{file_name}'] = last_value
                            break
            except:
                print("error")

data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
print(data)
i = 0
previous_source = None
prev_clip = None
for f in data:
    i += 1
    # Очистка предыдущего источника данных и его отображения
    if previous_source:
        Delete(previous_source)
    if prev_clip:
        Delete(prev_clip)
    # disable automatic camera reset on 'Show'
    paraview.simple._DisableFirstRenderCameraReset()
    # create a new 'OpenFOAMReader'
    viewfoam = OpenFOAMReader(registrationName='view.foam',
                              FileName=f)
    viewfoam.MeshRegions = ['/fins/internalMesh',
                            '/fluid/internalMesh', '/heater/internalMesh']
    viewfoam.CellArrays = ['T', 'U', 'p', 'p_rgh', 'rho']

    # get animation scene
    animationScene1 = GetAnimationScene()

    # get the time-keeper
    timeKeeper1 = GetTimeKeeper()

    # update animation scene based on data timesteps
    animationScene1.UpdateAnimationUsingDataTimeSteps()

    # get active view
    renderView1 = GetActiveViewOrCreate('RenderView')

    # show data in view
    viewfoamDisplay = Show(viewfoam, renderView1,
                           'UnstructuredGridRepresentation')

    # trace defaults for the display properties.
    viewfoamDisplay.Representation = 'Surface'
    viewfoamDisplay.ColorArrayName = [None, '']
    viewfoamDisplay.SelectTCoordArray = 'None'
    viewfoamDisplay.SelectNormalArray = 'None'
    viewfoamDisplay.SelectTangentArray = 'None'
    viewfoamDisplay.OSPRayScaleArray = 'T'
    viewfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
    viewfoamDisplay.SelectOrientationVectors = 'None'
    viewfoamDisplay.ScaleFactor = 0.006999999843537808
    viewfoamDisplay.SelectScaleArray = 'None'
    viewfoamDisplay.GlyphType = 'Arrow'
    viewfoamDisplay.GlyphTableIndexArray = 'None'
    viewfoamDisplay.GaussianRadius = 0.0003499999921768904
    viewfoamDisplay.SetScaleArray = ['POINTS', 'T']
    viewfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
    viewfoamDisplay.OpacityArray = ['POINTS', 'T']
    viewfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'
    viewfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
    viewfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
    viewfoamDisplay.ScalarOpacityUnitDistance = 0.0018580432374278543
    viewfoamDisplay.OpacityArrayName = ['POINTS', 'T']
    viewfoamDisplay.SelectInputVectors = ['POINTS', 'T']
    viewfoamDisplay.WriteLog = ''

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    viewfoamDisplay.ScaleTransferFunction.Points = [
        28.988758087158203, 0.0, 0.5, 0.0, 62.895633697509766, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    viewfoamDisplay.OpacityTransferFunction.Points = [
        28.988758087158203, 0.0, 0.5, 0.0, 62.895633697509766, 1.0, 0.5, 0.0]

    # reset view to fit data
    renderView1.ResetCamera(False)

    # get the material library
    materialLibrary1 = GetMaterialLibrary()

    # update the view to ensure updated data information
    renderView1.Update()

    # set scalar coloring
    ColorBy(viewfoamDisplay, ('FIELD', 'vtkBlockColors'))

    # show color bar/color legend
    viewfoamDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'vtkBlockColors'
    vtkBlockColorsLUT = GetColorTransferFunction('vtkBlockColors')

    # get opacity transfer function/opacity map for 'vtkBlockColors'
    vtkBlockColorsPWF = GetOpacityTransferFunction('vtkBlockColors')

    # get 2D transfer function for 'vtkBlockColors'
    vtkBlockColorsTF2D = GetTransferFunction2D('vtkBlockColors')

    # set scalar coloring
    ColorBy(viewfoamDisplay, ('POINTS', 'T'))

    # Hide the scalar bar for this color map if no visible data is colored by it.
    HideScalarBarIfNotNeeded(vtkBlockColorsLUT, renderView1)

    # rescale color and/or opacity maps used to include current data range
    viewfoamDisplay.RescaleTransferFunctionToDataRange(True, False)

    # show color bar/color legend
    viewfoamDisplay.SetScalarBarVisibility(renderView1, True)

    # get color transfer function/color map for 'T'
    tLUT = GetColorTransferFunction('T')

    # get opacity transfer function/opacity map for 'T'
    tPWF = GetOpacityTransferFunction('T')

    # get 2D transfer function for 'T'
    tTF2D = GetTransferFunction2D('T')

    # create a new 'Clip'
    clip1 = Clip(registrationName='Clip1', Input=viewfoam)
    clip1.ClipType = 'Plane'
    clip1.HyperTreeGridClipper = 'Plane'
    clip1.Scalars = ['POINTS', 'T']
    clip1.Value = 45.942195892333984

    # init the 'Plane' selected for 'ClipType'
    clip1.ClipType.Origin = [0.024999999441206455,
                             0.024999999441206455, 0.026499999687075615]

    # init the 'Plane' selected for 'HyperTreeGridClipper'
    clip1.HyperTreeGridClipper.Origin = [
        0.024999999441206455, 0.024999999441206455, 0.026499999687075615]

    # Properties modified on clip1.ClipType
    clip1.ClipType.Normal = [-0.013608669783618311, -
                             0.189765708962505, 0.9817350863693721]

    # show data in view
    clip1Display = Show(clip1, renderView1, 'UnstructuredGridRepresentation')

    # trace defaults for the display properties.
    clip1Display.Representation = 'Surface'
    clip1Display.ColorArrayName = ['POINTS', 'T']
    clip1Display.LookupTable = tLUT
    clip1Display.SelectTCoordArray = 'None'
    clip1Display.SelectNormalArray = 'None'
    clip1Display.SelectTangentArray = 'None'
    clip1Display.OSPRayScaleArray = 'T'
    clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
    clip1Display.SelectOrientationVectors = 'None'
    clip1Display.ScaleFactor = 0.006999999843537808
    clip1Display.SelectScaleArray = 'None'
    clip1Display.GlyphType = 'Arrow'
    clip1Display.GlyphTableIndexArray = 'None'
    clip1Display.GaussianRadius = 0.0003499999921768904
    clip1Display.SetScaleArray = ['POINTS', 'T']
    clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
    clip1Display.OpacityArray = ['POINTS', 'T']
    clip1Display.OpacityTransferFunction = 'PiecewiseFunction'
    clip1Display.DataAxesGrid = 'GridAxesRepresentation'
    clip1Display.PolarAxes = 'PolarAxesRepresentation'
    clip1Display.ScalarOpacityFunction = tPWF
    clip1Display.ScalarOpacityUnitDistance = 0.002086905966088798
    clip1Display.OpacityArrayName = ['POINTS', 'T']
    clip1Display.SelectInputVectors = ['POINTS', 'T']
    clip1Display.WriteLog = ''

    # init the 'PiecewiseFunction' selected for 'ScaleTransferFunction'
    clip1Display.ScaleTransferFunction.Points = [
        28.991281509399414, 0.0, 0.5, 0.0, 62.895633697509766, 1.0, 0.5, 0.0]

    # init the 'PiecewiseFunction' selected for 'OpacityTransferFunction'
    clip1Display.OpacityTransferFunction.Points = [
        28.991281509399414, 0.0, 0.5, 0.0, 62.895633697509766, 1.0, 0.5, 0.0]

    # hide data in view
    Hide(viewfoam, renderView1)

    # show color bar/color legend
    clip1Display.SetScalarBarVisibility(renderView1, True)

    # update the view to ensure updated data information
    renderView1.Update()

    animationScene1.GoToLast()

    # change interaction mode for render view
    renderView1.InteractionMode = '2D'

    # change interaction mode for render view
    renderView1.InteractionMode = '3D'

    # get layout
    layout1 = GetLayout()

    # layout/tab size in pixels
    layout1.SetSize(989, 799)

    # current camera placement for renderView1
    renderView1.CameraPosition = [
        0.05394425315602717, -0.16007324816233232, 0.1358962973777826]
    renderView1.CameraFocalPoint = [
        0.024999999441206452, 0.024999999441206455, 0.0264999996870756]
    renderView1.CameraViewUp = [0.06704942617865282,
                                0.5154544867838006, 0.8542897907054504]
    renderView1.CameraParallelScale = 0.056144900693575674

    # save screenshot
    SaveScreenshot(f'/home/alexesn/FOAM_project/heatExchanger/all_auto/anim/sc/T{i:03d}.png',
                   renderView1, ImageResolution=[844, 539])
    previous_source = viewfoam
    prev_clip = clip1
