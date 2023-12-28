import attrs
from typing import Optional
# ########################################################
from .rbbox import RBbox
from .bboxes import Bbox_x0y0x1y1
from .pose import Pose
# ########################################################


@attrs.define
class HolisticPart:
    rbbox:  Optional[RBbox]
    pose:   Optional[Pose]
    # ########################################################

    @property
    def bbox(self) -> Optional[Bbox_x0y0x1y1]:
        if self.rbbox is not None:
            return self.rbbox.to_bbox()
        else:
            return None
    # ########################################################

    def serialize(self):
        return {
            'rbbox': self.rbbox.serialize() if self.rbbox is not None else None, 
            'bbox': self.bbox.serialize() if self.bbox is not None else None,
            'pose': self.pose.serialize() if self.pose is not None else None,
        }
    # ########################################################
    
    @classmethod
    def deserialize(cls, obj, pose_class=Pose):
        rbbox = RBbox.deserialize(obj['rbbox']) if obj['rbbox'] is not None else None
        pose =  pose_class.deserialize(obj['pose']) if obj['pose'] is not None else None
        return cls(rbbox, pose)
    # ########################################################

