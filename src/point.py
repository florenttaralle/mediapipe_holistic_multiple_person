import numpy as np, cv2

class Point(np.ndarray):
    normalised: bool

    def __new__(cls, x, y, normalised: bool):
        obj = np.array((x, y)).view(cls)
        obj.normalised = normalised
        return obj

    def __init__(self, x, y, normalised: bool=False):
        # nothing to do here, only for code completion
        pass 

    def __repr__(self) -> str:
        return f"<Point x:{self.x} y:{self.y} n:{self.normalised}>"

    @property
    def x(self): return self[0]
    @x.setter
    def x(self, x): self[0] = x

    @property
    def y(self): return self[1]
    @y.setter
    def y(self, y): self[1] = y

    def draw(self, frame, radius, color, thickness=None):
        h, w        = frame.shape[:2]
        abs_point   = self.denormalise(w, h)
        point       = (int(abs_point.x), int(abs_point.y))
        cv2.circle(frame, point, radius, color, thickness or -1)

    def normalise(self, w, h):
        assert not self.normalised
        return Point(*list(self / [w, h]), True)

    def denormalise(self, w, h):
        assert self.normalised
        return Point(*list(self * [w, h]), False)
        
    def serialize(self):
        return {"x": self.x, "y": self.y, "normalised": self.normalised}

    @classmethod
    def deserialize(cls, obj):
        return cls(**obj)
