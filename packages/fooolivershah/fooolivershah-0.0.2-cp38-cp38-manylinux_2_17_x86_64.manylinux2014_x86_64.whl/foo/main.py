from foo import one
from foo.bar import two


def do_stuff(a, b):
    return one.test1.add1(a), two.test2.add2(b)
