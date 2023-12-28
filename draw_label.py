import numpy as np, cv2, json, os
import argparse as ap
from src.holistic_detection import HolisticDetection


parser = ap.ArgumentParser()
parser.add_argument('input_image')
parser.add_argument('input_label')
parser.add_argument('output_image')
args = parser.parse_args()

assert os.path.exists(args.input_image), f'Input Image file not Found: {args.input_image}'
assert os.path.exists(args.input_label), f'Input Label file not Found: {args.input_label}'

# load image
bgr_frame = cv2.imread(args.input_image)
assert bgr_frame is not None, f'Invalid Image file: {args.input_image}'

# load label data
with open(args.input_label, 'r') as json_file:
    label = json.load(json_file)
# parse label data
detections = [
    HolisticDetection.deserialize(detection_label)
    for detection_label in label["detections"]
]

# draw
for detection in detections:
    detection.draw(bgr_frame)

# export result
cv2.imwrite(args.output_image, bgr_frame)
print("> file://%s" % os.path.realpath(args.output_image))
