

def coroutine(x):
    while True:
        message = yield
        if x in message:
            print(message)


g = coroutine('al;skdf;lasdfj;alsdjfklajkgjn,mnvjlkashdfjfja;lkfdsjfjdklsa;')
g.send(None)
g.send("ad")
g.send("ad")
g.send("ad")
next(g)
g.send("ad")
