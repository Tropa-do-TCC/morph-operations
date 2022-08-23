import time
import glob
import pydicom
import numpy as np
from vtkplotter import Volume
import sys, os
from pdb import set_trace

def main(folderPath):
    dir = "ct_images50"
    st = time.time()
    #my_glob = glob.glob1(folderPath, "*")
    numFiles = 0
    rejected = 0
    files = []
    folder = os.listdir(dir)
    # Separate the file names in the folder from the. DCM following them
    for file in folder:
        files.append(dir + "/" + file)
    # return if empty directory
    if len(files) == 0:
        return False

    # get all readable dicom files in  array
    tem = []
    for file in files:
        try:
            data_item = pydicom.dcmread(file)
            if hasattr(data_item, 'SliceLocation'):
                tem.append(data_item)
                numFiles += 1
            else:
                print("veio")
                rejected += 1
                #print(file)
        except Exception as e:
            pass

    print("read done %s | %d files | %d rejected" % (time.time() - st, numFiles, rejected))
    if len(tem) <= 0:
        return False

    tem.sort(key=lambda x: x.InstanceNumber)

    # make 3d np array from all slices
    unset = True
    for i in range(len(tem)):
        arr = tem[i].pixel_array.astype(np.float32)
        if unset:
            imShape = (arr.shape[0], arr.shape[1], len(tem))
            scaledIm = np.zeros(imShape)
            pix_spacing = tem[i].PixelSpacing
            dist = 0
            for j in range(2):
                cs = [float(q) for q in tem[j].ImageOrientationPatient]
                ipp = [float(q) for q in tem[j].ImagePositionPatient]
                parity = pow(-1, j)
                dist += parity*(cs[1]*cs[5] - cs[2]*cs[4])*ipp[0]
                dist += parity*(cs[2]*cs[3] - cs[0]*cs[5])*ipp[1]
                dist += parity*(cs[0]*cs[4] - cs[1]*cs[3])*ipp[2]
            z_spacing = abs(dist)
            slope = tem[i].RescaleSlope
            intercept = tem[i].RescaleIntercept
            unset = False
        scaledIm[:, :, i] = arr

    set_trace()
    # convert to hounsfield units
    scaledIm = slope*scaledIm + intercept
    pix_spacing.append(z_spacing)

    wl = 300    # window parameters for Angio
    ww = 600

    windowed = np.zeros(imShape, dtype=np.uint8)
    # allImages[scaledIm <= (wl-0.5-(ww-1)/2.0)] = 0
    k = np.logical_and(scaledIm > (wl-0.5-(ww-1)/2.0), scaledIm <= (wl-0.5+(ww-1)/2.0))
    windowed[k] = ((scaledIm[k] - (wl-0.5))/(ww-1)+0.5)*255
    windowed[scaledIm > (wl-0.5+(ww-1)/2.0)] = 255
    # windowed image (in 2D) is correct i checked visually in other DICOM viewers
    print("arrays made %s" % (time.time() - st))


    # Volume(scaledIm, spacing=pix_spacing).show(bg="black")
    #Volume(windowed, spacing=pix_spacing).show(bg="black")
    vol = Volume(windowed, spacing=pix_spacing)
    vol.permuteAxes(2,1,0).mirror("y")
    vol.show(bg="black")

    # X, Y, Z = np.mgrid[:30, :30, :30]
    # scalar_field = ((X-15)**2 + (Y-15)**2 + (Z-15)**2)/225
    # Volume(scalar_field, spacing=pix_spacing).show(bg="black")      # looks good on this example


if __name__ == '__main__':
    folder = sys.argv[1]
    main(folder)
