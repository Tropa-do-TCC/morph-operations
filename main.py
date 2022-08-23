import os

import pydicom

from filtters_operation import gaussian_filter, blur_filter
from morph_operations import apply_closing, apply_opening
import reconstruction_vtk
from pdb import set_trace

# dicom folders
INPUT_FILES = "ct_images50"
OUTPUT_FILES = "ct_images_processed"


def read_files_dcm(path_folder):
    # Get all picture names
    files = []
    folder = os.listdir(path_folder)
    # Separate the file names in the folder from the. DCM following them
    for file in folder:
        files.append(path_folder + "/" + file)

    return files


def pre_processing(image):
    image_filtered = blur_filter(image)
    image_op_morpho = apply_closing(image_filtered)
    return image_op_morpho


def convert_images_to_process_and_save(files):
    numFiles = rejected = 0
    set_trace()
    for file in files:
        medical_image = pydicom.dcmread(file)
        if hasattr(medical_image, 'SliceLocation'):
            numFiles += 1
            # medical_image.file_meta.fix_meta_info()
            image_read = medical_image.pixel_array

            var = pre_processing(image_read)
            medical_image.PixelData = var
            set_trace()
            medical_image.save_as("./" + OUTPUT_FILES + "/" + file.split("/")[2])
        else:
            rejected += 1
    print("%d files | %d rejected" % (numFiles, rejected))

reconstruction_vtk.main(INPUT_FILES, 100)

read_images = read_files_dcm("./" + INPUT_FILES)
convert_images_to_process_and_save(read_images)
set_trace()
reconstruction_vtk.main(OUTPUT_FILES, 100)
