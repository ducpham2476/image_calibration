
from tracking import Tracking as module
import cv2
from random import randint


def center(box):
    cent = ((int(box[0] + box[2] / 2)), (int(box[1] + box[3] / 2)))
    return cent

def multi_create(bboxes, frame):
    cv2.legacy.TrackerCSRT_create()

    # Create MultiTracker object
    multiTracker = cv2.legacy.MultiTracker_create()

    for bbox in bboxes:
        multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, bbox)

    return multiTracker


def track(frame, multiTracker, bboxes):
    pre_centroi, lost_y, multiTracker = (module.module(frame, multiTracker, bboxes))
    return pre_centroi, lost_y, multiTracker