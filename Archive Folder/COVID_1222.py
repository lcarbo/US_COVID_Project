#Import Dependencies 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from census import Census
from scipy import stats as st
import gmaps



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

final_df["Population Density"] = round((final_df["Population"] / final_df["Area (Sq. Mi)"]),2)

#Rearranging and organizing the table
final_df = final_df[["Abbreviation","Longitude", "Latitude", "Area (Sq. Mi)", "Population", "Population Density", "Median Age", "Median Household Income","Positive", "Negative", "Recovered", "Death", "Total Test Results"]]

#Formatting median household income
final_df["Median Household Income"] = final_df["Median Household Income"].map("${:,.2f}".format)

# #Renaming the columns
# final_df = final_df.rename(columns={ "Population Density" : "Pop. Density (people/sq mile)", "Positive" : "# COVID Poistive", "Negative" : "# COVID Negative",  "Recovered" : "# Recovered", "Hospitalized" : "# Hospitalized", "Deaths" : "# COVID Deaths"})

#Display
final_df

# Remove outlier (DC)
final_df_outlier = final_df.drop(["District of Columbia"])
final_df_outlier

# Create a pie chart showing total number of positive cases by state
final_df_outlier["Positive"].plot(kind="pie", figsize=(15,15), rotatelabels=True)
plt.ylabel("")
plt.show()

# Find and print the correlation of Population Density to COVID Cases
correlation = st.pearsonr(final_df_outlier["Population Density"],final_df_outlier["Positive"])
print(f"The correlation between both factors is {round(correlation[0],2)}")

# Show the linear regression model for the scatter plot data
x_values = final_df_outlier["Population Density"]
y_values = final_df_outlier["Positive"]
(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x_values, y_values)
regress_values = x_values * slope + intercept
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.ylabel("COVID+ Cases")
plt.xlabel("Population Density (by State)")
plt.title("Correlation of Population Density to Incidence of COVID Cases")
plt.show()

# Find and print the correlation for Median Household Income to COVID Cases
correlation = st.pearsonr(final_df_outlier["Median Household Income"],final_df_outlier["Positive"])
print(f"The correlation between both factors is {round(correlation[0],2)}")

# Show the linear regression model for the scatter plot data
x_values = final_df_outlier["Median Household Income"]
y_values = final_df_outlier["Positive"]
(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x_values, y_values)
regress_values = x_values * slope + intercept
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.ylabel("COVID+ Cases")
plt.xlabel("Median Household Income (by State in USD)")
plt.title("Correlation of Median Household Income to Incidence of COVID Cases")
plt.show()

# Find and print the correlation for Median Age to COVID Cases
correlation = st.pearsonr(final_df_outlier["Median Age"],final_df_outlier["Positive"])
print(f"The correlation between both factors is {round(correlation[0],2)}")

# Show the linear regression model for the scatter plot data
x_values = final_df_outlier["Median Age"]
y_values = final_df_outlier["Positive"]
(slope, intercept, rvalue, pvalue, stderr) = st.linregress(x_values, y_values)
regress_values = x_values * slope + intercept
plt.scatter(x_values,y_values)
plt.plot(x_values,regress_values,"r-")
plt.ylabel("COVID+ Cases")
plt.xlabel("Median Age (by State in Years)")
plt.title("Correlation of Median Age to Incidence of COVID Cases")
plt.show()

# covid_state.to_csv("COVID_State.csv", index = False)


info_box_template = """
<dl>
<dt>State Name</dt><dd>{Abbreviation}</dd>
<dt>Median Income</dt><dd>{Median Household Income}</dd>
<dt>Population Density</dt><dd>{Population Density}</dd>
<dt>Total Cases</dt><dd>{Total Test Results}</dd>
</dl>
"""
# Store the DataFrame Row
corona_info = [info_box_template.format(**row) for index, row in final_df.iterrows()]
#set the locations to use for the marker layer
locations = final_df[["Latitude", "Longitude"]]
#make the marker layer
markers = gmaps.marker_layer(locations)
#make the info box layer
corona_markers = gmaps.symbol_layer(locations, info_box_content=corona_info)
#add both of the layers to the heat map
fig = gmaps.figure()
fig.add_layer(markers)
fig.add_layer(corona_markers)

#this is used to get the max intensity for the heat map
# for state in final_df:
#     print(final_df["Positive"]/final_df["Population"])
#create the heat Layer
per_capita_infection_rate = final_df["Positive"]/final_df["Population"].astype(float)
heat_layer = gmaps.heatmap_layer(locations, weights=per_capita_infection_rate, 
                                 dissipating=False, max_intensity=.118,
                                 point_radius =3.5)

fig.add_layer(heat_layer)
#print out the map
fig