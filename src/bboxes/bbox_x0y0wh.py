from .bbox_base import BboxBase

class Bbox_x0y0wh(BboxBase):
    def __init__(self, x0, y0, w, h, normalised: bool=False):
        # nothing to do here, only for code completion
        pass 

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} x0:{self.x0} y0:{self.y0} w:{self.w} h:{self.h}>"

    @classmethod
    def from_bbox(cls, other: BboxBase): return cls(other.x0, other.y0, other.w, other.h)

    @property
    def x0(self): return self[0]
    @x0.setter
    def x0(self, x0): self[0] = x0

    @property
    def y0(self): return self[1]
    @y0.setter
    def y0(self, y0): self[1] = y0

    @property
    def w(self): return self[2]
    @w.setter
    def w(self, w): self[2] = w

    @property
    def h(self): return self[3]
    @h.setter
    def h(self, h): self[3] = h

    @property
    def x1(self): return self.x0 + self.w - (1 if not self.normalised else 0)
    @property
    def y1(self): return self.y0 + self.h - (1 if not self.normalised else 0)
    @property
    def cx(self): return (self.x0 + self.x1) / 2
    @property
    def cy(self): return (self.y0 + self.y1) / 2