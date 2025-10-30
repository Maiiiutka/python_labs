cif = "0123456789"
buk = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
spec = "."
shifr = str(input())
shifr = list(shifr)
fin = ""
k = 0
s = True
first = 0 
second = 0 
stop = False

for i in range (len(shifr)):
    ind = i 
    if shifr[ind] in buk:
        fin += shifr[ind]
        first = i
    if shifr[i] in cif and s == True:
        fin += shifr[i+1]
        s = False 
        second = i + 1
    shag = second - first  
    ostalos = len(shifr[:second])
    if shag > 0 and ostalos != len(shifr):
        for j in range(ostalos+shag,len(shifr),shag):
            fin += shifr[j]
            if shifr[j] == ".":
                stop = True
    if stop == True:
        break
print(fin)