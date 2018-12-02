__author__ = "lucabasa"
__version__ = "1.0.0"

"""
Methods to get an overview of the police data

Other kinds of aggregations are possible

"""

from data_quality import list_all_files

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt



def _drop_columns(feats, additional=None):
    """
    This function takes a list of features and removes DETAILS and ID.
    The user can provide an additional list to remove more features
    """
    to_drop = ['DETAILS', 'ID']
    if additional:
        to_drop = to_drop + additional
    feats = [feat for feat in feats if feat not in to_drop]
    return feats       


def _get_columns(data):
    """
    This helper finds the columns regarding subjects and officers.
    The prefix SUBJECT_ and OFFICER_ are removed.
    It returns a list of columns regarding subjects, one regarding officers
    and one with their intersection
    """
    subj = [col.replace('SUBJECT_', '') for col in data.columns if 'SUBJECT' in col]
    off = [col.replace('OFFICER_', '') for col in data.columns if 'OFFICER' in col]
    conf = list(set(subj).intersection(off))
    conf = _drop_columns(conf)
    return subj, off, conf


def subj_v_off(data, conf):
    """
    This function takes the data and a list of columns describing both subjects and columns
    Accordingly to the nature of the columns, it produces side by side plots and prints some 
    descriptive statistics (count, crosstabs)
    """
    num = len(conf)
    # 2 plots side by side for each category
    fig, ax = plt.subplots(num,2, figsize=(15,5*num))
    i = 0
    for feat in conf:
        off = 'OFFICER_' + feat
        subj = 'SUBJECT_' + feat
        print(feat)
        if feat in ['GENDER', 'RACE', 'HOSPITALIZATION', 'INJURY', 'INJURY_TYPE']:
            print('Officers: ' + '-'*40)
            print(data[off].value_counts(dropna=False, normalize=True).head(10))
            
            print("Subjects: " + '-'*40)
            print(data[subj].value_counts(dropna=False, normalize=True).head(10))
            
            if (len(data[subj].unique()) > 10 or len(data[off].unique()) > 5):
                print("Too many unique values, crosstab not printed")
            else:
                print("Crosstab: " + '-'*40)
                print(pd.crosstab(data[subj], data[off], 
                                  dropna=False, margins=True))
                print(pd.crosstab(data[subj], data[off], 
                                  dropna=False, normalize=True, margins=True))
            print("_"*40)
            print("\n")
            if num == 1: # dirty escape for poor usage of subplots
                sns.countplot(x=off, data=data, ax=ax[0], 
                              order=data[off].value_counts().iloc[:5].index) # plot only top 5 
                sns.countplot(x=subj, data=data, ax=ax[1], 
                              order=data[subj].value_counts().iloc[:5].index)
            else:
                sns.countplot(x=off, data=data, ax=ax[i][0], 
                              order=data[off].value_counts().iloc[:5].index)
                sns.countplot(x=subj, data=data, ax=ax[i][1], 
                              order=data[subj].value_counts().iloc[:5].index)
                i = i + 1
                
        elif feat in ['AGE']:
            print('Officers: ' + '-'*40)
            print(f"\t- mean: {data[off].mean()}")
            print(f"\t- median: {data[off].median()}")
            print(f"\t- range: {data[off].min()}--{data[off].max()}")
            print(f"\t- std: {data[off].std()}")
            
            print('Subjects: ' + '-'*40)
            print(f"\t- mean: {data[subj].mean()}")
            print(f"\t- median: {data[subj].median()}")
            print(f"\t- range: {data[subj].min()}--{data[subj].max()}")
            print(f"\t- std: {data[subj].std()}")
            print("_"*40)
            print("\n")
            if num == 1:
                sns.distplot(data[off].dropna(), bins = 30, ax=ax[0])
                sns.distplot(data[subj].dropna(), bins = 30, ax=ax[1])
            else:
                sns.distplot(data[off].dropna(), bins = 30, ax=ax[i][0])
                sns.distplot(data[subj].dropna(), bins = 30, ax=ax[i][1])
                i = i + 1


def _cross_cat_cont(data, cont, cat, title=None):
    """
    This function plots a histogram of a continuous variable by segmenting it
    according to a categorical variable
    """
    g = sns.FacetGrid(data, hue=cat, height= 5)
    g.map(plt.hist, cont, alpha= 0.3, bins=30)
    g.add_legend()
    if title:
        plt.title(title)
        

def _experience_segm(data, segment, col=None):
    """
    This function plots the officers year on force, segmented by 2 categories (if provided)
    """
    g = sns.FacetGrid(data, col=col, hue=segment, height= 5)
    g.map(plt.hist, 'OFFICER_YEARS_ON_FORCE', alpha= 0.3, bins=30)
    g.add_legend()
    

