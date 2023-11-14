from mill.factory import factory


# also testing no argument/non-call
@factory
class A:
    x: int
    y: str

    def __init__(self, x: int, y: str):
        self.x = x
        self.y = y


def test_base():
    a = A()
    assert isinstance(a.x, int) and a.x != 0
    assert isinstance(a.y, str) and a.y != ""


def test_overrides():
    a = A(x="a")
    assert isinstance(a.x, str) and a.x == "a"
    assert isinstance(a.y, str) and a.y != ""
