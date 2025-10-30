def transpose(mat: list[list[float | int]]):
    result = []
    if mat == []:
        return []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ValueError"
    for i in range(len(mat[0])):
        new_mat = []
        for j in range(len(mat)):
            new_mat.append(mat[j][i])
        result.append(new_mat)
    return result

def row_sums(mat: list[list[float | int]]):
    result = []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ErrorValue"
    if mat == []:
        return []
    for i in range(len(mat)):
        s = sum(mat[i])
        result.append(s)
    return result 

def col_sums(mat: list[list[float | int]]):
    result = []
    first = len(mat[0])
    for row in mat:
        if first != len(row):
            return "ValueError"
    for i in range(len(mat[0])):
        new_mat = 0
        for j in range(len(mat)):
            new_mat += mat[j][i]
        result.append(new_mat)
    return result 

print(transpose([[1, 2], [3, 4]]))
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[1, 2, 3], [4, 5, 6]]))