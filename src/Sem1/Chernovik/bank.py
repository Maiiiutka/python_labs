def bank(s, years):
    percent = 1.1
    for i in range (years):
        s = s * percent
    return(s)

s = float(input("Enter count of money: "))
years = int(input("Enter how many years: "))
end = int(bank(s, years))
print(end)

#Функция банк для расчета вклада