def individuals(data, feats, role='SUBJECT'):
    """
    Prints and plots a summary of the features regarding subjects and officers
    The output depends on what is available
    """
    condition = all(x in feats for x in ['AGE', 'RACE'])
    if condition:
        _cross_cat_cont(data, role + '_AGE', role + '_RACE')
    
    condition = all(x in feats for x in ['AGE', 'GENDER'])
    if condition:
        _cross_cat_cont(data, role + '_AGE', role + '_GENDER')
    
    condition = all(x in feats for x in ['RACE', 'WAS_ARRESTED'])
    if condition:
        print(pd.crosstab(data[role + '_RACE'], data[role + '_WAS_ARRESTED'], 
                                  dropna=False, normalize='index', margins=True))
        print("_"*40)
        print('\n')
        
    condition = all(x in feats for x in ['RACE', 'INJURY'])
    if condition:
        print(pd.crosstab(data[role + '_RACE'], data[role + '_INJURY'], 
                                  dropna=False, normalize='index', margins=True))
        print("_"*40)
        print('\n')
        
    condition = all(x in feats for x in ['RACE', 'HOSPITALIZATION'])
    if condition:
        print(pd.crosstab(data[role + '_RACE'], data[role + '_HOSPITALIZATION'], 
                                  dropna=False, normalize='index', margins=True))
        print("_"*40)
        print('\n')
        
    condition = all(x in feats for x in ['YEARS_ON_FORCE', 'INJURY'])
    if condition:
        _cross_cat_cont(data, role + '_YEARS_ON_FORCE', role + '_INJURY')
    
    condition = all(x in feats for x in ['YEARS_ON_FORCE'])
    if condition:
        try:
            _experience_segm(data, 'SUBJECT_RACE', col='SUBJECT_INJURY')
        except KeyError:
            _cross_cat_cont(data, role + '_YEARS_ON_FORCE', 'SUBJECT_RACE')
        try:
            _experience_segm(data, 'SUBJECT_GENDER', col='SUBJECT_INJURY')
        except KeyError:
            _cross_cat_cont(data, role + '_YEARS_ON_FORCE', 'SUBJECT_GENDER')
        
            
def explore_police(data):
    """
    Wrapper for the functions above, calls the appropriate function given 
    what is available
    """
    subj, off, conf = _get_columns(data)
    if len(subj) > 0:
        try:
            individuals(data, subj, 'SUBJECT')
        except Exception as e:
            print("Something went wrong in exploring the subjects")
            print(e)
            pass
    if len(off) > 0:
        try:
            individuals(data, off, 'OFFICER')
        except Exception as e:
            print("Something went wrong in exploring the officers")
            print(e)
            pass
    if len(conf) > 0:
        try:
            subj_v_off(data, conf)
        except Exception as e:
            print("Something went wrong in comparing subjects and officers")
            print(e)
            pass
    print(f"Subject related variables found: {subj}")
    print(f"Officer related variables found: {off}")
    
    
col_list = ['SUBJECT_RACE', 'SUBJECT_GENDER', 'SUBJECT_INJURY', 'OFFICER_INJURY', 
            'SUBJECT_WAS_ARRESTED', 'SUBJECT_HOSPITALIZATION']


def _summary_cleanup(data, distr_col):
    """
    Keep only the columns selected above (plus the district)
    """
    feats = [distr_col] + [col for col in data.columns if col in col_list]
    return data[feats]


def police_by_distr(data, distr_col):
    """
    The police data are reduced to the one selected above
    and summarized according to the distr_col column.
    
    Returns a datafram with the aggregated data.
    """
    data = _summary_cleanup(data, distr_col)
    
    try:
        tot_df = data[[distr_col, data.columns[-1]]].groupby(distr_col, as_index=False).count()
        tot_df.columns = [distr_col, 'total_records']
    except ValueError:
        print("Insufficient data to aggregate")
        return data.head()
    sum_cols = [col for col in data.columns if
                ('RACE' not in col) and ('GENDER' not in col)]
    sum_df = data[sum_cols].groupby(distr_col, as_index=False).agg('sum')
    summary = pd.merge(tot_df, sum_df)
    
    if 'SUBJECT_RACE' in data.columns:
        race = data.groupby([distr_col, 'SUBJECT_RACE']).size().unstack().reset_index().fillna(0)
        summary = pd.merge(summary, race, on=distr_col)
        
    if 'SUBJECT_GENDER' in data.columns:
        gender = data.groupby([distr_col, 'SUBJECT_GENDER']).size().unstack().reset_index().fillna(0)
        summary = pd.merge(summary, gender, on=distr_col)
    
    return summary 
    

