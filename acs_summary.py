__author__ = "lucabasa"
__version__ = "1.0.0"

"""
Methods to prepare the ACS data for exploration
and to summarize them.

Dictionaries with the variable selection are provided and can be modified

"""

from data_quality import list_all_files

import pandas as pd
import numpy as np


poverty_list = {'HC01_EST_VC01' : 'p_total_est',  # these are just those we know the poverty level of
                'HC01_MOE_VC01' : 'p_total_moe',
                'HC02_EST_VC01' : 'p_below_pov_est',
                'HC02_MOE_VC01' : 'p_below_pov_moe',
                'HC03_EST_VC01' : 'p_below_pov_perc_est',
                'HC03_MOE_VC01' : 'p_below_pov_perc_moe',
                'HC02_EST_VC14' : 'p_males_below_pov_est',
                'HC02_MOE_VC14' : 'p_males_below_pov_moe',
                'HC03_EST_VC14' : 'p_males_below_pov_perc_est',
                'HC03_MOE_VC14' : 'p_males_below_pov_perc_moe',
                'HC02_EST_VC15' : 'p_females_below_pov_est',
                'HC02_MOE_VC15' : 'p_females_below_pov_moe',
                'HC03_EST_VC15' : 'p_females_below_pov_perc_est',
                'HC03_MOE_VC15' : 'p_females_below_pov_perc_moe',
                'HC02_EST_VC18' : 'p_white_below_pov_est',
                'HC02_MOE_VC18' : 'p_white_below_pov_moe',
                'HC03_EST_VC18' : 'p_white_below_pov_perc_est',
                'HC03_MOE_VC18' : 'p_white_below_pov_perc_moe',
                'HC02_EST_VC19' : 'p_black_below_pov_est',
                'HC02_MOE_VC19' : 'p_black_below_pov_moe',
                'HC03_EST_VC19' : 'p_black_below_pov_perc_est',
                'HC03_MOE_VC19' : 'p_black_below_pov_perc_moe',
                'HC02_EST_VC20' : 'p_native_below_pov_est',
                'HC02_MOE_VC20' : 'p_native_below_pov_moe',
                'HC03_EST_VC20' : 'p_native_below_pov_perc_est',
                'HC03_MOE_VC20' : 'p_native_below_pov_perc_moe',
                'HC02_EST_VC21' : 'p_asian_below_pov_est',
                'HC02_MOE_VC21' : 'p_asian_below_pov_moe',
                'HC03_EST_VC21' : 'p_asian_below_pov_perc_est',
                'HC03_MOE_VC21' : 'p_asian_below_pov_perc_moe',
                'HC02_EST_VC22' : 'p_islander_below_pov_est',
                'HC02_MOE_VC22' : 'p_islander_below_pov_moe',
                'HC03_EST_VC22' : 'p_islander_below_pov_perc_est',
                'HC03_MOE_VC22' : 'p_islander_below_pov_perc_moe',
                'HC02_EST_VC23' : 'p_other_race_below_pov_est',
                'HC02_MOE_VC23' : 'p_other_race_below_pov_moe',
                'HC03_EST_VC23' : 'p_other_race_below_pov_perc_est',
                'HC03_MOE_VC23' : 'p_other_race_below_pov_perc_moe',
                'HC02_EST_VC26' : 'p_hispanic_below_pov_est',
                'HC02_MOE_VC26' : 'p_hispanic_below_pov_moe',
                'HC03_EST_VC26' : 'p_hispanic_below_pov_perc_est',
                'HC03_MOE_VC26' : 'p_hispanic_below_pov_perc_moe'
                }


race_list = {'HC01_VC03': 'total_population',
             'HC01_VC04': 'total_males',
             'HC01_VC05': 'total_females',
             'HC01_VC49': 'total_white',
             'HC03_VC49': 'perc_white',
             'HC01_VC50': 'total_black',
             'HC03_VC50': 'perc_black',
             'HC01_VC51': 'total_native',  # sorry for not including the individual tribes
             'HC03_VC51': 'perc_native',
             'HC01_VC56': 'total_asian',
             'HC03_VC56': 'perc_asian', # sorry for not aknowledging that Asia is a huge place
             'HC01_VC64': 'total_islander',
             'HC03_VC64': 'perc_islander',
             'HC01_VC69': 'total_other_race',
             'HC03_VC69': 'perc_other_race',
             'HC01_VC88': 'total_hispanic',
             'HC03_VC88': 'perc_hispanic'
            }


