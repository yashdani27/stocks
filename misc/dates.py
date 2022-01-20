from datetime import datetime, date
import datetime
import math

print(datetime.datetime.today())
print(datetime.datetime.today().weekday())

# m t w t f s s
# 0 1 2 3 4 5 6
# 0 6 5 4 3 2 1


day_number = datetime.datetime.strptime("1/1/2026", '%d/%m/%Y').weekday()
add = [0, 6, 5, 4, 3, 2, 1]

print('next monday on ' + str(1 + add[day_number]))
print('next monday on ' + str(1 + (7 - day_number) % 7))


print(str(datetime.datetime.now()).split(' ')[0].split('-'))

doy = datetime.datetime.now().timetuple().tm_yday

print(doy)
print(doy/365)

buy_price = 100
current_price = 120
buy_date = 1
buy_month = 1
buy_year = 2021
current_date = 8
current_month = 9
current_year = 2021

b_date = date(buy_year, buy_month, buy_date)
c_date = date(current_year, current_month, current_date)
diff_days = (c_date - b_date).days
print(diff_days)

cagr = (((current_price / buy_price) ** (1 / (diff_days/365))) - 1) * 100

print(cagr)

