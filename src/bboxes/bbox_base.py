from abc import ABC, abstractproperty, abstractclassmethod, abstractmethod
import numpy as np, cv2
from ..point import Point


class BboxBase(np.ndarray, ABC):
    normalised: bool

    def __new__(cls, p0, p1, p2, p3, normalised):
        obj = np.array((p0, p1, p2, p3)).view(cls)
        obj.normalised = normalised
        return obj 
    
    @abstractclassmethod
    def from_bbox(cls, other): ...

    def denormalise(self, width: int, height: int): 
        assert self.normalised
        return self.__class__(*list(self * [width, height, width, height]), False)

    def normalise(self, width: int, height: int): 
        assert not self.normalised
        return self.__class__(*list(self / [width, height, width, height]), True)

    @abstractproperty
    def x0(self): ...
    @abstractproperty
    def y0(self): ...
    @abstractproperty
    def w(self): ...
    @abstractproperty
    def h(self): ...
    @abstractproperty
    def x1(self): ...
    @abstractproperty
    def y1(self): ...
    @abstractproperty
    def cx(self): ...
    @abstractproperty
    def cy(self): ...

    @property
    def area(self): return self.w * self.h

    @property
    def tl(self): return Point(self.x0, self.y0, self.normalised)
    @property
    def tr(self): return Point(self.x1, self.y0, self.normalised)
    @property
    def bl(self): return Point(self.x0, self.y1, self.normalised)
    @property
    def br(self): return Point(self.x1, self.y1, self.normalised)


    def draw(self, frame, color, thickness=1):
        h, w    = frame.shape[:2]
        bbox = self.denormalise(w, h) if self.normalised else self
        p0      = tuple(bbox.tl.astype(int))
        p1      = tuple(bbox.br.astype(int)) 
        cv2.rectangle(frame, p0, p1, color, thickness)


    def serialize(self):
        return {
            "x0":           self.x0, 
            "y0":           self.y0, 
            "w":            self.w,
            "h":            self.h,
            "normalised":   self.normalised
        }
    
    @classmethod
    def deserialize(cls, obj):
        from .bbox_x0y0wh import Bbox_x0y0wh # avoid circular import
        return cls.from_bbox(Bbox_x0y0wh(**obj))

