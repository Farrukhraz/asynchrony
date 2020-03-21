def some_yields():
    n = 10
    while True:
        yield n
        yield (n // 10)
        yield (n / 2)
        n += 10


g = some_yields()
print(next(g))
print(next(g))
print(next(g))
print(next(g))             # Вышли из 1-ой итерации цикла и поехали по новой
print(next(g))
print(next(g))
