import pandas as pd

sick_db = pd.read_csv("data/time_series_covid19_confirmed_global.csv")
print(sick_db.info())
print(sick_db.head(5))
print(sick_db.tail(5))

death_db = pd.read_csv("data/time_series_covid19_deaths_global.csv")
print(death_db.info())
print(death_db.head(5))
print(death_db.tail(5))

vaccine_db = pd.read_csv("data/time_series_covid19_vaccine_global.csv")
print(vaccine_db.info())
print(vaccine_db.head(5))
print(vaccine_db.tail(5))