housing_list = {'HC01_EST_VC01': 'h_total_houses_est',
                'HC01_MOE_VC01': 'h_total_houses_moe',
                'HC02_EST_VC01': 'h_owner_houses_est',
                'HC02_MOE_VC01': 'h_owner_houses_moe',
                'HC03_EST_VC01': 'h_rented_houses_est',
                'HC03_MOE_VC01': 'h_rented_houses_moe',
                'HC04_EST_VC04': 'h_total_houses_white_est',
                'HC04_MOE_VC04': 'h_total_houses_white_moe',
                'HC02_EST_VC04': 'h_owner_houses_white_est',
                'HC02_MOE_VC04': 'h_owner_houses_white_moe',
                'HC03_EST_VC04': 'h_rented_houses_white_est',
                'HC03_MOE_VC04': 'h_rented_houses_white_moe',
                'HC05_EST_VC05': 'h_total_houses_black_est',
                'HC05_MOE_VC05': 'h_total_houses_black_moe',
                'HC02_EST_VC05': 'h_owner_houses_black_est',
                'HC02_MOE_VC05': 'h_owner_houses_black_moe',
                'HC03_EST_VC05': 'h_rented_houses_black_est',
                'HC03_MOE_VC05': 'h_rented_houses_black_moe',
                'HC06_EST_VC06': 'h_total_houses_native_est',
                'HC06_MOE_VC06': 'h_total_houses_native_moe',
                'HC02_EST_VC06': 'h_owner_houses_native_est',
                'HC02_MOE_VC06': 'h_owner_houses_native_moe',
                'HC03_EST_VC06': 'h_rented_houses_native_est',
                'HC03_MOE_VC06': 'h_rented_houses_native_moe',
                'HC07_EST_VC07': 'h_total_houses_asian_est',
                'HC07_MOE_VC07': 'h_total_houses_asian_moe',
                'HC02_EST_VC07': 'h_owner_houses_asian_est',
                'HC02_MOE_VC07': 'h_owner_houses_asian_moe',
                'HC03_EST_VC07': 'h_rented_houses_asian_est',
                'HC03_MOE_VC07': 'h_rented_houses_asian_moe',
                'HC08_EST_VC08': 'h_total_houses_islander_est',
                'HC08_MOE_VC08': 'h_total_houses_islander_moe',
                'HC02_EST_VC08': 'h_owner_houses_islander_est',
                'HC02_MOE_VC08': 'h_owner_houses_islander_moe',
                'HC03_EST_VC08': 'h_rented_houses_islander_est',
                'HC03_MOE_VC08': 'h_rented_houses_islander_moe',
                'HC09_EST_VC09': 'h_total_houses_other_race_est',
                'HC09_MOE_VC09': 'h_total_houses_other_race_moe',
                'HC02_EST_VC09': 'h_owner_houses_other_race_est',
                'HC02_MOE_VC09': 'h_owner_houses_other_race_moe',
                'HC03_EST_VC09': 'h_rented_houses_other_race_est',
                'HC03_MOE_VC09': 'h_rented_houses_other_race_moe',
                'HC12_EST_VC12': 'h_total_houses_hispanic_est',
                'HC12_MOE_VC12': 'h_total_houses_hispanic_moe',
                'HC02_EST_VC12': 'h_owner_houses_hispanic_est',
                'HC02_MOE_VC12': 'h_owner_houses_hispanic_moe',
                'HC03_EST_VC12': 'h_rented_houses_hispanic_est',
                'HC03_MOE_VC12': 'h_rented_houses_hispanic_moe'
               }


