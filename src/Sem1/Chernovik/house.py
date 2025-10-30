doors = int(5)
floors = int(5)
flats = int(20)
floor_flat = int(4)

number = int(input("Введите номер квартиры: "))
door_number = int((number - 1) // flats + 1)
floor_number = int(((number + 3) - (door_number - 1) * flats) // floor_flat)

if (0 < door_number <= doors) and (0 < floor_number <= floors):
    print("Номер подъезда: ", door_number)
    print("Этаж: ", floor_number)
else:
    print("Error")