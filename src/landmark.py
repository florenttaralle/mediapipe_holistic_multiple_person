import attrs
from .point import Point
from .utils import score_to_color


@attrs.define
class Landmark:
    point:      Point
    visibility: float

    @classmethod
    def from_mp(cls, mp_lm):
        return cls(
            Point(mp_lm.x, mp_lm.y, True), 
            round(mp_lm.visibility, 2))

    def draw(self, frame, radius, color=None, thickness=None):
        if color is None:
            color = score_to_color(self.visibility)
        self.point.draw(frame, radius, color, thickness)

    def serialize(self):
        return {
            "point": self.point.serialize(), 
            "visibility": self.visibility
        }

    @classmethod
    def deserialize(cls, obj):
        return cls(
            Point.deserialize(obj["point"]),
            obj["visibility"]
        )
