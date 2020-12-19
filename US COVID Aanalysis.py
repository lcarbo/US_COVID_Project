#!/usr/bin/env python
# coding: utf-8

# In[ ]:


CDC_COVID_API = https://data.cdc.gov/resource/vbim-akqf.json 


# In[3]:


#Import Dependencies 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from census import Census


# In[5]:


# Kyle Test


# In[12]:


#read data files 
state_abb = "Resources/state-abbrevs.csv"
state_area = "Resources/state-areas.csv"

state_abb_read = pd.read_csv(state_abb)
state_abb_df = pd.DataFrame(state_abb_read)

state_area_read = pd.read_csv(state_area)
state_area_df = pd.DataFrame(state_area_read)
state_info_df = pd.merge(state_abb_df, state_area_df)

state_info_df


# In[9]:


#create covid data frame
covid_file= "Resources/all-states-history-1219.csv"
covid_data=pd.read_csv(covid_file)
covid_df = pd.DataFrame(covid_data) 
covid_df.head()


# In[ ]:


#using dataframe of State Abbrevs and State Areas 


# In[ ]:


#review and clean the covid data 
#remove outliers, rename columns


# In[ ]:


#gather general COVID data by states - number of cases by state 
#overlay onto a map in a heatmap in gmaps / use markers per state showing total cases 


# In[ ]:


#gather stats about Census data
#show population per state as marker 


# In[ ]:


#compare # of cases v population density 


# In[ ]:


#combine data about each state and COVID infections grouped by age 
#include % of population, % of COVID infections 


# In[ ]:


#create a summary table of US overall 

