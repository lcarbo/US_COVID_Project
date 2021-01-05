 # CDC_COVID_API = https://data.cdc.gov/resource/vbim-akqf.json 

#Import Dependencies 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from census import Census

state_abb = "Resources/state-abbrevs.csv"
state_area = "Resources/state-areas.csv"

state_abb_read = pd.read_csv(state_abb)
state_abb_df = pd.DataFrame(state_abb_read)
state_area_read = pd.read_csv(state_area)
state_area_df = pd.DataFrame(state_area_read)
state_info_df = pd.merge(state_abb_df, state_area_df)
print(state_info_df)

covid_file= "Resources/all-states-history-1219.csv"
covid_data=pd.read_csv(covid_file)
covid_df = pd.DataFrame(covid_data) 
covid_df.rename(columns = {"state" : "abbreviation"}, inplace = True)
print(covid_df)

covid_state = pd.merge(state_info_df, covid_df, on = "abbreviation")

# covid_state.to_csv("COVID_State.csv", index = False)

covid_state.dropna()
covid_state = covid_state[["state", "abbreviation", "area (sq. mi)", "date", "dataQualityGrade", "death", "hospitalized", "positive", "negative", "recovered", "totalTestResults"]]
# print(covid_state.head())
# for state in covid_state["state"]:
    
# Median income by state and population 
census_key = 'e3bdb742454fec392bd8e25113654b613eae40f0'
c = Census(census_key, year = 2019)

census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
                          "B19301_001E",
                          "B17001_002E",
                          "B23025_005E"), {'for': 'state:*'})

# Convert to DataFrame
census_pd = pd.DataFrame(census_data)

# Column Reordering
census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "B01002_001E": "Median Age",
                                      "B19013_001E": "Median Household Income",
                                      "B19301_001E": "Per Capita Income",
                                      "B17001_002E": "Poverty Count",
                                      "B23025_005E": "Unemployment Count",
                                      "NAME": "Name", "state": "State"})
print(census_pd)
#Get a general latitude and longitude for each state




# nj_df = covid_state.loc[covid_state["abbreviation"] == "NJ"]
# print(nj_df)

#using dataframe of State Abbrevs and State Areas 
#review and clean the covid data 
#remove outliers, rename columns
#gather general COVID data by states - number of cases by state 


#overlay onto a map in a heatmap in gmaps / use markers per state showing total cases 
#gather stats about Census data
#show population per state as marker 
#compare # of cases v population density 
#combine data about each state and COVID infections grouped by age 
#include % of population, % of COVID infections 
#create a summary table of US overall 