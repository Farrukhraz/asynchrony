from inspect import getgeneratorstate
import functools


def initialize_gen(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper


@initialize_gen
def gen():
    index = 0
    while True:
        step = yield index
        index += step or 1


class AwesomeException(Exception):
    pass


@initialize_gen
def average():
    sum_ = 0
    count = 0
    average_sum = None          # None для того чтобы "x = yield average" при первом вызове нечего не возвращал
    while True:
        try:
            num = yield average_sum
        except StopIteration:
            print("Stopped by StopIteration!")
        except AwesomeException:
            print("Stopped by your AwesomeException!")
        else:
            sum_ += num
            count += 1
            average_sum = round(sum_ / count, 2)















