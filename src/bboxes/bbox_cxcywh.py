from .bbox_base import BboxBase

class Bbox_cxcywh(BboxBase):
    def __init__(self, cx, cy, w, h, normalised):
        # nothing to do here, only for code completion
        pass 

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} cx:{self.cx} cy:{self.cy} w:{self.w} h:{self.h} n:{self.normalised}>"

    @classmethod
    def from_bbox(cls, other: BboxBase): return cls(other.cx, other.cy, other.w, other.h, other.normalised)

    @property
    def cx(self): return self[0]
    @cx.setter
    def cx(self, cx): self[0] = cx

    @property
    def cy(self): return self[1]
    @cy.setter
    def cy(self, cy): self[1] = cy

    @property
    def w(self): return self[2]
    @w.setter
    def w(self, w): self[2] = w

    @property
    def h(self): return self[3]
    @h.setter
    def h(self, h): self[3] = h

    @property
    def x0(self): return self.cx - self.w / 2
    @property
    def y0(self): return self.cy - self.h / 2
    @property
    def x1(self): return self.cx + self.w / 2
    @property
    def y1(self): return self.cy + self.h / 2
