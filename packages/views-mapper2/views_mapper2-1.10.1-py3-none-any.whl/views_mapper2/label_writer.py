"""
Small functions enabling ease of writing recursive mapping code
And simplifying the lookup and conversion of month and country ids
"""
import pandas as pd
from ingester3.ViewsMonth import ViewsMonth
from ingester3.Country import Country
import pycountry
from datetime import date
import os
import numpy as np


def vid2date(month_id):
    """
    Writes a label in standard year/month format from month_id
    :param month_id:
    :return: year/month date
    """
    year=str(ViewsMonth(month_id).year)
    month=str(ViewsMonth(month_id).month)
    return year+'/'+month

def vid2date_version2(month_id):
    """
    Writes a label in standard year_month format from month_id
    :param month_id:
    :return: year_month date
    """
    year=str(ViewsMonth(month_id).year)
    month=str(ViewsMonth(month_id).month)
    return year+'_'+month

def date2id(date_string):
    """
    Writes month id from date, iso format
    :param date_string: date in iso format, e.g., '2010-04-01'
    :return: ViEWS month id
    """
    date_iso = date.fromisoformat(date_string)
    month_id = ViewsMonth.from_date(date_iso).id
    return month_id

def cid2name(country_id):
    """
    Function useful for labeling countries if needed by their name
    Create a string output name by country id
    Uses ingester3 Country as basis
    :param country_id: Views Country ID
    :return: name
    """
    name = Country(country_id).name
    return name

def name2iso(country):
    """
    Creates a quick lookup of the ISO label for a country
    Contains soft search suggestion if the input is wrong
    :param name: name, please make sure to input in ''. e.g. 'England'
    :return: ISO code
    """
    try:
        output = pycountry.countries.get(name=country).alpha_3
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

def name_mid2cid(country, month_id):
    """
    Quick lookup of the country id from name and month id
    :param country: Name of country, please enter as a string within '', e.g., 'England'
    :param month_id: ViEWS month ID
    :return: ViEWS country ID
    """
    try:
        output = Country.from_iso(pycountry.countries.get(name=country).alpha_3, month_id).id
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

def name_date2cid(country, date_string):
    """
    Quick looks up of the country id from name and iso date
    :param country: name of the country, enter as string, e.g., 'England'
    :param date_string: date in iso format, enter as string, e.g., '2010-04-01'
    :return: ViEWS country ID
    """
    date_iso = date.fromisoformat(date_string)
    month_id = ViewsMonth.from_date(date_iso).id
    try:
        output = Country.from_iso(pycountry.countries.get(name=country).alpha_3, month_id).id
    except AttributeError:
        try:
            output = 'no match, did you mean'+' ' + str(pycountry.countries.search_fuzzy(country)[0])
        except LookupError:
            output= 'check_spelling'
    return output

def give_me_top10_country_id(df, month_value, var_name, variable_transformation):
    """the dataframe must contain month_id and country_id columns with those names"""
    if variable_transformation == 'actual':
        temp = df.reset_index()
        temp = temp.set_index(['country_id', 'month_id'])
        temp2 = temp.iloc[temp.index.get_level_values('month_id') == month_value]
        temp3 = temp2.nlargest(10, str(var_name)).reset_index()
        output = list(temp3['country_id'])
    elif variable_transformation == 'ln1':
        temp = df.reset_index()
        temp = temp.set_index(['country_id', 'month_id'])
        temp['actual'] = np.exp(temp[var_name]) - 1
        temp2 = temp.iloc[temp.index.get_level_values('month_id') == month_value]
        temp3 = temp2.nlargest(10, str('actual')).reset_index()
        output = list(temp3['country_id'])
    else: output = 'function works for actual or single ln transformed variables only'
    return output


def give_me_topX_country_id_cumulative(df, time_index, number_wanted, variable, start, end, variable_transformation):
    if variable_transformation == 'actual':
        temp = df.reset_index()
        temp = temp.set_index(['country_id', str(time_index)])
        time_wanted = list(range(start, end + 1))
        temp2 = temp[temp.index.get_level_values(str(time_index)).isin(time_wanted)]
        temp3 = pd.DataFrame(temp2.groupby('country_id').agg({str(variable): 'sum'}))
        temp4 = temp3.nlargest(number_wanted, str(variable)).reset_index()
        output = list(temp4['country_id'])
    elif variable_transformation == 'ln1':
        temp = df.reset_index()
        temp = temp.set_index(['country_id', str(time_index)])
        temp['actual'] = np.exp(temp[variable]) - 1
        time_wanted = list(range(start, end + 1))
        temp2 = temp[temp.index.get_level_values(str(time_index)).isin(time_wanted)]
        temp3 = pd.DataFrame(temp2.groupby('country_id').agg({str('actual'): 'sum'}))
        temp4 = temp3.nlargest(number_wanted, str('actual')).reset_index()
        output = list(temp4['country_id'])
    else:
        output = 'function works for actual or single ln transformed variables'
    return output

