n = int(input())


def even(n):
    value = 0
    for _ in range(0, n):
        if value % 2 == 0:
            yield value
            value = value + 2


# Don't forget to print out the first n numbers one by one here
generator = even(n)
for n in range(0, n):
    print(next(generator))
