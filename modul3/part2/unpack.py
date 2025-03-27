a = (1, 2, 3, 4, 5, 6)

one, *rest, four = a
print(one)
print(rest)
print(four)

args = 2, *rest
print(args)