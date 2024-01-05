import numpy as np, cv2, os
from typing import Optional, List
from mediapipe.python.solution_base import SolutionBase
from mediapipe.python.solutions import download_utils
# ########################################################
from .holistic_detection import HolisticDetection, HolisticPart
from .rbbox import RBbox
from .pose import BodyPose, HeadPose, FacePose, HandPose
# ########################################################


class HolisticDetector:
    def __init__(self, primary_pbtxt: str, secondary_pbtxt: str,
            model_complexity: int=0, refine_face_landmarks: bool=True):
        assert os.path.exists(primary_pbtxt), f'Missing Primary PbTxt: {primary_pbtxt}'
        self.primary_pbtxt = primary_pbtxt
        assert os.path.exists(secondary_pbtxt), f'Missing Secondary PbTxt: {secondary_pbtxt}'
        self.secondary_pbtxt = secondary_pbtxt

        # load primary detector
        with open(self.primary_pbtxt) as txt_file:
            graph_config = txt_file.read()
        self.primary_detector = SolutionBase(graph_config=graph_config)

        # Secondary Detector
        with open(self.secondary_pbtxt) as txt_file:
            graph_config = txt_file.read()
        self.secondary_detector = SolutionBase(
            graph_config = graph_config,
            side_inputs = {
                'model_complexity':       model_complexity,    # 0, 1, 2
                'refine_face_landmarks':  refine_face_landmarks, # True/False
            }
        )
    # ########################################################
        
    @staticmethod
    def download_pose_landmark(model_complexity: int):
        # Download Pose Landmark detectors if not available (depending on complexity)
        if model_complexity == 0:
            download_utils.download_oss_model('mediapipe/modules/pose_landmark/pose_landmark_lite.tflite')
        if model_complexity == 2:
            download_utils.download_oss_model('mediapipe/modules/pose_landmark/pose_landmark_heavy.tflite')
    # ########################################################

    @staticmethod
    def to_rbbox(mp_rbbox) -> Optional[RBbox]:
        if mp_rbbox is not None:
            return RBbox(
                mp_rbbox.x_center, mp_rbbox.y_center, 
                mp_rbbox.width, mp_rbbox.height, 
                mp_rbbox.rotation, True)
        else:
            return None
    # ########################################################

    def __call__(self, frame: np.array, is_bgr: bool=True) -> List[HolisticDetection]:
        if is_bgr:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        else:
            rgb_frame = frame

        # multiple ppl detection
        primary_result = self.primary_detector.process({"image": rgb_frame})
        # per-ppl poses 
        if primary_result.detections is not None:
            detections = [
                self._secondary(rgb_frame, pose_detection)
                for pose_detection in primary_result.detections
            ]
        else:
            detections = []

        return detections
    # ########################################################

    def _secondary(self, rgb_frame, pose_detection) -> HolisticDetection:
        secondary_result = self.secondary_detector.process({
            'image':          rgb_frame,
            'pose_detection': pose_detection
        })
        # load bboxes
        body_rbbox  = self.to_rbbox(
            secondary_result.pose_rect_from_landmarks or
            secondary_result.pose_rect_from_detection
        )
        head_rbbox  = self.to_rbbox(secondary_result.face_roi_from_pose)
        face_rbbox  = self.to_rbbox(secondary_result.face_rect_from_landmarks)
        lhand_rbbox = self.to_rbbox(secondary_result.left_hand_roi)
        rhand_rbbox = self.to_rbbox(secondary_result.right_hand_roi)
        # load poses (or None)
        body_pose   = BodyPose.from_mp(secondary_result.pose_landmarks)
        head_pose   = HeadPose(body_pose.landmarks[:11]) if body_pose is not None else None
        face_pose   = FacePose.from_mp(secondary_result.face_landmarks)
        lhand_pose  = HandPose.from_mp(secondary_result.left_hand_landmarks)
        rhand_pose  = HandPose.from_mp(secondary_result.right_hand_landmarks)

        return HolisticDetection(
            HolisticPart(body_rbbox, body_pose),
            HolisticPart(head_rbbox, head_pose),
            HolisticPart(face_rbbox, face_pose),
            HolisticPart(lhand_rbbox, lhand_pose),
            HolisticPart(rhand_rbbox, rhand_pose)
        )
    # ########################################################
    