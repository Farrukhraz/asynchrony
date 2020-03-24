import functools


class AwesomeException(Exception):
    pass


def initialize_gen(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        g = func(*args, **kwargs)
        g.send(None)
        return g
    return wrapper


def sub_gen():
    while True:
        try:
            message = yield
        except StopIteration:
            break
        else:
            print("Hello from sub_gen! data =", message)
    return "Return from sub_gen!"


@initialize_gen
def delegator(g):
    result = yield from g
    print(result)


# sg = sub_gen()
# d = delegator(sg)
# d.send('Shalom')
# d.throw(StopIteration)