income_list = {'HC01_EST_VC02': 'i_total_income_est',
               'HC01_MOE_VC02': 'i_total_income_moe',
               'HC02_EST_VC02': 'i_median_income_est',
               'HC02_MOE_VC02': 'i_median_income_moe',
               'HC01_EST_VC04': 'i_total_income_white_est',
               'HC01_MOE_VC04': 'i_total_income_white_moe',
               'HC02_EST_VC04': 'i_median_income_white_est',
               'HC02_MOE_VC04': 'i_median_income_white_moe',
               'HC01_EST_VC05': 'i_total_income_black_est',
               'HC01_MOE_VC05': 'i_total_income_black_moe',
               'HC02_EST_VC05': 'i_median_income_black_est',
               'HC02_MOE_VC05': 'i_median_income_black_moe',
               'HC01_EST_VC06': 'i_total_income_native_est',
               'HC01_MOE_VC06': 'i_total_income_native_moe',
               'HC02_EST_VC06': 'i_median_income_native_est',
               'HC02_MOE_VC06': 'i_median_income_native_moe',
               'HC01_EST_VC07': 'i_total_income_asian_est',
               'HC01_MOE_VC07': 'i_total_income_asian_moe',
               'HC02_EST_VC07': 'i_median_income_asian_est',
               'HC02_MOE_VC07': 'i_median_income_asian_moe',
               'HC01_EST_VC08': 'i_total_income_islander_est',
               'HC01_MOE_VC08': 'i_total_income_islander_moe',
               'HC02_EST_VC08': 'i_median_income_islander_est',
               'HC02_MOE_VC08': 'i_median_income_islander_moe',
               'HC01_EST_VC09': 'i_total_income_other_race_est',
               'HC01_MOE_VC09': 'i_total_income_other_race_moe',
               'HC02_EST_VC09': 'i_median_income_other_race_est',
               'HC02_MOE_VC09': 'i_median_income_other_race_moe',
               'HC01_EST_VC12': 'i_total_income_hispanic_est',
               'HC01_MOE_VC12': 'i_total_income_hispanic_moe',
               'HC02_EST_VC12': 'i_median_income_hispanic_est',
               'HC02_MOE_VC12': 'i_median_income_hispanic_moe'
              }


employment_list = {'HC04_EST_VC01': 'e_unempl_rate_est',
                   'HC04_MOE_VC01': 'e_unempl_rate_moe',
                   'HC04_EST_VC15': 'e_unempl_rate_white_est',
                   'HC04_MOE_VC15': 'e_unempl_rate_white_moe',
                   'HC04_EST_VC16': 'e_unempl_rate_black_est',
                   'HC04_MOE_VC16': 'e_unempl_rate_black_moe',
                   'HC04_EST_VC17': 'e_unempl_rate_native_est',
                   'HC04_MOE_VC17': 'e_unempl_rate_native_moe',
                   'HC04_EST_VC18': 'e_unempl_rate_asian_est',
                   'HC04_MOE_VC18': 'e_unempl_rate_asian_moe',
                   'HC04_EST_VC19': 'e_unempl_rate_islander_est',
                   'HC04_MOE_VC19': 'e_unempl_rate_islander_moe',
                   'HC04_EST_VC20': 'e_unempl_rate_other_race_est',
                   'HC04_MOE_VC20': 'e_unempl_rate_other_race_moe',
                   'HC04_EST_VC23': 'e_unempl_rate_hispanic_est',
                   'HC04_MOE_VC23': 'e_unempl_rate_hispanic_moe',
                   'HC04_EST_VC28': 'e_unempl_rate_males_est',
                   'HC04_MOE_VC28': 'e_unempl_rate_males_moe',
                   'HC04_EST_VC29': 'e_unempl_rate_females_est',
                   'HC04_MOE_VC29': 'e_unempl_rate_females_moe'
                  }


