import numpy as np, cv2
import attrs
from .bboxes import Bbox_x0y0x1y1

@attrs.define
class RBbox:
    cx:         float
    cy:         float
    w:          float
    h:          float
    r:          float
    normalised: bool = False

    def copy(self):
        return attrs.evolve(self)

    def to_bbox(self) -> Bbox_x0y0x1y1:
        corners = self.corners()
        return Bbox_x0y0x1y1(*corners.min(0), *corners.max(0), self.normalised)

    def denormalise(self, w, h):
        if not self.normalised:
            return self.copy()
        else:
            return RBbox(
                self.cx * w, self.cy * h,
                self.w * w, self.h * h,
                self.r, False
            )

    def normalise(self, w, h):
        if self.normalised:
            return self.copy()
        else:
            return RBbox(
                self.cx / w, self.cy / h,
                self.w / w, self.h / h,
                self.r, True
            )

    def corners(self) -> np.ndarray:
        x0      = self.cx - (self.w / 2)
        y0      = self.cy - (self.h / 2)
        x1      = self.cx + (self.w / 2)
        y1      = self.cy + (self.h / 2)

        corners = np.array([(x0, y0), (x1, y0), (x1, y1), (x0, y1)])
        Mr      = cv2.getRotationMatrix2D((self.cx, self.cy), self.r, 1.0)

        corners = np.reshape(corners, (4, 1, 2))
        corners = cv2.transform(corners, Mr)
        corners = np.reshape(corners, (4, 2))
        return corners

    def draw(self, frame, color, thickness=None):
        h, w    = frame.shape[:2]
        corners = self.denormalise(w, h).corners().astype(int)
        cv2.polylines(frame, [corners], True, color, thickness or 1)

    def serialize(self):
        return attrs.asdict(self)
    @classmethod
    def deserialize(cls, obj):
        return cls(**obj)
