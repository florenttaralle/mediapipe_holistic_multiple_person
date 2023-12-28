import numpy as np, cv2, json, os
import argparse as ap
from glob import glob
from src.holistic_detector import HolisticDetector
from tqdm import tqdm
from queue import Queue
from contextlib import contextmanager
from concurrent.futures import wait, ThreadPoolExecutor, FIRST_COMPLETED

parser = ap.ArgumentParser()
parser.add_argument('input_image_pattern')
parser.add_argument('-c', '--complexity', type=int, choices={0, 1, 2}, default=1)
parser.add_argument('-r', '--refine_face', type=bool, default=True)
parser.add_argument('-w', '--workers', type=int, default=1)
parser.add_argument('-m', '--models', type=int, default=1)
args = parser.parse_args()

assert args.workers >= args.models, 'You are wasting models.'

if args.complexity in {0, 2}:
    HolisticDetector.download_pose_landmark(args.complexity)

# Model Pool 
modelPool = Queue()
for _ in range(args.models):
    detector = HolisticDetector(
        'data/mp_pipelines/pose_detection_cpu.pbtxt',
        'data/mp_pipelines/holistic_custom.pbtxt',
        args.complexity, args.refine_face
    )
    modelPool.put(detector)
    
# Auto Pull/Put Model Context
@contextmanager
def getModel():
    detector = modelPool.get()
    try:
        yield detector
    finally:
        modelPool.put(detector)


def process(image_path: str) -> int:
    bgr_frame = cv2.imread(image_path)
    with getModel() as detector:
        detections = detector(bgr_frame, True)
    serialized = {
        'width': bgr_frame.shape[1],
        'height': bgr_frame.shape[0],
        'detections': [
            detection.serialize()
            for detection in detections
        ]
    }
    json_path = os.path.splitext(image_path)[0] + '.json'
    with open(json_path, 'w') as json_file:
        json.dump(serialized, json_file, indent=2)
    return len(detections)


image_pathes = glob(args.input_image_pattern, recursive=True)
print('%d image files found.' % len(image_pathes))

with ThreadPoolExecutor(max_workers=args.workers) as executor:
    with tqdm(total=len(image_pathes)) as pbar:    
        nb_detection = 0
        futures = set([
            executor.submit(process, image_pathes.pop())
            for _ in range(min(len(image_pathes), args.workers))
        ])
        while len(futures) or len(image_pathes):
            done, futures = wait(futures, return_when=FIRST_COMPLETED)
            pbar.update(len(done))
            for future in done:
                nb_detection += future.result()
            futures.update(set([
                executor.submit(process, image_pathes.pop())
                for _ in range(min(len(done), len(image_pathes)))    
            ]))

print('%d detections.' % nb_detection)
