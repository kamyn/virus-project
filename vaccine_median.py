import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import date
import matplotlib.dates as mdates

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

    ax = fig.add_subplot(221)
    ax.plot(datelist, vaccine)
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
    

    ax = fig.add_subplot(223)
    ax.plot(datelist, vaccine_reg)
    ax.plot(date1, vaccine_reg[0], '-bo', date2, vaccine_reg[-1], 'bo')
    ax.set(title='Vaccinated per Day',
            xlabel='Date',
            ylabel='Deaths')
    ax.grid()

    ax = fig.add_subplot(133)
    ax.boxplot(vaccine_reg)
    ax.set(title=f"Vaccine per Day, median: {stat.median(vaccine_reg)}",
           xlabel = '', ylabel='Vaccinated')

    plt.savefig(f"vaccine_median_plots/{country}.png")
    j += 1
    #plt.show()
