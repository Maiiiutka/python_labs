N = int(input())
m = []
for i in range(N):
    m.append(input())
k1 = 0
k2 = 0
for i in range(len(m)):
    if m[i].count("True") > 0:
        k1 += 1
    elif m[i].count("False") > 0:
        k2 += 1
print(k1,k2)