education_list = {'HC02_EST_VC42': 'ed_perc_hs_white_est',
                  'HC04_EST_VC42': 'ed_perc_hs_white_male_est',
                  'HC06_EST_VC42': 'ed_perc_hs_white_female_est',
                  'HC02_EST_VC43': 'ed_perc_ba_white_est',
                  'HC04_EST_VC43': 'ed_perc_ba_white_male_est',
                  'HC06_EST_VC43': 'ed_perc_ba_white_female_est',
                  'HC02_EST_VC46': 'ed_perc_hs_black_est',
                  'HC04_EST_VC46': 'ed_perc_hs_black_male_est',
                  'HC06_EST_VC46': 'ed_perc_hs_black_female_est',
                  'HC02_EST_VC47': 'ed_perc_ba_black_est',
                  'HC04_EST_VC47': 'ed_perc_ba_black_male_est',
                  'HC06_EST_VC47': 'ed_perc_ba_black_female_est',
                  'HC02_EST_VC50': 'ed_perc_hs_native_est',
                  'HC04_EST_VC50': 'ed_perc_hs_native_male_est',
                  'HC06_EST_VC50': 'ed_perc_hs_native_female_est',
                  'HC02_EST_VC51': 'ed_perc_ba_native_est',
                  'HC04_EST_VC51': 'ed_perc_ba_native_male_est',
                  'HC06_EST_VC51': 'ed_perc_ba_native_female_est',
                  'HC02_EST_VC54': 'ed_perc_hs_asian_est',
                  'HC04_EST_VC54': 'ed_perc_hs_asian_male_est',
                  'HC06_EST_VC54': 'ed_perc_hs_asian_female_est',
                  'HC02_EST_VC55': 'ed_perc_ba_asian_est',
                  'HC04_EST_VC55': 'ed_perc_ba_asian_male_est',
                  'HC06_EST_VC55': 'ed_perc_ba_asian_female_est',
                  'HC02_EST_VC58': 'ed_perc_hs_islander_est',
                  'HC04_EST_VC58': 'ed_perc_hs_islander_male_est',
                  'HC06_EST_VC58': 'ed_perc_hs_islander_female_est',
                  'HC02_EST_VC59': 'ed_perc_ba_islander_est',
                  'HC04_EST_VC59': 'ed_perc_ba_islander_male_est',
                  'HC06_EST_VC59': 'ed_perc_ba_islander_female_est',
                  'HC02_EST_VC62': 'ed_perc_hs_other_race_est',
                  'HC04_EST_VC62': 'ed_perc_hs_other_race_male_est',
                  'HC06_EST_VC62': 'ed_perc_hs_other_race_female_est',
                  'HC02_EST_VC63': 'ed_perc_ba_other_race_est',
                  'HC04_EST_VC63': 'ed_perc_ba_other_race_male_est',
                  'HC06_EST_VC63': 'ed_perc_ba_other_race_female_est',
                  'HC02_EST_VC70': 'ed_perc_hs_hispanic_est',
                  'HC04_EST_VC70': 'ed_perc_hs_hispanic_male_est',
                  'HC06_EST_VC70': 'ed_perc_hs_hispanic_female_est',
                  'HC02_EST_VC71': 'ed_perc_ba_hispanic_est',
                  'HC04_EST_VC71': 'ed_perc_ba_hispanic_male_est',
                  'HC06_EST_VC71': 'ed_perc_ba_hispanic_female_est'
                 }
                 
                 
                 
def _add_ACS_column(data, column, output):
    try:
        to_add = data[['GEO.id', 'GEO.id2', 'GEO.display-label', column]].copy()
        output = pd.merge(output, to_add, on=['GEO.id', 'GEO.id2', 'GEO.display-label'])
    except KeyError:
        pass
    return output


def _add_ACS_topic(data, output, col_list):
    data = data.rename(columns=col_list)
    col_list = list(col_list.values())
    for col in col_list:
        output = _add_ACS_column(data, col, output)
    return output


def prepare_ACS(dept):
    """
    This function merges together the chosen columns for all the topics in the census data
    """
    topics = [topic for topic in list(dept.keys()) if '_meta' not in topic 
              and 'police' not in topic and 'shapefile' not in topic 
              and 'education-attainment-over-25' not in topic]  # it is redundant
    
    switcher = {  # this is because python is cool by I still miss a switch statement
        'poverty': poverty_list,
        'poverty-status': poverty_list,
        'owner-occupied-housing': housing_list,
        'race-sex-age': race_list,
        'race-age-sex': race_list,
        'income': income_list,
        'education-attainment': education_list,
        'employment': employment_list
        }
    
    output = dept['education-attainment'][['GEO.id', 'GEO.id2', 'GEO.display-label']].copy()
    size = 0
    
    for topic in topics:
        col_list = switcher.get(topic)
        size += len(col_list.keys())
        output = _add_ACS_topic(dept[topic], output, col_list)
        
    print(f"Expected size of the output: {size} columns")
    print(f"Available data: {output.shape}")
    return output


