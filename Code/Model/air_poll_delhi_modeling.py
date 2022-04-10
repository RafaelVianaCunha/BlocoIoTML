!pip install seaborn==0.9.0
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
import seaborn as sns

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv('../../Data/Modeling/airpollutiondelhidataset.csv')
df.head()

df.date = pd.to_datetime(df.date, errors='coerce')
df['year'] = df['date'].dt.year
df.set_index('date', inplace=True)

df.pm25 = df.pm25.astype(float).fillna(0.0)
df.pm10 = df.pm10.astype(float).fillna(0.0)
df.so2 = df.so2.astype(float).fillna(0.0)
df.co = df.co.astype(float).fillna(0.0)
df.ozone = df.ozone.astype(float).fillna(0.0)

# The AQI calculation uses 7 measures: PM2.5, PM10, SO2, NOx, NH3, CO and O3.
# For PM2.5, PM10, SO2, NOx and NH3 the average value in last 24-hrs is used with the condition of having at least 16 values.
# For CO and O3 the maximum value in last 8-hrs is used.
# Each measure is converted into a Sub-Index based on pre-defined groups.
# Sometimes measures are not available due to lack of measuring or lack of required data points.
# Final AQI is the maximum Sub-Index with the condition that at least one of PM2.5 and PM10 should be available and at least three out of the seven should be available.

df["PM10_24hr_avg"] = df.groupby("name")["pm10"].rolling(window = 24, min_periods = 16).mean().values
df["PM2.5_24hr_avg"] = df.groupby("name")["pm25"].rolling(window = 24, min_periods = 16).mean().values
df["SO2_24hr_avg"] = df.groupby("name")["so2"].rolling(window = 24, min_periods = 16).mean().values
df["CO_8hr_max"] = df.groupby("name")["co"].rolling(window = 8, min_periods = 1).max().values
df["O3_8hr_max"] = df.groupby("name")["ozone"].rolling(window = 8, min_periods = 1).max().values

## PM2.5 Sub-Index calculation
def get_PM25_subindex(x):
    if x <= 30:
        return x * 50 / 30
    elif x <= 60:
        return 50 + (x - 30) * 50 / 30
    elif x <= 90:
        return 100 + (x - 60) * 100 / 30
    elif x <= 120:
        return 200 + (x - 90) * 100 / 30
    elif x <= 250:
        return 300 + (x - 120) * 100 / 130
    elif x > 250:
        return 400 + (x - 250) * 100 / 130
    else:
        return 0

df["PM2.5_SubIndex"] = df["PM2.5_24hr_avg"].apply(lambda x: get_PM25_subindex(x))

## PM10 Sub-Index calculation
def get_PM10_subindex(x):
    if x <= 50:
        return x
    elif x <= 100:
        return x
    elif x <= 250:
        return 100 + (x - 100) * 100 / 150
    elif x <= 350:
        return 200 + (x - 250)
    elif x <= 430:
        return 300 + (x - 350) * 100 / 80
    elif x > 430:
        return 400 + (x - 430) * 100 / 80
    else:
        return 0

df["PM10_SubIndex"] = df["PM10_24hr_avg"].apply(lambda x: get_PM10_subindex(x))

## SO2 Sub-Index calculation
def get_SO2_subindex(x):
    if x <= 40:
        return x * 50 / 40
    elif x <= 80:
        return 50 + (x - 40) * 50 / 40
    elif x <= 380:
        return 100 + (x - 80) * 100 / 300
    elif x <= 800:
        return 200 + (x - 380) * 100 / 420
    elif x <= 1600:
        return 300 + (x - 800) * 100 / 800
    elif x > 1600:
        return 400 + (x - 1600) * 100 / 800
    else:
        return 0

df["SO2_SubIndex"] = df["SO2_24hr_avg"].apply(lambda x: get_SO2_subindex(x))

## CO Sub-Index calculation
def get_CO_subindex(x):
    if x <= 1:
        return x * 50 / 1
    elif x <= 2:
        return 50 + (x - 1) * 50 / 1
    elif x <= 10:
        return 100 + (x - 2) * 100 / 8
    elif x <= 17:
        return 200 + (x - 10) * 100 / 7
    elif x <= 34:
        return 300 + (x - 17) * 100 / 17
    elif x > 34:
        return 400 + (x - 34) * 100 / 17
    else:
        return 0

df["CO_SubIndex"] = df["CO_8hr_max"].apply(lambda x: get_CO_subindex(x))

## O3 Sub-Index calculation
def get_O3_subindex(x):
    if x <= 50:
        return x * 50 / 50
    elif x <= 100:
        return 50 + (x - 50) * 50 / 50
    elif x <= 168:
        return 100 + (x - 100) * 100 / 68
    elif x <= 208:
        return 200 + (x - 168) * 100 / 40
    elif x <= 748:
        return 300 + (x - 208) * 100 / 539
    elif x > 748:
        return 400 + (x - 400) * 100 / 539
    else:
        return 0

df["O3_SubIndex"] = df["O3_8hr_max"].apply(lambda x: get_O3_subindex(x))

## AQI bucketing
def get_AQI_bucket(x):
    if x <= 50:
        return "Good"
    elif x <= 100:
        return "Satisfactory"
    elif x <= 200:
        return "Moderate"
    elif x <= 300:
        return "Poor"
    elif x <= 400:
        return "Very Poor"
    elif x > 400:
        return "Severe"
    else:
        return np.NaN

