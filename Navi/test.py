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


@initialize_gen
def subgen():
    while True:
        try:
            msg_from_delegator = yield
        except AwesomeException:
            print("AwesomeException from delegator received!")
        else:
            print("Delegator sent this message: ", msg_from_delegator)


@initialize_gen
def delegator(sg):
    while True:
        try:
            message = yield
        except AwesomeException as ex:
            sg.throw(ex)
        else:
            sg.send(message)

