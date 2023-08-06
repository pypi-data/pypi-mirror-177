
import pandas as pd
from datetime import datetime
import matplotlib as plt
from scipy.stats import ttest_ind
import folium
from folium import plugins
from folium.plugins import HeatMap,HeatMapWithTime


#-------------------------ALISA'S FUNCTIONS-------------------------------#


### VARIABLES PER YEAR SPECIFIED ###
## Avg People Info from df ##

def AvgInjury(Year):
    """Finds the average injury rate per year.
    Year: the year of interest 
    Returns the average injure score for that year"""
    year = df[df['CRASH_YEAR'] == Year]
    avg = year['INJURY_RATING'].mean()
    return avg

def AvgAge(Year):
    """Finds the average age of those involved in crash for the year specified.
    Year: the crash year of interest
    Returns the average age of individuals involved in a crash that year"""
    year = df[df['CRASH_YEAR'] == Year]
    avg = year['AGE'].mean()
    return avg

## All People Info from df ##

def Injury(Year):
    """Finds the injury rates per year.
    Year: the year of interest
    Returns the injury ratings for that year."""
    year = df[df['CRASH_YEAR'] == Year]
    injury = year['INJURY_RATING']
    return injury

def Age(Year):
    """Finds the ages of those involved in crash for year specified.
    Year: the crash year of interest
    Returns the ages of those involved for that year."""
    year = df[df['CRASH_YEAR'] == Year]
    ages = year['AGE']
    return ages


## Avg Car Info from df ##

def AvgCarYear(Year):
    """Finds the average vehicle year of those who were involved in a crash that year
    Year: the year of interest
    Returns the average year of the car involved in crash that year"""
    year = df[df['CRASH_YEAR'] == Year]
    avg = year['VEHICLE_YEAR'].mean()
    return avg

def AvgPostedSpeed(Year):
    """Finds the avg speed posted when crashed for the year specified
    Year: the crash year of interest
    Returns the avg speed posted during crash that year"""
    year = df[df['CRASH_YEAR'] == Year]
    avg = year['POSTED_SPEED_LIMIT'].mean()
    return avg

## All Car Infor from df ##

def CarYear(Year):
    """Finds the car years of those invovled in crash for year specified.
    Year: the crash year of interest
    Returns the car years involved in a crash that year."""
    year = df[df['CRASH_YEAR'] == Year]
    caryears = year['VEHICLE_YEAR']
    return caryears

def PostedSpeed(Year):
    """Finds the posted speeds when crashed for year specified.
    Year: the crash year of interest
    Returns the posted speed limits when crashed that year."""
    year = df[df['CRASH_YEAR'] == Year]
    speedlimit = year['POSTED_SPEED_LIMIT']
    return speedlimit

def CarMake(Year):
    """Finds the car makes of those invovled in crash that year.
    Year: the crash year of interest
    Returns the car makes involved in accident that year."""
    year = df[df['CRASH_YEAR'] == Year]
    carmake = year['MAKE']
    return carmake


### AVG PHONE DATA PER YEAR ##

def AgePhone(Year, Phone):
    """Finds the average age of person involved in accident
    Year: the crash year of interest
    Phone: whether individual on phone or not ('Y' or 'N')
    Returns the average age of person involved in accident per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    avg = phone['AGE'].mean() 
    return avg

def CarYearPhone(Year, Phone):
    """Finds the average car year involved in accident
    Year: the crash year of interest
    Phone: whether individual was on phone or not ('Y' or 'N')
    Returns the average car year involved in accident per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    avg = phone['VEHICLE_YEAR'].mean()
    return avg

def InjuryPhone(Year, Phone):
    """Finds the average injury rate for phone usage per year
    Year: the crash year of interest
    Phone: whether individual was on phone or not ('Y' or 'N')
    Returns average injury rate for that year per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    avg = phone['INJURY_RATING'].mean()
    return avg

### PHONE DATA PER YEAR ##

def AgePhoneAll(Year, Phone):
    """Finds the ages of all persons involved in accident
    Year: the crash year of interest
    Phone: whether individual on phone or not ('Y' or 'N')
    Returns the ages of persons involved in accident per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    ages = phone['AGE'] 
    return ages

