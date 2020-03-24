from inspect import getgeneratorstate
import functools


def initialize_gen(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper


class AwesomeException(Exception):
    pass


def sub_gen():
    sum_ = 0
    while True:
        try:
            num = yield
            if hasattr(num, '__int__'):
                sum_ += num
        except StopIteration:
            print("Sub_gen has been stopped!")
            break
        else:
            pass
    return sum_


@initialize_gen
def delegator(g):
    result = yield from g   # == (x = yield; g.send(x)/g.throw(x))
    print("Result is", result)


sg = sub_gen()
d = delegator(sg)
d.send(12)
d.send('123')
d.send(True)
d.throw(StopIteration)



