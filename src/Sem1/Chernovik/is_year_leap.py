year = int(input("Entr year: "))

if year % 4 == 0 and year % 100 == 0 and year % 400 == 0:
    print("Visokosniy year")
elif year % 4 == 0 and year % 100 == 0 and year % 400 != 0:
    print("Default year")
elif year % 4 == 0:
    print("Visokosniy year")
else:
    print("Default year")