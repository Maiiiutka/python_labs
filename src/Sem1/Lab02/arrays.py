import sys
def min_max(nums: list[float | int]): 
    return float(min(nums)) if float(min(nums)) % 1 != 0 else int(min(nums)) ,float(max(nums)) if float(max(nums)) % 1 != 0 else int(max(nums))

def unique_sorted(nums: list[float | int]):
    return sorted(set(nums))

def flatten(mat: list[list | tuple]):
    result = []
    for item in mat:
        result.extend(item)
    return result

buk = "abcdefghijklmnopqrstuvwxyz"
cif = "0123456789"

print("What function you are going to use?")
print("min_max - 1, unique_sorted - 2, flatten - 3")
c = int(input())
if c == 1 or c == 2:
    print("Write your numbers in one line with spaces")
    m = []
    d = input().replace(",", " ").split()
    for i in range(len(d)):
        m.append(int(d[i]) if d[i].count(".") == 0 else float(d[i]))

s = []
if c == 3:
    print("how many lists you want, write number")
    z = input()
    if str(z) not in cif:
        print("ValueError")
        sys.exit() 
    z = int(z)
    print(f"write numbers in one line {z} times")
    for j in range(z):
        l = []
        y = input().replace(","," ").split()
        for v in range(len(y)):
            if str(y[v]) in buk:
                print("TypeError")
                sys.exit() 
            if y[v].count("0") == 0 and y[v].count("1") == 0 and y[v].count("2") == 0 and y[v].count("3") == 0 and y[v].count("4") == 0 and y[v].count("5") == 0 and y[v].count("6") == 0 and y[v].count("7") == 0 and y[v].count("8") == 0 and y[v].count("9") == 0:
                break
            l.append(int(y[v]) if y[v].count(".") == 0 else float(y[v]))
        s.append(l)




if c == 1:
    print(min_max(m) if len(m) > 0 else "ErrorValue")
elif c == 2:
        print(unique_sorted(m) if len(m) > 0 else [])
else:
    print(flatten(s))