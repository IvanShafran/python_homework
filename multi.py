table = tuple(tuple((x + 1)*(y + 1) for y in range(9)) for x in range(9))
for x in table:
    print(x)