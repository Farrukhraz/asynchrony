from collections import deque
from time import sleep


def counter():
    count = 0
    while True:
        print(count)
        count += 1
        sleep(0.3)
        yield


def greet():
    n = 0
    while True:
        if n % 3 == 0:
            print("Hello, sir!")
        yield
        n += 1


def main():
    g1 = counter()
    g2 = greet()
    deque_ = deque([g1, g2])
    while True:
        g = deque_.popleft()
        next(g)
        deque_.append(g)


if __name__ == '__main__':
    main()

