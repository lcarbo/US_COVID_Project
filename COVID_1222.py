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



covid_file= "Resources/all-states-history-1219.csv"
covid_data=pd.read_csv(covid_file)
covid_df = pd.DataFrame(covid_data) 
covid_df.rename(columns = {"state" : "abbreviation"}, inplace = True)
covid_df.head()



#convert date column to date format
covid_df['date'] = pd.to_datetime(covid_df['date'])
covid_df


#merge the data files 
covid_state = pd.merge(state_info_df, covid_df, on = "abbreviation")
covid_state



# covid_state.to_csv("COVID_State.csv", index = False)

covid_state = covid_state[["state", "abbreviation", "area (sq. mi)", "date", "dataQualityGrade", "death", "hospitalized", "positive", "negative", "recovered", "totalTestResults"]]
covid_state


#identify most recent date in the dataframe
covid_state = covid_state.sort_values("date", ascending=False)
covid_state


#isolate the data from the most recent report
old_covid = covid_state[(covid_state['date'] != (covid_state['date'].max()))].index
old_covid

#create a dataframe of only the most recent data
recent_df =covid_state.drop(old_covid, inplace=False)
recent_df

#add columns for additional details we need 
recent_df["Population Density"]="" 

#pull census populations from API 
census_key = 'e3bdb742454fec392bd8e25113654b613eae40f0'
c = Census(census_key, year = 2019)

census_data = c.acs5.get(("NAME", "B19013_001E", "B01003_001E", "B01002_001E",
                          "B19301_001E"), {'for': 'state:*'})

# Convert to DataFrame
census_pd = pd.DataFrame(census_data)

# Column Reordering
census_pd = census_pd.rename(columns={"B01003_001E": "Population",
                                      "B01002_001E": "Median Age",
                                      "B19013_001E": "Median Household Income",
                                      "B19301_001E": "Per Capita Income",
                                      "NAME": "Name", "state": "State"})

merge_df = pd.merge(recent_df, census_pd, left_on='state', right_on='Name', how='inner')
date = merge_df["date"][0]

final_df = merge_df.drop(columns=['state','dataQualityGrade','date',"State"])
# Adding lat and lng
gkey = "xxx"
lat = []
lng = []
target_state = []
for state in final_df["Name"]:
    target_state.append(state)
for state in target_state:
    target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
    'address={0}&key={1}').format(state, gkey)
    target_data = requests.get(target_url).json()
    lat_data = target_data["results"][0]["geometry"]["location"]["lat"]
    lng_data = target_data["results"][0]["geometry"]["location"]["lng"]
    lat.append(lat_data)
    lng.append(lng_data)
final_df["Latitude"] = lat
final_df["Longitude"] = lng

final_df = final_df.set_index('Name')

print(f'This data was collected on: {date}')


final_df.columns = map(str.title,final_df.columns)

final_df = final_df.rename(columns={"Totaltestresults":"Total Test Results"})

final_df["Population Density"] = final_df["Population"] / final_df["Area (Sq. Mi)"]
print(final_df)






# covid_state.to_csv("COVID_State.csv", index = False)



#overlay onto a map in a heatmap in gmaps / use markers per state showing total cases 
#gather stats about Census data
#show population per state as marker 
#compare # of cases v population density 
#combine data about each state and COVID infections grouped by age 
#include % of population, % of COVID infections 
#create a summary table of US overall 

# #creating a heatmap figure
# #DANS CODE HERE


# # Using the template add the location marks to the heatmap
# info_box_template = """
# <dl>
# <dt>State Name</dt><dd>{State Name}</dd>
# <dt>Median Income</dt><dd>{Median Income}</dd>
# <dt>Population Density</dt><dd>{Population Density}</dd>
# <dt>Total Cases</dt><dd>{Total Cases}</dd>
# </dl>
# """
# # Store the DataFrame Row
# corona_info = [info_box_template.format(**row) for index, row in census_pd.iterrows()]
# #set the locations to use for the marker layer
# locations = census_pd[["Latitude", "Longitude"]]
# #make the marker layer
# markers = gmaps.marker_layer(locations)
# #make the info box layer
# corona_markers = gmaps.symbol_layer(locations, info_box_content=corona_info)
# #add both of the layers to the heat map
# fig.add_layer(markers)
# fig.add_layer(corona_markers)
# #print out the map
# fig