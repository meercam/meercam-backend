from dataclasses import dataclass

@dataclass
class BoundingBox:
    x: float
    y: float
    w: float
    w: float
    color: tuple
    label: str
    def __init__(self, x, y, w, h, color, label):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.label = label
    def __iter__(self):
        return iter((self.x, self.y, self.w, self.h, self.color))
    