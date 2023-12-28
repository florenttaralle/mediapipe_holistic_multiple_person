import attrs
from typing import List
# ########################################################
from .pose import BodyPose, FacePose, HandPose
from .holistic_part import HolisticPart
# ########################################################


@attrs.define
class HolisticDetection:
    body:       HolisticPart
    face:       HolisticPart
    left_hand:  HolisticPart
    right_hand: HolisticPart
    # ########################################################

    @property
    def parts(self) -> List[HolisticPart]:
        return [self.body, self.face, self.left_hand, self.right_hand]
    # ########################################################

    def serialize(self):
        return {
            "body": self.body.serialize(),
            "face": self.face.serialize(),
            "left_hand": self.left_hand.serialize(),
            "right_hand": self.right_hand.serialize(),
        }
    # ########################################################
    
    @classmethod
    def deserialize(cls, obj):
        return cls(
            HolisticPart.deserialize(obj["body"], BodyPose),
            HolisticPart.deserialize(obj["face"], FacePose),
            HolisticPart.deserialize(obj["left_hand"], HandPose),
            HolisticPart.deserialize(obj["right_hand"], HandPose),
        )
    # ########################################################

    def draw(self, bgr_frame):
        for part in self.parts:
            if part.rbbox is not None:
                part.bbox.draw(bgr_frame, (255, 0, 0), 2)
                part.rbbox.draw(bgr_frame, (255, 255, 255), 1)
            if part.pose is not None:
                part.pose.draw_links(bgr_frame, (255, 255, 255))
                part.pose.draw_points(bgr_frame, 1)
    # ########################################################
