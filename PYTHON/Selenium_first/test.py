M = 9
def puzzle(a):
    for i in range(M):
        with open('text.txt', 'a') as file:
            file.write("\n")
            for j in range(M):
                file.write(str(a[i][j])+" ")
                #print(a[i][j], end=" ")
        print()


def solve(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False

    for x in range(9):
        if grid[x][col] == num:
            return False

    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(2):
        for j in range(2):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True


def Suduko(grid, row, col):
    with open('text.txt','a') as file:
        file.write("Calling function with row:" + str(row) + "and col: "+ str(col)+"\n")
        puzzle(grid)
    if (row == M - 1 and col == M):
        return True
    if col == M:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Suduko(grid, row, col + 1)
    for num in range(1, M + 1, 1):

        if solve(grid, row, col, num):

            grid[row][col] = num
            if Suduko(grid, row, col + 1):
                print("YES")
                return True
        grid[row][col] = 0
    return False


'''0 means the cells where no value is assigned'''
grid = [[2, 5, 0, 0, 3, 0, 9, 0, 1],
        [0, 1, 0, 0, 0, 4, 0, 0, 0],
        [4, 0, 7, 0, 0, 0, 2, 0, 8],
        [0, 0, 5, 2, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 9, 8, 1, 0, 0],
        [0, 4, 0, 0, 0, 3, 0, 0, 0],
        [0, 0, 0, 3, 6, 0, 0, 7, 2],
        [0, 7, 0, 0, 0, 0, 0, 0, 3],
        [9, 0, 3, 0, 0, 0, 6, 0, 4]]

# grid = [
#     [4,0,0,2],
#     [0,0,0,4],
#     [0,3,0,0],
#     [1,0,0,0]
# ]

if (Suduko(grid, 0, 0)):
    puzzle(grid)
else:
    print("Solution does not exist:(")