from circle import Circle
import math

def test_small():
    c = Circle(3)
    assert(round(c.circumference(), 1) == 18.8)
    assert(round(c.area(), 1) == 28.3)

def test_big():
    c = Circle(236)
    assert(round(c.circumference(), 1) == round(2 * math.pi * 236, 1))
    assert(round(c.area(), 1) == round(math.pi * 236 * 236,1))

def test_really_small():
    c = Circle(1)
    assert(round(c.circumference(), 1) == round(2 * math.pi * 1, 1))
    assert(round(c.area(), 1) == round(math.pi * 1 * 1,1))