df["Checks"] = (df["PM2.5_SubIndex"] > 0).astype(int) + \
                (df["PM10_SubIndex"] > 0).astype(int) + \
                (df["SO2_SubIndex"] > 0).astype(int) + \
                (df["CO_SubIndex"] > 0).astype(int) + \
                (df["O3_SubIndex"] > 0).astype(int)

df["AQI_calculated"] = round(df[["PM2.5_SubIndex", "PM10_SubIndex", "SO2_SubIndex", 
                                 "CO_SubIndex", "O3_SubIndex"]].max(axis = 1))
df.loc[df["PM2.5_SubIndex"] + df["PM10_SubIndex"] <= 0, "AQI_calculated"] = np.NaN
df.loc[df.Checks < 3, "AQI_calculated"] = np.NaN

df["AQI_bucket_calculated"] = df["AQI_calculated"].apply(lambda x: get_AQI_bucket(x))

"""## Qualidade do ar ao longo do tempo"""

df_aqi = df['AQI_calculated'].resample('1M').mean()
df_aqi = pd.DataFrame(df_aqi).fillna(0)

fig, ax = plt.subplots(1, 1, figsize=(20, 7));
df_aqi.plot(ax = ax);
plt.xlabel('Período');
plt.ylabel('Qualidade do ar');

"""## Qualidade do ar por cidade"""

city_most_polluted = df[['city', 'AQI_calculated']].groupby(['city']).mean().sort_values(by = 'AQI_calculated', ascending = False)
city_most_polluted

plt.style.use('seaborn-whitegrid')
f, ax = plt.subplots(1, 1, figsize = (15,15))

bar1 = sns.barplot(x = city_most_polluted.AQI_calculated,
                   y = city_most_polluted.index,
                   palette = 'Reds_r',
                   ax = ax);

ax.set_ylabel('')   
ax.set_yticklabels(labels = ax.get_yticklabels(), fontsize = 14);
ax.set_title('Indíce de qualidade do ar')
f.tight_layout();

"""## Distribuição do AQI ao longo do tempo"""

fig, ax= plt.subplots(1, 1, figsize=(20, 6))
plt.title('Ditribuição da classificação do AQI ao longo do tempo')
sns.countplot(x = 'AQI_bucket_calculated', data = df, hue='year');

df = df.reset_index()

dates = pd.to_datetime(df['date'].values)
df['month'] = dates.month
df['month_name'] = dates.month_name()

aqi_month = df.groupby(['month','month_name'])['AQI_calculated'].mean().reset_index()
aqi_month['AQI_calculated'] = round(aqi_month['AQI_calculated'],2)
average = round(aqi_month['AQI_calculated'].mean(), 2)

px.bar(data_frame= aqi_month, x = aqi_month['month_name'], y = (aqi_month['AQI_calculated'].values - average), color = 'AQI_calculated',
       color_continuous_scale=px.colors.sequential.Bluered,template = 'ggplot2',
      labels = {'y':'Variação mensal no AQI da média','month_name':''} ,hover_name = aqi_month['month_name'],
      hover_data={'month_name': False},title = 'AQI médio: ' + str(average),width = 750,height = 500)

"""# Prevendo próximo dois anos"""

df = df.reset_index()

data_aqi = df[['date', 'AQI_calculated']]
data_aqi.set_index('date', inplace=True)
data_aqi = data_aqi['AQI_calculated'].resample('M').mean()

fig, ax= plt.subplots(1, 1, figsize=(20, 6))
sns.set_style("ticks")
sns.set_context("talk")

data_aqi.plot(ax=ax)
ax.yaxis.grid(True)
sns.despine(offset=5, trim=False)

"""Separando treino e teste"""

size_of_train = int(np.ceil(data_aqi.shape[0] * 0.70))
train = data_aqi.iloc[:size_of_train]
test = data_aqi.iloc[size_of_train:]

fig, ax = plt.subplots(1, 1, figsize=(20, 6))
sns.set_style("ticks")
sns.set_context("talk")

train.plot(ax=ax)
test.plot(ax=ax, c="g")
ax.yaxis.grid(True)
ax.legend(["Treino", "Teste"])
sns.despine(offset=5, trim=False)

train_prophet = train.reset_index().rename(columns={'date': 'ds', 'AQI_calculated': 'y'})
train_prophet.head()

from fbprophet import Prophet

model = Prophet()
model.fit(train_prophet)

periods = df_aqi.shape[0] - size_of_train
future = model.make_future_dataframe(periods = periods, freq="M")
forecast = model.predict(future)

Sfig, ax= plt.subplots(1, 1, figsize=(20, 6))
sns.set_style("ticks")

sns.set_context("talk")
model.plot(forecast, ax=ax);

test.plot(ax=ax, c="g");
ax.yaxis.grid(True)

sns.despine(offset=5, trim=False)

"""## Prevendo próximos três anos"""

far_future = model.make_future_dataframe(periods= 3 * periods, freq="M")
far_forecast = model.predict(far_future)

fig, ax= plt.subplots(1, 1, figsize=(20, 6))
sns.set_style("ticks")

sns.set_context("talk")
model.plot(far_forecast, ax=ax);

test.plot(ax=ax, c="g");
ax.yaxis.grid(True)

sns.despine(offset=5, trim=False)