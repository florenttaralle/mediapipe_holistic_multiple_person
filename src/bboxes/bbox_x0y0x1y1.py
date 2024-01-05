from .bbox_base import BboxBase

class Bbox_x0y0x1y1(BboxBase):
    def __init__(self, x0, y0, x1, y1, normalised):
        # nothing to do here, only for code completion
        pass 

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} x0:{self.x0} y0:{self.y0} x1:{self.x1} y1:{self.y1} n:{self.normalised}>"

    @classmethod
    def from_bbox(cls, other: BboxBase): return cls(other.x0, other.y0, other.x1, other.y1, other.normalised)

    @property
    def x0(self): return self[0]
    @x0.setter
    def x0(self, x0): self[0] = x0

    @property
    def y0(self): return self[1]
    @y0.setter
    def y0(self, y0): self[1] = y0

    @property
    def x1(self): return self[2]
    @x1.setter
    def x1(self, x1): self[2] = x1

    @property
    def y1(self): return self[3]
    @y1.setter
    def y1(self, y1): self[3] = y1

    @property
    def w(self): return self.x1 - self.x0 + (1 if not self.normalised else 0)
    @property
    def h(self): return self.y1 - self.y0 + (1 if not self.normalised else 0)
    @property
    def cx(self): return (self.x0 + self.x1) / 2
    @property
    def cy(self): return (self.y0 + self.y1) / 2