__author__ = "lucabasa"
__version__ = "1.0.0"

"""
Methods to import a department, 
including police data, census data, and shapefiles
"""

from data_quality import list_all_files

import pandas as pd
import numpy as np

import geopandas as gp

import gc



def import_topic(path, tolerance=0.7):
    """
    Imports the file at a given location,
    Coerces the values to be numerical in order to easily spot the missing values
    Drops every column with enough missing values, the threshold is set by the parameter tolerance
    
    It returns 2 DataFrames: one with the data, one with the metadata.
    """
    # find the file with the ACS data and load it
    datafile = list_all_files(path, pattern='_with_ann.csv')[0]
    data = pd.read_csv(datafile, skiprows=[1], low_memory=False)
    # take out the ids momentarily
    ids = data[[col for col in data.columns if 'GEO' in col]]
    rest = data[[col for col in data.columns if 'GEO' not in col]]
    # convert to numeric and force na's if necessary
    rest = rest.apply(pd.to_numeric, errors='coerce')
    # put data together again
    data = ids.join(rest)
    print(f'Shape: {data.shape}')
    cols = data.columns
    nrows = data.shape[0]
    removed = 0
    for col in cols:
        mis = data[col].isnull().sum() / nrows
        if mis > tolerance:
            removed += 1
            del data[col]
    if removed > 0:
        print("Removed {} columns because more than {}% of the values are missing".format(removed, 
                                                                                      tolerance*100))
        print(f"New shape: {data.shape}")
    meta = datafile.replace('_with_ann.csv', '_metadata.csv')
    metadata = pd.read_csv(meta, header=None, names=['key', 'description'])
    return data, metadata


def import_dept(location):
    """
    Imports all the police files, the ACS, the shapefiles at a given location
    
    It returns a dictionary of DataFrames
    """
    dept_num = location.split('_')[1]
    print(f'Importing department {dept_num}')
    print('\n')
    data_list = {}
    # Police data ------------------------
    print("Importing police data...")
    crime_files = list_all_files(location, pattern='.csv', recursive=False)
    crm_count = 1
    for crm in crime_files:
        crm_name = "police_" + str(crm_count)
        data_list[crm_name] = pd.read_csv(crm, skiprows=[1], low_memory=False)
        print("File {}, shape: {}".format(crm_count,
                                         data_list[crm_name].shape))
        crm_count += 1
    # ACS -------
    data_path = location + '/' + dept_num + '_ACS_data/'
    topics = listdir(data_path)
    for topic in topics:
        topic_name = topic.split('_')[-1]
        print(f'Importing {topic_name}...')
        data, meta = import_topic(data_path + topic, tolerance=0.3)  # I am being more strict than the default
        data_list[topic_name] = data
        data_list[topic_name + '_meta'] = meta    
    # Shapefiles -----
    print("Importing shapefile(s)...")
    data_path = location + '/' + dept_num + '_Shapefiles/'
    shapes = list_all_files(data_path, pattern='.shp')
    shapes = [shp for shp in shapes if shp.endswith('.shp')]
    shp_count = 1
    for shp in shapes:
        shp_name = 'shapefile_' + str(shp_count)
        data_list[shp_name] = gp.read_file(shp)
        print("File {}, shape: {}".format(shp_count,
                                         data_list[shp_name].shape))
        shp_count += 1
    gc.collect() # in case some of the files were really big
    return data_list
    
