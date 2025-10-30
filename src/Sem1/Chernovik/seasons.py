def season(month):
    time = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
    if month in time[0:2]:
        season_name = "winter"
    elif month in time[11:12]:
        season_name = "winter"
    elif month in time[2:5]:
        season_name = "spring"
    elif month in time[5:8]:
        season_name = "summer"
    elif month in time[8:11]:
        season_name = "autumn"
    return(season_name)

month = int(input("Enter number of month: "))
season_name = season(month)
print(season_name)