def give_me_top10_names(df, month_value, var_name, variable_transformation):
    """the dataframe must contain month_id and country_id columns with those names"""
    temp = df.copy()
    temp_list = give_me_top10_country_id(df = temp, month_value = month_value, var_name = var_name, variable_transformation=variable_transformation)

    try:
        list_1 = list()
        for i in temp_list:
            list_1.append(Country(i).name)
        output = list_1
    except: output = temp_list
    return output

def give_me_topX_country_names_cumulative(df, time_index, number_wanted, variable, start, end, variable_transformation):
    temp = df.copy()
    temp_list = give_me_topX_country_id_cumulative(df=temp, time_index = time_index, number_wanted = number_wanted, variable = variable, start = start, end = end, variable_transformation= variable_transformation)

    try:
        list_1 = list()
        for i in temp_list:
            list_1.append(Country(i).name)
        output = list_1
    except: output = temp_list

    return output

def make_a_folder(folderpath):
    if not os.path.exists(folderpath):
        os.mkdir(folderpath)
        print('Directory', folderpath, "created")
    else:
        print('Directory', folderpath, 'already exists')

def make_folders_complete_set(main_folderpath):
    #main folder
    make_a_folder(main_folderpath)
    #Features is the actuals
    make_a_folder(main_folderpath+'/Features')
    make_a_folder(main_folderpath + '/Features'+'/Maps')
    make_a_folder(main_folderpath + '/Features'+'/Maps'+'/cm')
    make_a_folder(main_folderpath + '/Features'+'/Maps'+'/pgm')

    make_a_folder(main_folderpath + '/Features' + '/ChangeMaps')
    make_a_folder(main_folderpath + '/Features' + '/ChangeMaps' + '/cm')
    make_a_folder(main_folderpath + '/Features' + '/ChangeMaps' + '/pgm')

    #Dichotomous subfolders
    make_a_folder(main_folderpath+'/Dichotomous')
    make_a_folder(main_folderpath+'/Dichotomous'+'/Ensemble')

    make_a_folder(main_folderpath+'/Dichotomous'+'/Ensemble'+'/ForecastMaps')
    make_a_folder(main_folderpath + '/Dichotomous' + '/Ensemble' + '/ForecastMaps'+'/cm')
    make_a_folder(main_folderpath + '/Dichotomous' + '/Ensemble' + '/ForecastMaps'+'/pgm')

    make_a_folder(main_folderpath+'/Dichotomous'+'/Ensemble'+'/ChangeMaps')
    make_a_folder(main_folderpath + '/Dichotomous' + '/Ensemble' + '/ChangeMaps'+'/cm')
    make_a_folder(main_folderpath + '/Dichotomous' + '/Ensemble' + '/ChangeMaps'+'/pgm')

    make_a_folder(main_folderpath+'/Dichotomous'+'/Ensemble'+'/LineGraphs')

    #Continous subfolders
    make_a_folder(main_folderpath+'/Continuous')
    #Continous ensemble subfolders
    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble')

    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble'+'/ForecastMaps')
    make_a_folder(main_folderpath + '/Continuous' + '/Ensemble' + '/ForecastMaps'+'/cm')
    make_a_folder(main_folderpath + '/Continuous' + '/Ensemble' + '/ForecastMaps'+'/pgm')

    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble'+'/ChangeMaps')
    make_a_folder(main_folderpath + '/Continuous' + '/Ensemble' + '/ChangeMaps'+'/cm')
    make_a_folder(main_folderpath + '/Continuous' + '/Ensemble' + '/ChangeMaps'+'/pgm')

    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble'+'/LineGraphs')
    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble'+'/PieCharts')
    make_a_folder(main_folderpath+'/Continuous'+'/Ensemble'+'/BarCharts')
    #Continuous interpretation subfolders
    make_a_folder(main_folderpath+'/Continuous'+'/Interpretation')
    make_a_folder(main_folderpath+'/Continuous'+'/Interpretation'+'/Uncertainty')
    make_a_folder(main_folderpath + '/Continuous' + '/Interpretation' + '/Surrogate')



#this looks for the violence type, note requires that a variable has _sb at the end
def find_the_violence_type(string):
    if string.count('_sb')>0: output = 'state-based violence'
    elif string.count('_ns')>0: output = 'non-state violence'
    elif string.count('_os')>0: output = 'one-sided violence'
    else: output = 'please check the variable name'
    return output

def give_me_violence_string_label_only(string):
    if string.count('_sb')>0: output = '_sb'
    elif string.count('_ns')>0: output = '_ns'
    elif string.count('_os'): output = '_os'
    else: output = 'please check the variable name'
    return output
