#!/usr/bin/env python

# noinspection PyUnresolvedReferences
from pdb import set_trace
import vtk.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtk.vtkRenderingOpenGL2
from vtk.vtkCommonColor import vtkNamedColors

from vtk.vtkCommonDataModel import vtkImageData
from vtk.vtkFiltersCore import (
    vtkFlyingEdges3D,
    vtkMarchingCubes
)
from vtk.vtkFiltersSources import vtkSphereSource
from vtk.vtkIOImage import vtkDICOMImageReader
from vtk.vtkImagingHybrid import vtkVoxelModeller
from vtk.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)
from vtkmodules.vtkRenderingCore import vtkProp3D


def main(path, iso):
    # vtkFlyingEdges3D was introduced in VTK >= 8.2
    use_flying_edges = vtk_version_ok(8, 2, 0)

    colors = vtkNamedColors()

    dicom_dir = path
    iso_value = iso
    if iso_value is None and dicom_dir is not None:
        print('An ISO value is needed.')
        return ()
    set_trace()
    volume = vtkImageData()
    reader = vtkDICOMImageReader()
    reader.SetDirectoryName(dicom_dir)
    reader.Update() # para aqui
    volume.DeepCopy(reader.GetOutput())

    if use_flying_edges:
        try:
            surface = vtkFlyingEdges3D()
        except AttributeError:
            surface = vtkMarchingCubes()
    else:
        surface = vtkMarchingCubes()
    surface.SetInputData(volume)
    surface.ComputeNormalsOn()
    surface.SetValue(0, iso_value)

    renderer = vtkRenderer()
    renderer.SetBackground(colors.GetColor3d('Black'))

    render_window = vtkRenderWindow()
    render_window.AddRenderer(renderer)
    render_window.SetWindowName('Cranial Reconstruction: ' + path)
    render_window.SetSize(1500, 800)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(render_window)

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(surface.GetOutputPort())
    mapper.ScalarVisibilityOff()

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(colors.GetColor3d('Green'))

    # pointPicker = vtk.vtkPointPicker()
    # pointPicker.PickFromListOn()
    # try:
    #     pointPicker.SetUseCells(True)
    # except:
    #     print("Warning, vtkPointPicker patch not installed, picking will not work properly.")
    renderer.AddActor(actor)
    renderer.ResetCamera()

#    pointPicker.InitializePickList()
#    interactor.SetPicker(pointPicker)
    render_window.Render()
    interactor.Start()


def vtk_version_ok(major, minor, build):
    """
    Check the VTK version.

    :param major: Major version.
    :param minor: Minor version.
    :param build: Build version.
    :return: True if the requested VTK version is greater or equal to the actual VTK version.
    """
    needed_version = 10000000000 * int(major) + 100000000 * int(minor) + int(build)

    vtk_version_number = 10000000000 * vtk.VTK_MAJOR_VERSION + 100000000 * vtk.VTK_MINOR_VERSION \
                         + vtk.VTK_BUILD_VERSION
    if vtk_version_number >= needed_version:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
