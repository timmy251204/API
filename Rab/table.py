table = []
for i in range (10):
    table.append(list(map(int, input().split(' '))))
print(table)
table_run_min = []
table_run_max= []
for i in range(10):
    table_run_max.append([0] * 10)
    table_run_min.append([0] * 10)
table_run_min[0][0] = table[0][0]
table_run_max[0][0] = table[0][0]



def min_run(n):
    for i in range (n):
        for j in range (n):
            if i == 0 and j == 0:
                table_run_min[i][j] = table[i][j]
            elif i == 0:
                table_run_min[i][j] = table_run_min[i][j - 1] + table[i][j]
            elif j == 0:
                table_run_min[i][j] = table_run_min[i - 1][j] + table[i][j]
            else:
                table_run_min [i][j] = min(table_run_min[i - 1][j], table_run_min[i][j - 1]) + table[i][j]
def max_run(n):
    for i in range (n):
        for j in range (n):
            if i == 0 and j == 0:
                table_run_max[i][j] = table[i][j]

            elif i == 0:
                table_run_max[i][j] = table_run_max[i][j - 1] + table[i][j]

            elif j == 0:
                table_run_max[i][j] = table_run_max[i - 1][j] + table[i][j]

            else:
                table_run_max[i][j] = max(table_run_max[i - 1][j], table_run_max[i][j - 1]) + table[i][j]


min_run(10)
max_run(10)
print(table_run_max[9][9])
print(table_run_min[9][9])
