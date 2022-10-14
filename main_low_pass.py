from pdb import set_trace
from scipy import fftpack
import numpy as np
import imageio
from PIL import Image, ImageDraw
import numpy as np
import pydicom
from pydicom.pixel_data_handlers.util import apply_voi_lut
from scipy.signal import butter, lfilter, freqz
from PIL import Image, ImageFilter
import cv2


path = "./CT000000.dcm"

def low_pass_filter2(data, band_limit=1000, sampling_rate=44100):
    cutoff_index = int(band_limit * data.size / sampling_rate)
    F = np.fft.fft(data)
    F[cutoff_index + 1 : -cutoff_index] = 0
    return np.fft.ifft(F).real

def convert(matrix):
    from PIL import Image
    import numpy as np
    set_trace()
    PIL_image = Image.fromarray(np.uint8(matrix)).convert('RGB')

    PIL_image = Image.fromarray(matrix.astype('uint8'), 'RGB')
    return PIL_image

def read_xray2(path):
    #dicom = pydicom.read_file(path)
    dicom = pydicom.dcmread(path)
    return dicom.pixel_array

    def low_pass_filter(adata: np.ndarray, bandlimit: int = 1000, sampling_rate: int = 44100) -> np.ndarray:
            set_trace()
            # translate bandlimit from Hz to dataindex according to sampling rate and data size
            bandlimit_index = int(bandlimit * adata.size / sampling_rate)

            fsig = np.fft.fft(adata)

            for i in range(bandlimit_index + 1, len(fsig) - bandlimit_index ):
                fsig[i] = 0

            adata_filtered = np.fft.ifft(fsig)

            return np.real(adata_filtered)

    def test(matrix):
        image1_np = matrix #read_xray2("./CT000000.dcm")

        #set_trace()

        #fft of image
        fft1 = fftpack.fftshift(fftpack.fft2(image1_np))

        #Create a low pass filter image
        x,y = image1_np.shape[0],image1_np.shape[1]
        #size of circle
        e_x,e_y=50,50
        #create a box
        bbox=((x/2)-(e_x/2),(y/2)-(e_y/2),(x/2)+(e_x/2),(y/2)+(e_y/2))

        low_pass=Image.new("L",(image1_np.shape[0],image1_np.shape[1]),color=0)

        draw1=ImageDraw.Draw(low_pass)
        draw1.ellipse(bbox, fill=1)

        low_pass_np=np.array(low_pass)

        #multiply both the images
        filtered=np.multiply(fft1,low_pass_np)

        #inverse fft
        ifft2 = np.real(fftpack.ifft2(fftpack.ifftshift(filtered)))
        ifft2 = np.maximum(0, np.minimum(ifft2, 255))

        return ifft2

dicom = pydicom.dcmread(path)
matrix = dicom.pixel_array
print(dicom.pixel_array.shape)
#set_trace()

#dicom.PixelData = test(dicom.pixel_array)
#converted = convert(dicom.pixel_array)
for i in range(30):
    try:
        dicom.PixelData = cv2.GaussianBlur(matrix, (i,i), 0)


    #save the image
        imageio.imsave(f'image{i}.jpg', dicom.PixelData.astype(np.uint8))
        dicom.save_as(r"./result.dcm")
    except:
        pass
#dicom.save_as(r"./result.dcm")
