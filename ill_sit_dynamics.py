import statistics as stat
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from datetime import date
import matplotlib.dates as mdates

#import & work with base structure
death_db = pd.read_csv('data/time_series_covid19_confirmed_global.csv')
death_db = death_db.drop(columns = ['Province/State', 'Lat', 'Long'])
death_db = death_db.dropna()

#list of dates
date_lst = death_db.columns.tolist()
date_lst = date_lst[1:]
print(f"first day: {date_lst[0]}\nlast_day: {date_lst[-1]}")
days = np.arange(1, len(date_lst) + 1, 1)

date1 = date(2020, 1, 22)
date2 = date(2022, 5, 28)
datelist = pd.date_range(date1, date2).tolist()

#list of deaths
country_list = death_db['Country/Region'].values.tolist()

#country = country_list[0]
j = 0
while j < len(country_list) - 1:
    if(country_list[j] == country_list[j + 1]):
        j += 1
        continue
    country = country_list[j]
    j += 1

    death = death_db.loc[
            death_db['Country/Region']==country].values.tolist()[0]
    death = death[1:]

    i = 0
    while i < len(death):
        if death[i] < 0:
            death[i] = 0
        i += 1

    count = 0
    death_reg = list()
    death_reg.append(death[count])
    while count != len(death) - 1:
        death_reg.append(abs(death[count + 1] - death[count]))
        count += 1

    #plots
    fig = plt.figure(f"virus in {country}", figsize=(20, 10))

    ax = fig.add_subplot(221)
    ax.plot(datelist, death)
    ax.set(title=f"Total ill situations in {country}: {max(death)}",
            xlabel='Date',
            ylabel='Ill situation')
    ax.plot(date1, death[0], '-bo', date2, death[-1], 'bo')
    ax.text(datelist[0], death[0], f"{date1}", color='r')
    ax.text(datelist[-50], death[-1], f"{date2}", color='r')
    ax.grid()

    ax = fig.add_subplot(223)
    ax.plot(datelist, death_reg)
    ax.plot(date1, death_reg[0], '-bo', date2, death_reg[-1], 'bo')
    ax.set(title=f"Ill situation per Day, max: {max(death_reg)}",
            xlabel='Date',
            ylabel='Ill situation')
    ax.grid()

    ax = fig.add_subplot(133)
    ax.boxplot(death_reg)
    ax.set(title=f"Ill situation per Day, median: {stat.median(death_reg)}",
           xlabel = '', ylabel='Ill situations')
    
    plt.savefig(f"ill_sit_plots/{country}.png")
    #plt.show()
    print(f"{country}\n")
