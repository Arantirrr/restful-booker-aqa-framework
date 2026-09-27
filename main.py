def add(x, y, z):
    return x + y + z

nums = (1, 2, 3)
print(add(*nums))   # это ровно то же самое, что add(1, 2, 3)