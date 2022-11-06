import os
import numpy as np
from pydicom import dcmread
import imageio
from tqdm import tqdm
from skimage import exposure

import sys

def load_dicom(path):
    print("Loading scan", path)
    slices = [dcmread(path / s) for s in os.listdir(path)]
    slices.sort(key = lambda x: float(x.ImagePositionPatient[2]))
    return slices


"""
Convert the DICOM pixel_array values to the corresponding HU values.
If oor_filter (out of region filter) is set to True, then the region outside the chest will be set to zero before conversion to HU.
This correspondslice to setting this region to the value of air.
"""
def to_hu(slices, oor_filter=True):
    images = np.stack([ s.pixel_array for s in slices]).astype(np.int16)
    
    # oor_filter , out of region filter
    if oor_filter:
        images[images <= -1000] = 0
    
    for n in range(len(slices)):
        slope = slices[n].RescaleSlope
        intercept = slices[n].RescaleIntercept
        
        images[n] = slope * images[n].astype(np.float64)
        images[n] = images[n].astype(np.int16)
        images[n] += np.int16(intercept)
        
    return np.array(images, dtype=np.int16)



def affine3d(slices):
    dslice = slices[0]
    F11, F21, F31 = dslice.ImageOrientationPatient[3:]
    F12, F22, F32 = dslice.ImageOrientationPatient[:3]

    n1, n2, n3 = np.cross(dslice.ImageOrientationPatient[3:], dslice.ImageOrientationPatient[:3])

    dr, dc = dslice.PixelSpacing
    ds = np.abs(slices[0].ImagePositionPatient[2] - slices[1].ImagePositionPatient[2])
    Sx, Sy, Sz = dslice.ImagePositionPatient

    return np.array(
        [
            [F11 * dr, F12 * dc, ds * n1, Sx],
            [F21 * dr, F22 * dc, ds * n2, Sy],
            [F31 * dr, F32 * dc, ds * n3, Sz],
            [0, 0, 0, 1]
        ]
    )


"""
For this function I am not sure on the best values for the in_range. Should I use the same allong all the slices
or optimize it to obtain better contrast for each slice, but then loosing consistency between slices.

TODO:
    - Optimize the GIF. File is too large and takes too long to view.
    - Choose a value for in_range.
"""
def gifshow(img_stack, filename):
    minv = np.min(img_stack)
    maxv = np.max(img_stack)

    print("start:\t rescaling images")
    rescaled = np.stack([
        exposure.rescale_intensity(img, in_range=(minv, 500),out_range = np.uint8) for img in tqdm(img_stack[::5])
    ])
    imageio.mimsave(filename, rescaled, duration=0.1)
    return #Image(filename=filename, format='png')

