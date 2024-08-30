class Foo:
    def __init__(self):
        print(self.__class__.__name__)


class Bar(Foo):
    def __init__(self):
        super().__init__()


x = Foo()
y = Bar()
x.bingbang = 10
print(x.bingbang)
