from pycountry_convert import country_alpha2_to_continent_code, country_name_to_country_alpha2
from functools import reduce
from datetime import datetime as dt,timedelta
import pandas as pd
import numpy as np

#Confirmed_Us_data=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",error_bad_lines=False)
Confirmed_World_data=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",error_bad_lines=False)
#Deaths_Us_data=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv",error_bad_lines=False)
Deaths_World_data=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",error_bad_lines=False)
Recovered_World_data=pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",error_bad_lines=False)
#Recovered_Us_data=pd.read_csv("US_recovered.csv")



def read_df_world_tracker(df,string="NULL"):
    df=pd.melt(df, id_vars=df.columns[0:4], value_vars=df.columns[5:])
    df["variable"]=pd.to_datetime(df["variable"])
    df=df.sort_values("variable")
    df['DateString']=df['variable'].apply(lambda x: x.strftime("%d/%m/%Y"))
    df['variable']=df['variable'].dt.date
    df.rename(columns={'variable': 'Date','value':string},inplace=True)
    L=[]
    for i in df.columns:
        if i.find("_")==-1:
            L.append(i)
        elif i.find("_")!=-1:
            if (i=="Long_"):
                i=i.replace("_","")
            else:
                i=i.replace("_","/")
            L.append(i)
    df.columns=L
    return df
Confirmed_World=read_df_world_tracker(Confirmed_World_data,"Confirmed")
Recovered_World=read_df_world_tracker(Recovered_World_data,"Recovered")
Deaths_World=read_df_world_tracker(Deaths_World_data,"Deaths")

df_world=reduce(lambda left,right: pd.merge(left,right,on=['Date','DateString','Lat','Long','Province/State','Country/Region'],how='outer'), [Confirmed_World,Deaths_World,Recovered_World])
df_world= df_world.reset_index(drop=True)
df_world[['Confirmed','Recovered','Deaths']]=df_world[['Confirmed','Recovered','Deaths']].fillna(0)



case_list = {}
for country in df_world['Country/Region'].unique():
    try:
        if country in case_list:
            case_list[country].append(country_alpha2_to_continent_code(country_name_to_country_alpha2(country)))
        else:
            case_list[country] = country_alpha2_to_continent_code(country_name_to_country_alpha2(country))
    except:
        if country in (['Mainland China','Republic of Korea','Taiwan*','Burma','Korea, South','Hong Kong SAR','Iran (Islamic Republic of)','Taipei and environs','occupied Palestinian territory']):
            case_list[country]="AS"
        elif country=='US':   
            case_list[country]="NA"
        elif country in (['UK','Vatican City','Saint Barthelemy','Kosovo']):
            case_list[country]="EU"
        elif country in(['Congo (Kinshasa)', 'Congo (Brazzaville)']):
            case_list[country]="AF"
        else:
            case_list[country]="Regions undefined"
df_world['Continent']=df_world['Country/Region'].map(case_list)         


# In[6]:


###Groupbylogic
df_ana_1=pd.melt(df_world, id_vars=['Date','Continent','Lat','Long','Province/State','Country/Region'],value_vars=['Deaths','Recovered','Confirmed'])
df_ana_1.rename(columns={"variable":"Flag","value":"Deaths/Recovered/Confirmed"},inplace=True)


def return_func():
   return df_ana_1