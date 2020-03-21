from collections import deque


def gen1(n):
    for i in range(n):
        yield print(i)


def gen2(string):
    for el in string:
        yield print(el)


g1 = gen1(3)
g2 = gen2('Bob')

tasks = deque([g1, g2])

while tasks:
    try:
        task = tasks.popleft()
        next(task)
        tasks.append(task)
    except StopIteration:
        pass



