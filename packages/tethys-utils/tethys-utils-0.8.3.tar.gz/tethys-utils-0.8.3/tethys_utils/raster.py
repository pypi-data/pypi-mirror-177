#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  7 09:29:29 2021

@author: mike
"""
import numpy as np
import xarray as xr
import pandas as pd
import os
import glob
# from tethys_utils.processing import write_pkl_zstd, process_datasets, prepare_results, assign_station_id, make_run_date_key
# from tethys_utils.s3 import process_run_date, update_results_s3, put_remote_dataset, put_remote_agg_stations, put_remote_agg_datasets, s3_connection
from tethys_utils import misc, s3, processing, titan, data_io, grid
from shapely.geometry import shape, mapping, Point, box
import copy
import rasterio
import concurrent.futures
import multiprocessing as mp
import rioxarray as rxr
from hdf5tools import H5, xr_to_hdf5
import uuid

###########################################
### Parameters


############################################
### Functions


def parse_images(glob_str_dict):
    """

    """
    raster_dict = {}
    for param, glob_str in glob_str_dict.items():
        if isinstance(glob_str, str):
            f2 = glob.glob(glob_str)
        elif isinstance(glob_str, list):
            f2 = glob_str.copy()
        else:
            raise TypeError

        f3 = {f: os.path.getsize(f) for f in f2}
        max1 = max(f3.values())
        max_f = [f for f in f3 if f3[f] == max1][0]

        raster_dict[param] = {'images': f3, 'max_image': max_f}

    return raster_dict


def raster_file_checks(file):
    """

    """
    src = rasterio.open(file)
    crs = src.crs

    if crs.to_epsg() != 4326:
        raise ValueError('Raster CRS is in epsg: ' + str(crs) + ', but should be 4326')

    src.close()


def process_raster(image, parameter, encodings, output_path, time, height, x_name='x', y_name='y', band=1):
    """

    """
    time1 = pd.Timestamp(time)

    xr1 = rxr.open_rasterio(image, mask_and_scale=True)
    xr1 = xr1.rename({x_name: 'lon', y_name: 'lat'}).sel(band=band).drop(['band', 'spatial_ref']).sortby(['lon', 'lat'])
    xr1 = xr1.assign_coords(height=height).expand_dims('height', axis=2)
    xr1 = xr1.assign_coords(time=time1).expand_dims('time')
    xr1.name = parameter
    enc = encodings[parameter]
    xr1.encoding = enc
    xr1 = xr1.to_dataset()

    for coord in list(xr1.coords):
        xr1[coord].encoding = processing.base_encoding[coord]

    file_name = os.path.splitext(os.path.split(image)[-1])[0] + '.h5'
    output = os.path.join(output_path, file_name)
    xr_to_hdf5(xr1, output)

    return output


############################################
### Class


class Raster(grid.Grid):
    """

    """
    ## Initial import and assignment function
    def import_rasters(self, source_paths_dict, time, height, x_name='x', y_name='y', band=1):
        """

        """
        misc.diagnostic_check(self.diagnostics, 'load_dataset_metadata')

        raster_dict = parse_images(source_paths_dict)

        for param in raster_dict:
            ## Run checks
            raster_file_checks(raster_dict[param]['max_image'])

            raster_dict[param].update({'time': time, 'band': band, 'height': height, 'x_name': x_name, 'y_name': y_name})

        setattr(self, 'raster_attrs', raster_dict)

        return raster_dict


    def process_rasters(self, remove_source_images=False, max_workers=3):
        """

        """
        raster_attrs = copy.deepcopy(self.raster_attrs)

        ## Merge images
        dataset = self.dataset_list[0]
        parameter = dataset['parameter']
        ds_id = dataset['dataset_id']
        encodings = dataset['properties']['encoding']
        time1 = pd.Timestamp(raster_attrs[parameter]['time']).round('S')
        time_str = time1.strftime('%Y%m%d%H%M%S')

        ## Iterate through files
        file_paths = []
        if max_workers <= 1:
            for param in raster_attrs:
                dict1 = raster_attrs[param].copy()
                files = dict1.pop('images')
                _ = dict1.pop('max_image')

                dict1['parameter'] = param
                dict1['encodings'] = encodings
                dict1['output_path'] = self.preprocessed_path

                for file in files:
                    dict1['image'] = file
                    new_paths0 = process_raster(**dict1)
                    file_paths.append(new_paths0)
        else:
            with concurrent.futures.ProcessPoolExecutor(max_workers=max_workers, mp_context=mp.get_context("spawn")) as executor:
                futures = []
                for param in raster_attrs:
                    dict1 = raster_attrs[param].copy()
                    files = dict1.pop('images')
                    _ = dict1.pop('max_image')

                    dict1['parameter'] = param
                    dict1['encodings'] = encodings
                    dict1['output_path'] = self.preprocessed_path

                    for file in files:
                        dict1['image'] = file
                        f = executor.submit(process_raster, **dict1)
                        futures.append(f)
                runs = concurrent.futures.wait(futures)

            file_paths = [r.result() for r in runs[0]]

        file_paths.sort()

        file_id = uuid.uuid4().hex[:14]

        merged_h5 = os.path.join(self.preprocessed_path, '{ds_id}_{file_id}_{time}.h5'.format(time=time_str, ds_id=ds_id, file_id=file_id))

        h1 = H5(file_paths)
        h1.to_hdf5(merged_h5)

        if remove_source_images:
            for i in file_paths:
                os.remove(i)

        return merged_h5


    # def open_big_one(self):
    #     """

    #     """
    #     xr1 = xr.open_rasterio(self.max_image)

    #     return xr1


    # def determine_grid_block_size(self, starting_x_size=100, starting_y_size=100, increment=100, min_size=800, max_size=1100):
    #     """

    #     """
    #     parameter = self.grid.datasets[0]['parameter']
    #     xr1 = process_image(self.max_image, parameter, x_name=self.x_name, y_name=self.y_name, band=1)
    #     self.grid.load_data(xr1.to_dataset(), parameter, self.time, self.height)
    #     size_dict = self.grid.determine_grid_block_size(starting_x_size, starting_y_size, increment, min_size, max_size)

    #     setattr(self, 'grid_size_dict', size_dict)

    #     res = xr1.attrs['res'][0]
    #     setattr(self, 'grid_res', res)

    #     return size_dict


    # def save_results(self, x_size, y_size, threads=30):
    #     """

    #     """
    #     ## Iterate through the images
    #     images = list(self.images.keys())
    #     images.sort()

    #     for tif in images:
    #         print(tif)

    #         parameter = self.grid.datasets[0]['parameter']
    #         xr1 = process_image(self.max_image, parameter, x_name=self.x_name, y_name=self.y_name, band=1)
    #         self.grid.load_data(xr1.to_dataset(), parameter, self.time, self.height)

    #         self.grid.save_results(x_size, y_size, threads=threads)










