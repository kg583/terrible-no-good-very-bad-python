def do_while(cond):
    def inner(func):
        def loop():
            func()
            while cond():
                func()

        return loop

    return inner


a = 8
@do_while(lambda: a > 5)
def my_loop():
    global a

    a = a - 1
    print(a)


my_loop()
