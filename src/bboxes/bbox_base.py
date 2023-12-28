from abc import ABC, abstractproperty, abstractclassmethod
import numpy as np, cv2
from ..point import Point


class BboxBase(np.ndarray, ABC):
    normalised: bool

    def __new__(cls, p0, p1, p2, p3, normalised: bool=False):
        obj = np.array((p0, p1, p2, p3)).view(cls)
        obj.normalised = normalised
        return obj 
    
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

    def draw(self, frame, color, thickness=1):
        h, w    = frame.shape[:2]
        p0      = Point(self.x0, self.y0, self.normalised).denormalise(w, h)
        p0      = tuple(p0.astype(int))
        p1      = Point(self.x1, self.y1, self.normalised).denormalise(w, h)
        p1      = tuple(p1.astype(int))
        cv2.rectangle(frame, p0, p1, color, thickness)

    def serialize(self):
        return {
            "x0":            self.x0, 
            "y0":            self.y0, 
            "w":            self.w,
            "h":            self.h,
            "normalised":   self.normalised
        }
    @classmethod
    def deserialize(cls, obj):
        from .bbox_x0y0wh import Bbox_x0y0wh # avoid circular import
        return cls.from_bbox(Bbox_x0y0wh(**obj))

    @abstractclassmethod
    def from_bbox(cls, other): ...