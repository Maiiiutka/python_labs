buk = "abcdefghijklmnopqrstuvwxyz"
def format_record(rec: tuple[str, str, float]):
    result = []
    FIO = rec[0].split()
    FIO_LEN = len(FIO)
    if FIO_LEN == 0:
        return "ValueError"
    elif FIO_LEN == 3:
        c = rec[0].split()
        second = c[1][0] + "."
        third = c[2][0] + "."
        NEW_FIO = c[0][0].upper() + c[0][1:].lower() + " " + second.upper() + third.upper()
    elif FIO_LEN == 2:
        c = rec[0].split()
        second = c[1][0] + "."
        NEW_FIO = c[0][0].upper() + c[0][1:].lower() + " " + second.upper()
    result.append(NEW_FIO)
    if rec[1] == "":
        return "ValueError"
    else:
        NEW_GROUP = "гр." + " " + rec[1]
    result.append(NEW_GROUP)
    GPU_STR = str(rec[2])
    for j in GPU_STR:
        if GPU_STR.count(".") == 1:
            if j not in buk:
                NEW_GPU = f"GPU {round(float(rec[2]), 2):.2f}"
        else:
            return "ErrorValue"
    result.append(NEW_GPU)
    return result[0] +"," + " " + result[1]+ "," + " " +result[2]


print(format_record(("ИВАНОВ ИВАН ИВАНОВИЧ", "BIVT-25", 4.6)))
print(format_record(("Петров Пётр", "IKBO-12", 5.0)))
print(format_record(("Петров Пётр Петрович", "IKBO-12", 5.0)))
print(format_record(("  сидорова  анна   сергеевна ", "ABB-01", 3.999)))