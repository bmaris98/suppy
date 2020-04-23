from suppy.utils.borg import Borg

class TestBorg:

    def test_one(self):
        f1 = First(1)
        assert f1.a == 1
        
        f2 = First(2)
        assert f1.a == 2 and f2.a == 2

        s1 = Second(1)
        assert f1.a == 2 and f2.a == 2
        assert s1.a == 1

        s2 = Second(3)
        assert s1.a == 3 and s2.a == 3
        assert f1.a == 2 and f2.a == 2

class First(Borg):
    _shared_state = {}
    def __init__(self, a):
        Borg.__init__(self)
        self._a = a

    @property
    def a(self):
        return self._a

class Second(Borg):
    _shared_state = {}
    def __init__(self, a):
        Borg.__init__(self)
        self._a = a

    @property
    def a(self):
        return self._a