def _wavg(data, column, weight):
    return np.average(data[column], weights=data[weight])


def _print_stats(data, col_list, total='total_population'):
    try:
        tmp = data[[total] + col_list].fillna(0)
        for col in col_list:
            print('{}: {}'.format(col, round(_wavg(tmp, col, total),3)))
    except KeyError:
        print('Total population unavailable, the means are not weighted')
        tmp = data[col_list].fillna(0)
        for col in col_list:
            print('{}:{}'.format(col, round(tmp[col].mean(),3)))

            
def _print_perc(data, col_list):
    for col in col_list:
        min_perc = data[col].min()
        med_perc = data[col].median()
        max_perc = data[col].max()
        print(col)
        print(f'\t Min: {min_perc}')
        print(f'\t Median: {med_perc}')
        print(f'\t Max: {max_perc}')


def overview_ACS(data):
    tot_pop = data[[col for col in data.columns if col.startswith('total_')]].sum()
    tot_pop = round(tot_pop / tot_pop[0] * 100, 2)
    print(tot_pop)
    print("_"*40)

    race_perc = [col for col in data.columns if col.startswith('perc_')]
    _print_perc(data, race_perc)


def unemployment_ACS(data):
    unemp_cols = [col for col in data.columns if 'e_unemp' in col and '_est' in col]
    _print_stats(data, unemp_cols)
            

def poverty_ACS(data):
    pov_cols = [col for col in data.columns if 'below_pov_perc_est' in col]
    _print_stats(data, pov_cols)
    print("_"*40)
    _print_perc(data, pov_cols)


def income_ACS(data):
    inc_cols = [col for col in data.columns if 'median_income' in col and '_est' in col]
    mean_inc = round(data[inc_cols].mean(),1)
    max_inc = round(data[inc_cols].max(), 1)
    min_inc = round(data[inc_cols].min(), 1)
    print('Mean of medians: ' + '-'*10)
    print(mean_inc)
    print('Max of medians: ' + '-'*10)
    print(max_inc)
    print('Min of medians: ' + '-'*10)
    print(min_inc)
    
    
def education_ACS(data):
    ed_cols = [col for col in data.columns if 'ed_perc_' in col and
               'male' not in col and 'female' not in col]
    _print_perc(data, ed_cols)
        

def summarize_ACS(data):
	"""
	Wrapper of the functions above
	"""
    print("Population overview (estimated totals)")
    overview_ACS(data)
    print('\n')
    
    print("Unemployment rate (weighted averages)")
    unemployment_ACS(data)
    print('\n')
    
    print('Below poverty level (weighted averages)')
    poverty_ACS(data)
    print('\n')
    
    print('Median income (means and ranges)')
    income_ACS(data)
    print('\n')
    
    print('Education (estimated percentages)')
    education_ACS(data)
    print('\n')


def acs_by_district(data):
	"""
	The input has to contain a district column and a fraction column.
	Fraction says what percentage of the area of a given GEO.id2 belongs to a district
	
	"""
    data = data[[col for col in data.columns if 'GEO' not in col 
                 and 'geometry' not in col]].copy()
    
    # applying the fraction to the merged dataframe
    fraction = data['fraction']
    del data['fraction']
    cols = [col for col in data.columns if 'district' not in col]
    data[cols] = data[cols].multiply(fraction, axis="index")
    
    sel = ['district'] + [col for col in data.columns if '_est' in col 
                          or col.startswith('total_')]
    
    # grouping the totals
    tot_cols = [col for col in sel if 'perc' not in col
               and 'rate' not in col and 'median' not in col]
    totals = data[tot_cols].groupby('district', as_index=False).sum()
    
    # grouping the proportions
    try:
        prp = [col for col in sel if 'perc' in col
                                   or 'rate' in col]
        prop_cols = ['district'] + prp
        props = data[prop_cols].copy()
        # make them proportions
        props[prp] = props[prp].multiply(0.01, axis='index')
        # groupby with weighted average
        wm = lambda x: np.average(x, weights=data.loc[x.index, "total_population"])
        props = props.groupby('district', as_index=False).agg(wm)    
    except KeyError:
        print("Total population unavailable, percentages and rates can't be summarized")
        
    # mergin together
    summary = pd.merge(totals, props, on='district')
    
    return summary

