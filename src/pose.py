import numpy as np, cv2, attrs
from typing import List
import mediapipe as mp
from .landmark import Landmark


@attrs.define
class Pose:
    landmarks:  List[Landmark]

    def draw_points(self, frame, radius, color=None, thickness=None):
        for lm in self.landmarks:
            lm.draw(frame, radius, color, thickness)

    def draw_links(self, frame, links, color, thickness=None):
        h, w = frame.shape[:2]
        for (id0, id1) in links:
            p0 = tuple(self.landmarks[id0].point.denormalise(w, h).astype(int))
            p1 = tuple(self.landmarks[id1].point.denormalise(w, h).astype(int))
            cv2.line(frame, p0, p1, color, thickness)

    @classmethod
    def from_mp(cls, mp_landmarks):
        if mp_landmarks:
            return cls([Landmark.from_mp(lm) for lm in mp_landmarks.landmark])
        else:
            return None
    
    def serialize(self):
        return [lm.serialize() for lm in self.landmarks]
    @classmethod
    def deserialize(cls, obj):
        return cls([Landmark.deserialize(slm) for slm in obj])


class BodyPose(Pose):
    def draw_links(self, frame, color, thickness=None):
        links = mp.solutions.pose.POSE_CONNECTIONS
        Pose.draw_links(self, frame, links, color, thickness)

class HeadPose(Pose):
    def draw_links(self, frame, color, thickness=None):
        links = np.array(list(mp.solutions.pose.POSE_CONNECTIONS))
        links = links[np.all(links < 11, 1)]
        Pose.draw_links(self, frame, links, color, thickness)

class FacePose(Pose):
    def draw_links(self, frame, color, thickness=None):
        links = mp.solutions.face_mesh.FACEMESH_TESSELATION
        Pose.draw_links(self, frame, links, color, thickness)

class HandPose(Pose):
    def draw_links(self, frame, color, thickness=None):
        links = mp.solutions.hands.HAND_CONNECTIONS
        Pose.draw_links(self, frame, links, color, thickness)

