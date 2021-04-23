a = list(input())
a = a
b = []
count = 0
for i in range(1, len(a)):
    if a[i] != a[i - 1]:
        if i == len(a) - 1:
            b.append(count)
        else:
            count += 1
    else:
        b.append(count)
        count = 1
print(max(b) + 1)

# 0 1 2 3 4 5
