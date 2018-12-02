__author__ = "lucabasa"
__version__ = "1.0.0"

"""
Methods to quickly check the quality of the data
"""


from os.path import join, isfile
from os import path, scandir, listdir

import pandas as pd
import numpy as np



def list_all_files(location='../input/', pattern=None, recursive=True):
    """
    This function returns a list of files at a given location (including subfolders)
    
    - location: path to the directory to be searched
    - pattern: part of the file name to be searched (ex. pattern='.csv' would return all the csv files)
    - recursive: boolean, if True the function calls itself for every subdirectory it finds
    """
    subdirectories= [f.path for f in scandir(location) if f.is_dir()]
    files = [join(location, f) for f in listdir(location) if isfile(join(location, f))]
    if recursive:
        for directory in subdirectories:
            files.extend(list_all_files(directory))
    if pattern:
        files = [f for f in files if pattern in f]
    return files


def _get_topics(topics_list):
    for topic in topics_list:
        topics_list[topics_list.index(topic)] = topic.split('_')[-1]
    return topics_list


def check_topics(dept_num, base_topics, test_topics):
    """
    This function checks that a department has all the topics (education, poverty, etc.)
    that are present in the other departments.
    
    - dept_num: string identifying the department
    - base_topics: list of topics that the other departments have (if empty, it is created)
    - test_topics: topics found for the given department
    
    If there are new topics, the function updates base_topics and returns it
    """
    test_topics = _get_topics(test_topics)
    if len(base_topics) < 1:
        base_topics = test_topics  # the first time just create the list
    # check if something is missing
    mis_topics = [top for top in base_topics if top not in test_topics]
    if len(mis_topics) > 0:
        print(f"Department {dept_num} does not have data about the following topics:")
        print(mis_topics)
    # check if something is new
    new_topics = [top for top in test_topics if top not in base_topics]
    if len(new_topics) > 0:
        print(f"Department {dept_num} has data about the following new topics:")
        print(new_topics)
        print("The departments previously checked do not have these data")
        # updating the base_topics
        base_topics = list(set(base_topics + test_topics))
    return base_topics


def check_ids(base_ids, data):
    """
    This function checks that, across the topics, the id's are consistent
    """
    tmp_ids = data['GEO.id2'].unique()
    if len(tmp_ids) != data.shape[0]:
        print(f"In {file} inconsistent id's")
    if len(base_ids) < 1: # the first time it creates the "base" of id's
        base_ids = tmp_ids
    if set(tmp_ids) != set(base_ids):
        print(f"In {file} inconsistent id's with the other files")
    return base_ids


def data_quality(location='../input/data-science-for-good/cpe-data/'):
    """
    This is the main function, it checks every department at the given location,
    assuming that every department is in a separate directory.
    
    It checks for:
    - presence of police related data
    - consistency of the ACS files (and relative metadata)
    - presence of all the necessary shapefiles
    """
    # Get the list of the departments
    dept_list = [d.path for d in scandir(location) if d.is_dir()]
    topics = []  # needed to check if we have all
    
    # loop over departments
    for dept in dept_list:
        dept_num = dept.split('_')[1]
        print("_"*40)
        print(f'Checking department {dept_num}')
        
        # Check if we have some kind of data about crime or police-------------
        crime_files = list_all_files(dept, pattern='.csv', recursive=False)
        if len(crime_files) < 1:
            print(f"Department {dept_num} does not have data about police interventions")
        else:
            print("Department {} has {} file(s) about police interventions".format(dept_num, 
                                                                                   len(crime_files)))
            
        # Check the ACS data consistency -------------------------------------------
        data_path = dept + '/' + dept_num + '_ACS_data/'
        # Check if we have all the topics (poverty, education, etc)
        temp_topics = [d.path for d in scandir(data_path) if d.is_dir()]
        topics = check_topics(dept_num, topics, temp_topics)
        
        # Check if the data have consistent id's and columns
        files = list_all_files(data_path, pattern='_with_ann.csv')
        ids = []  # needed to check if we have all
        for file in files:
            data = pd.read_csv(file, skiprows=[1], low_memory=False, nrows=3)  # nrows is for speed
            meta = file.replace('_with_ann.csv', '_metadata.csv')
            metadata = pd.read_csv(meta, header=None, names=['key', 'description'])
            if not data.columns.all() in list(metadata['key']):
                print("In {} inconsistent metadata".format(file))
            ids = check_ids(ids, data)
        
        # Check the Shapefiles consistency ------------------------------------------
        data_path = dept + '/' + dept_num + '_Shapefiles/'
        extensions = ['.shp', '.shx', '.dbf', '.prj']
        for ext in extensions:
            files = list_all_files(data_path, pattern=ext)
            if len(files) < 1:
                print("Department {} does not have the {} file".format(dept_num, 
                                                                       ext))
            if len(files) > 1:
                print("Department {} has {} files with extension {}".format(dept_num,
                															len(files), 
                                                                            ext))
        print("\n")
    print("Done!")

