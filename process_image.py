import numpy as np, cv2
import argparse as ap
from src.holistic_detector import HolisticDetector

parser = ap.ArgumentParser()
parser.add_argument('input_image')
parser.add_argument('output_path')
parser.add_argument('-c', '--complexity', type=int, choices={0, 1, 2}, default=1)
parser.add_argument('-r', '--refine_face', type=bool, default=True)
args = parser.parse_args()

if args.complexity in {0, 2}:
  HolisticDetector.download_pose_landmark(args.complexity)

detector = HolisticDetector(
  'data/mp_pipelines/pose_detection_cpu.pbtxt',
  'data/mp_pipelines/holistic_custom.pbtxt',
  args.complexity, args.refine_face
)

bgr_frame = cv2.imread(args.input_image)
detections = detector(bgr_frame, True)

for detection in detections:
    detection.draw(bgr_frame)

cv2.imwrite(args.output_path, bgr_frame)
