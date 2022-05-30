import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import date
import matplotlib.dates as mdates

sick_db = pd.read_csv("data/time_series_covid19_confirmed_global.csv")
sick_db = sick_db.drop(columns = ['Province/State', 'Lat', 'Long'])
del_col = sick_db.columns[1:325]
sick_db = sick_db.drop(columns = del_col)
sick_db = sick_db.dropna()

death_db = pd.read_csv("data/time_series_covid19_deaths_global.csv")
death_db = death_db.drop(columns = ['Province/State', 'Lat', 'Long'])
del_col = death_db.columns[1:325]
death_db = death_db.drop(columns = del_col)
death_db = death_db.dropna()

vaccine_db = pd.read_csv("data/time_series_covid19_vaccine_global.csv")
vaccine_db = vaccine_db.drop(columns = ['Province_State', 'Lat', 'Long_',
                                        'UID', 'iso2', 'iso3', 'code3',
                                        'FIPS', 'Admin2', 'Combined_Key',
                                        'Population'])
vaccine_db = vaccine_db.dropna()

#list of dates
date_lst = vaccine_db.columns.tolist()
date_lst = date_lst[1:]
print(f"first day: {date_lst[0]}\nlast_day: {date_lst[-1]}")
days = np.arange(1, len(date_lst) + 1, 1)

date1 = date(2020, 12, 12)
date2 = date(2022, 5, 28)
datelist = pd.date_range(date1, date2).tolist()

#list of regions
country_list = vaccine_db['Country_Region'].values.tolist()

set_norm = 0 

j = 0
while j < len(country_list):
    country = country_list[j]

    fig = plt.figure(f"virus in {country}", figsize=(20, 20))

    """vaccine stuff"""
    vaccine = vaccine_db.loc[
                vaccine_db['Country_Region']==country].values.tolist()[0]
    vaccine = vaccine[1:]

    count = 0
    while count != len(vaccine) - 1:
        if(vaccine[count] > vaccine[count + 1]):
            vaccine[count + 1] = vaccine[count]
        count += 1

    ax = fig.add_subplot(321)
    ax.plot(datelist, vaccine)
    if set_norm == 1:
        mx = max(vaccine)
        ax.set_ylim(0, mx)
    ax.set(title=f"Total vaccine in {country}",
            xlabel='Date',
            ylabel='vaccineted')
    ax.plot(date1, vaccine[0], '-bo', date2, vaccine[-1], 'bo')
    ax.text(datelist[0], vaccine[0], f"{date1}", color='r')
    ax.text(datelist[-50], vaccine[-1], f"{date2}", color='r')
    ax.grid()

    count = 0
    vaccine_reg = list()
    vaccine_reg.append(vaccine[count])
    while count != len(vaccine) - 1:
        vaccine_reg.append(vaccine[count + 1] - vaccine[count])
        count += 1
    

    ax = fig.add_subplot(322)
    ax.plot(datelist, vaccine_reg)
    if set_norm == 1:
        mx1 = max(vaccine_reg)
        ax.set_ylim(0, mx1)
    ax.plot(date1, vaccine_reg[0], '-bo', date2, vaccine_reg[-1], 'bo')
    ax.set(title='Vaccinated per Day',
            xlabel='Date',
            ylabel='Deaths')
    ax.grid()

    """death stuff"""
    death = death_db.loc[
            death_db['Country/Region']==country].values.tolist()[0]
    tmp = death[1]
    death = death[2:]

    i = 0
    while i < len(death):
        if death[i] < 0:
            death[i] = 0
        i += 1

    count = 0
    death_reg = list()
    death_reg.append(death[0] - tmp)
    while count != len(death) - 1:
        death_reg.append(abs(death[count + 1] - death[count]))
        count += 1

    ax = fig.add_subplot(323)
    if set_norm == 1:
        ax.set_ylim(0, mx)
    ax.plot(datelist, death)
    ax.set(title=f"Total Deaths in {country}: {max(death)}",
            xlabel='Date',
            ylabel='Deaths')
    ax.plot(date1, death[0], '-bo', date2, death[-1], 'bo')
    ax.text(datelist[0], death[0], f"{date1}", color='r')
    ax.text(datelist[-50], death[-1], f"{date2}", color='r')
    ax.grid()

    ax = fig.add_subplot(324)
    ax.plot(datelist, death_reg)
    if set_norm == 1:
        ax.set_ylim(0, mx1)
    ax.plot(date1, death_reg[0], '-bo', date2, death_reg[-1], 'bo')
    ax.set(title=f"Deaths per Day, max: {max(death_reg)}",
            xlabel='Date',
            ylabel='Deaths')
    ax.grid()

    """sick stuff"""
    sick = sick_db.loc[
            sick_db['Country/Region']==country].values.tolist()[0]
    tmp = sick[1]
    sick = sick[2:]

    i = 0
    while i < len(sick):
        if sick[i] < 0:
            sick[i] = 0
        i += 1

    count = 0
    sick_reg = list()
    sick_reg.append(sick[0] - tmp)
    while count != len(sick) - 1:
        sick_reg.append(abs(sick[count + 1] - sick[count]))
        count += 1

    ax = fig.add_subplot(325)
    ax.plot(datelist, sick)
    if set_norm == 1:
        ax.set_ylim(0, mx)
    ax.set(title=f"Total Ill situation in {country}",
            xlabel='Date',
            ylabel='Illness situation')
    ax.plot(date1, sick[0], '-bo', date2, sick[-1], 'bo')
    ax.text(datelist[0], sick[0], f"{date1}", color='r')
    ax.text(datelist[-50], sick[-1], f"{date2}", color='r')
    ax.grid()

    ax = fig.add_subplot(326)
    ax.plot(datelist, sick_reg)
    if set_norm == 1:
        ax.set_ylim(0, mx1)
    ax.plot(date1, sick_reg[0], '-bo', date2, sick_reg[-1], 'bo')
    ax.set(title='Ill situation per Day',
            xlabel='Date',
            ylabel='Ill situation')
    ax.grid()

    j += 1
    print(country)
    
    if set_norm == 0:
        plt.savefig(f"vaccine_rates_cmp_plots/not_norm/{country}.png")
    if set_norm == 1:
        plt.savefig(f"vaccine_rates_cmp_plots/norm/{country}.png")
    #plt.show()
