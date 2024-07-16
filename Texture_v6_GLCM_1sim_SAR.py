# -*- coding: cp1252 -*-
from skimage.feature import greycomatrix, greycoprops
import numpy as np
import osgeo.gdal, gdal
from osgeo.gdalconst import *
import time
import sys
import sklearn
#from AccuracyAssesment_PRIN import *
#from Classifiers import *
from HDT_Texture_1409 import *
from matplotlib import pyplot as plt
import pylab
'''
input_img = "C:\Work_Test\\PRIN\\DataExample\\Pavia\\pavia_quickbird_ritaglio2.raw"
input_img = "C:\Work_Test\\PRIN\\DataExample\\DatasetPaviaQB_EnviFolder\\DatasetPaviaQB_EnviFolder\\Pavia_PS_Envi"
training_img = "C:\Work_Test\\PRIN\\DataExample\\IndianPines\\indianpines_ts_raw_classes.raw"
truth_img = "C:\Work_Test\\PRIN\\DataExample\\IndianPines\\indianpines_gt_raw.raw"
'''
#input_img = "C:\Work_Test\\PRIN\\DataExample\\QBPaviaAndSAR\\spot_SAR_LP3_07m_17pts_pol1_nn_subset_SAR"
#input_img = "C:\Work_Test\\PRIN\\DataExample\\Xuzhou-QB\\Xuzhou-QB\\exp2.tif"
#input_img = "C:\\Work_Test\\PRIN\\DataExample\\ASAR_IMP_Beijing\\Subset\\ASA_APP_1PNDPA20100527_141259_000000162089_00440_43079_0008_georef_utm_30m_HH_tif_clip.tif"
input_img = "C:\\Users\\UTENTE\\Desktop\\Fabricio\\LayerStacking_SAR\\SAR_resize_.raw"
#input_img = "C:\\Work_Test\\PRIN\\DataExample\\ASAR_IMP_Beijing\\Subset\\test_stack.raw"


#Read Input image
inb = osgeo.gdal.Open(input_img, GA_ReadOnly)
data = inb.ReadAsArray()
geoTransform = inb.GetGeoTransform()
proj = inb.GetProjection()
n_bands = inb.RasterCount
inb = None

#bright, morph = Morph_Image_Test(data)
GLCM_window_1 = 3
GLCM_window_2 = 5
GLCM_window_3 = 7
GLCM_window_4 = 9

where_are_NaNs = np.isnan(data)
data[where_are_NaNs] = 0

data = data * 10000
morph = GLCM_min_all_plus1Band(data,GLCM_window_1,GLCM_window_2,GLCM_window_3,GLCM_window_4)
#morph = GLCM_min_all_plusBand(data,GLCM_window_1,GLCM_window_2,GLCM_window_3,GLCM_window_4)

driver = gdal.GetDriverByName('GTiff')
driver.Register()
outDataset = driver.Create('C:\\Users\\UTENTE\\Desktop\\Fabricio\\LayerStacking_SAR\\CSK_10m_GLCM_3_5_7_9.tif', data.shape[1], data.shape[0], morph.shape[0], gdal.GDT_Float32)
outDataset.SetGeoTransform(geoTransform )
outDataset.SetProjection(proj)
#outBand = outDataset.GetRasterBand(1)

#Le bande sono al contrario!!! Non sono in ordine corretto...
for band in range(morph.shape[0]):
    outBand=outDataset.GetRasterBand(band+1)
    outBand.WriteArray(morph[band,:,:], 0, 0)

outBand = None
outDataset = None
