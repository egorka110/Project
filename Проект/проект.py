import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objs as go  
import plotly.express as px 
from pandas_profiling import ProfileReport
from datetime import datetime
df = pd.read_csv('covid_19_data.csv')
df['Province/State'] = df['Province/State'].fillna("Unknown") 
df.isnull().sum()  # нулевые значения
df.info() #информация о датасте
df = df.rename(columns = {"Province/State":"State"})
df = df.rename(columns = {"Country/Region":"Country"}) #изменяет название
df[['Confirmed','Deaths','Recovered']] = df[['Confirmed','Deaths','Recovered']].astype(int)  #заменяет значениями типа integer
df['Active'] = df['Confirmed']-df['Deaths']-df['Recovered']
df.columns
df['Date'] = df['ObservationDate'].copy()
labels = ["Active Cases","Recovered Cases","Death Cases"]

sumactive= sum(df['Active'])
sumrecoverd = sum(df['Recovered'])
sumdeaths = sum(df['Deaths'])

fig = px.pie(df, 
             values = [sumactive,sumrecoverd,sumdeaths],
             names = labels,
             color_discrete_sequence = ['SkyBlue','PaleGreen','LightSlateGray'])

fig.update_traces(textposition = 'inside', textinfo = 'percent+label') #установка значений 

fig.update_layout(title = 'Процент заболевших Covid-19 в мире',
                  title_x = 0.5,
                  title_font= dict(size = 18, color = 'MidnightBlue' )) #установка значений

fig.show()


df['Date'] = pd.to_datetime(df['Date'])
df = df.sort_values("Date") #сортировка значений
dftime = df.groupby("Date")[["Confirmed","Active","Recovered","Deaths"]].sum().reset_index() #группирровка значений



df1 = df.groupby("Country")["Recovered"].sum().sort_values(ascending = False).reset_index().head(30)

fig = px.bar(df1,
             x = 'Country',
             y = 'Recovered',
             color = 'Recovered',
             color_continuous_scale = 'greens',
             labels = {"Confirmed":"Recovered Cases"})

fig.update_layout(title = 'Top 30 Countries with the most Recovered Cases',
                  title_x = 0.5,
                  title_font = dict(size = 18, color = 'DarkGreen'),
                  yaxis = dict(title = 'Recovered Cases'),
                  xaxis = dict(tickangle = 45))

fig.show()

df1 = df.groupby("Country")["Deaths"].sum().sort_values(ascending = False).reset_index().head(30)

fig = px.bar(df1,
             x = 'Country',
             y = 'Deaths',
             color = 'Deaths',
             color_continuous_scale = 'gray',
             labels = {"Deaths":"Death Cases"})

fig.update_layout(title = 'Top 30 Countries with the most Death Cases',
                  title_x = 0.5,
                  title_font = dict(size = 18, color = 'DarkSlateGray'),
                  yaxis = dict(title = 'Death Cases'),
                  xaxis = dict(tickangle = 45))

fig.show()