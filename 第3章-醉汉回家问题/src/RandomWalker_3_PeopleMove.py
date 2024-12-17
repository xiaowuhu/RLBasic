
city = 20000
country = 100000
city_2_country = 0.1
country_2_city = 0.3

city_old = city
country_old = country

for i in range(26):
    print(f"{i}, {country:.0f}, {city:.0f}")
    city = city_old + country_old * country_2_city - city_old * city_2_country
    country = country_old + city_old * city_2_country - country_old * country_2_city
    city_old = city
    country_old = country


import numpy as np

a = np.array([[0.7, 0.3],[0.1, 0.9]])
b = a.copy()
for i in range(35):
    b = np.dot(b, a)
    print(i, b)