def CarYearPhoneAll(Year, Phone):
    """Finds the car years involved in accident
    Year: the crash year of interest
    Phone: whether individual was on phone or not ('Y' or 'N')
    Returns the car years involved in accident per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    caryear = phone['VEHICLE_YEAR']
    return caryear

def InjuryPhoneAll(Year, Phone):
    """Finds the injury rates for phone usage per year
    Year: the crash year of interest
    Phone: whether individual was on phone or not ('Y' or 'N')
    Returns injury rates for that year per year and phone use indicated"""
    year = df2[df2['CRASH_YEAR'] == Year]
    phone = year[year['CELL_PHONE_USE'] == Phone]
    injury = phone['INJURY_RATING']
    return injury

# bar plot
def plot_bar(x, y, x_label='x', y_label='y', title=None, figsize=(8,3)):
    fh = plt.figure(figsize=figsize)
    plt.bar(x,y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)

    return fh

# histogram
def plot_hist100(x, density=True, bins=100):
    fh = plt.hist(x, density=True, bins=100)
    plt.ylabel('Probability')
    var = input("Variable: ")
    plt.xlabel(var)
    
    return fh

def plot_hist10(x, density=True, bins=10):
    fh = plt.hist(x,density=True, bins=10)
    plt.ylabel('Probability')
    var = input("Variable: ")
    plt.xlabel(var)
    
    return fh

# scatterplot
def plot_scatter(x,y):
    plt.scatter(x,y)
    plt.show()

# multiline plot - Not working
#need to define variables (var1,var2,var3) prior, then create dataframe
##resultsplot = DataFrame({'name': var1, 'name2': var2, 'name3': var3})
def plot_lines(var1, var2, var3):
    resultsplot.plot()
    plt.legend(loc='lower right')
    plt.xlabel('participants')
    plt.ylabel(var1)
    plt.show()


#--------------------------JADYN'S FUNCTIONS-----------------------------#

def load_crash_data(crash_path):
    """
    :param crash_path: full path of file
    :return: dataframe
    """
    crash_loaded = pd.read_csv(crash_path)
    print(f'Loaded {crash_path}')
    return crash_loaded

def load_people_data(people_path):
    """
    :param people_path: full path of file
    :return: dataframe
    """
    people_loaded = pd.read_csv(people_path)
    print(f'Loaded {people_path}')
    return people_loaded

def load_vehicles_data(vehicles_path):
    """
    :param vehicles_path: full path of file
    :return: dataframe
    """
    vehicles_loaded = pd.read_csv(vehicles_path)
    print(f'Loaded {vehicles_path}')
    return vehicles_loaded

def load_master_data(data_path):
    """
    :param data_path: full path to merged data
    :return: dataframe
    """
    data_loaded = pd.read_csv(data_path)
    print(f'Loaded {data_path}')
    return data_loaded

def extract_year(df_unit):
    crash_date = pd.to_datetime(df_unit['CRASH_DATE'], format = '%m/%d/%Y %I:%M:%S %p')
    crash_year = crash_date.dt.year
    return crash_year

def merge_dataset(crash_small, people_small, vehicles_small):
    """

    :param crash_small: cleaned crash data
    :param people_small: cleaned people data
    :param vehicles_small: cleaned vehicles data
    :return: merged dataframe that contains columns from all three datasets
    """
    df1 = pd.merge(crash_small, people_small, on = 'CRASH_RECORD_ID', how = 'inner')
    merged_df = pd.merge(df1, vehicles_small, on = 'CRASH_RECORD_ID', how = 'inner')
    return merged_df


    #--------------------------YUETONG'S FUNCIONS-------------------------------------#

def ttest_by_variable(df,group_var,l1,l2,var):
    group1 = df[df[group_var]==l1].dropna()
    group2 = df[df[group_var]==l2].dropna()
    print(f"Average of {var} for {group_var} = {l1}:")
    print(group1[var].mean())
    print(f"Average of {var} in {group_var} = {l2}:")
    print(group2[var].mean())
    return ttest_ind(group1[var], group2[var])
def geoplot_accidents(df, year_range=(2021,2022), injury_range=(2,3),r=15):
    Map = folium.Map(location=[41.878876, -87.635918],
                     zoom_start = 12,
                     control_scale=True)
    heat_df = df[(df['CRASH_YEAR']>=year_range[0]) & (df['CRASH_YEAR']<=year_range[1])]
    heat_df = heat_df[(heat_df['INJURY_RATING']>=injury_range[0]) & (heat_df['INJURY_RATING']<=injury_range[1])]
    heat_df = heat_df.dropna(axis=0, subset=['LATITUDE','LONGITUDE'])
    heat_data = zip(heat_df['LATITUDE'],heat_df['LONGITUDE'])
    HeatMap(heat_data,radius=r).add_to(Map)
    return Map