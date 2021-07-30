#!/usr/bin/env python

'''this script generates pcp data for every pixel (CHIRPS data) from 01/01/1981
        however, the start date can be changed depending on the downloaded tif files.

Author  : albert nkwasa
Contact : nkwasa.albert@gmail.com / albert.nkwasa@vub.be 
Date    : 2021.07.30

'''

import geopandas as gpd
import rasterio
import gdal
import os
import xarray as xr
import numpy as np
from pyproj import Proj, transform
from affine import Affine
import pandas as pd
from shapely.geometry import Point
import warnings
import shutil
warnings.filterwarnings("ignore")

working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)

master_file = 'chirps_master.tif'
clip = 'clip.tif'
shp = '#put the name of the shape file here e.g victoria_basin.shp'
shp_rep = '{}_rep.shp'.format(shp.split('.')[0])
# src_dem = 'mara_basin_dem.tif'
dem_africa = 'africa_dem.tif'

os.system('ogr2ogr {} -s_srs EPSG:3395 -t_srs "EPSG:4326" {}'.format(shp_rep, shp))
os.system('gdalwarp -overwrite -of GTiff -cutline {} -crop_to_cutline -r mode {} {}'.format(shp_rep, master_file, clip))

# extract lists of center coordinates of the clipped raster file
with rasterio.open(clip) as src:
    src_band = src.read()
    src_trans = src.transform
    src_proj = Proj(src.crs)
cols, rows = np.meshgrid(
    np.arange(src_band.shape[2]), np.arange(src_band.shape[1]))
src_affine = src_trans*Affine.translation(0.5, 0.5)


def rs2en(src, c):
    return src_affine*(c, src)


eastings, northings = np.vectorize(
    rs2en, otypes=[np.float, np.float])(rows, cols)


p2 = Proj(proj='latlong', datum='WGS84')
longs, lats = transform(src_proj, p2, eastings, northings)
lats_flat = lats.flatten()
lats_list = lats_flat.tolist()
longs_flat = longs.flatten()
longs_list = longs_flat.tolist()


# precipitation stations shapefile
df_lats = pd.DataFrame(lats_list, columns=['X'])
df_longs = pd.DataFrame(longs_list, columns=['Y'])
df_longs['X'] = df_lats['X'].values
df_longs['geometry'] = df_longs.apply(lambda row: Point(row.X, row.Y), axis=1)
crs = {'init': 'epsg:4326'}
gdf = gpd.GeoDataFrame(df_longs, crs=crs)
coord_points = 'pcp_stations.shp'
gdf.to_file(coord_points, driver='ESRI Shapefile')

try:
    os.makedirs(f"pcp")
except:
    pass

os.chdir(f'{working_dir}/extracted_tifs')

pcp_list = []
elevation_list = []
index = 0
for i, j in zip(lats_list, longs_list):
    empty = []
    for files in os.listdir():
        if files.endswith('.tif'):
            xarr = xr.open_rasterio(files)
            val = xarr.sel(x=i, y=j, method="nearest")
            empty.append(val.values)
    df = pd.DataFrame(empty)
    df = df.rename(columns={0: '19810101'})
    df['19810101'] = df['19810101'].apply(lambda x: round(x, 2))
    pre_name = 'stpcp{}'.format(1001 + index)
    file_name = '{}.txt'.format(pre_name)
    df.to_csv(f'{working_dir}/pcp/{file_name}',
              sep='\t', index=False)
    # creating the pcp file
    pcp_list.append(
        {'NAME': pre_name, 'LAT': round(j, 3), 'LONG': round(i, 3)})
    # reading the elevation values
    dataset = gdal.Open(f'{working_dir}/{dem_africa}')
    band = dataset.GetRasterBand(1)
    cols = dataset.RasterXSize
    rows = dataset.RasterYSize

    transform = dataset.GetGeoTransform()

    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = -transform[5]

    data = band.ReadAsArray(0, 0, cols, rows)
    col = int((i - xOrigin) / pixelWidth)
    row = int((yOrigin - j) / pixelHeight)
    elevation_list.append(data[row][col])
    index += 1
    dataset = None

df_pcp = pd.DataFrame(pcp_list)
df_pcp.index = df_pcp.index+1
df_pcp.index.name = 'ID'
df_pcp = df_pcp.assign(ELEVATION=elevation_list)
df_pcp.to_csv(f'{working_dir}/pcp/pcp.txt', sep=',')

os.chdir(working_dir)
# deleting created files
for k in os.listdir():
    if k.endswith('.tif') or k.startswith(str((shp.split('.')[0]))):
        os.remove(k)
try:
    shutil.rmtree(f'{os.getcwd()}/extracted_tifs')
except:
    pass

print('\t >finished')
