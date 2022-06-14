from __future__ import print_function
from re import A
import sys
import cv2
from random import randint
import imutils
from matplotlib.pyplot import box
import numpy as np
import math
import time

#---------------------------Variable-------------------------#

im_lower = np.array([20, 75, 75], dtype="uint8")
im_upper = np.array([35, 255, 255], dtype="uint8")
kernel = np.ones((3, 3), np.uint8)

trackerTypes = ['BOOSTING', 'MIL', 'KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE', 'CSRT']

check = False

# quit if unable to read the video file

#Center of previous boxes
# pre_centroid = [(478, 595), (1163, 624), (300, 857), (1222, 907)]
pre_centroid = []

# bboxes = [(442, 542, 110, 106), (1124, 570, 116, 108), (270, 804, 98, 106), (1176, 854, 130, 106)]
img_array = []

#waitKey
count = 0
aa = 1

#store lost landmark's name
lost_box_store = []

#store order of landmark
num = [0, 1, 2, 3]

#for fixing tracking area
# bboxes_num_def = dict(zip(num, bboxes))

lost_box = None
average_dist = -2

#---------------------------Pre_process-------------------------#


def landmark_recog(img):
    img_copy = img.copy()
    im_hsv = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
    im_mask = cv2.inRange(im_hsv, im_lower, im_upper)
    im_mask = cv2.morphologyEx(im_mask, cv2.MORPH_OPEN, kernel)
    cur_cnt, _ = cv2.findContours(im_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    try:
        c = cv2.contourArea(max(cur_cnt, key = cv2.contourArea))
    except:
        c = 100
    # if(c != 100):
    #     print(c)
    #     cv2.imshow('A', img_copy)
    #     cv2.waitKey()
    return c

#Return center of tracking box
def center(box):
    cent = ((int(box[0] + box[2] / 2)), (int(box[1] + box[3] / 2)))
    if(box[1] == 0 and box[0] == 0):
        cent = (0, 0)
    return cent
    
def module(frame, multiTracker, bboxes):

    global pre_centroid
    global lost_box
    global count 
    global boxes
    global average_dist

    height, width, layers = frame.shape
    size = (width,height)
    if(not count):
        for box in bboxes:
            pre_centroid.append(center(box))

    #recognize and caculate contourArea
    colors = []
    for i in range(4):
        colors.append((randint(0, 25), randint(0, 25), randint(0, 25)))
    # Specify the tracker type

    # Process video and track objects
    start = time.time()
    print("---------------------\n")
    cur_centroid = []
    

    # creat new track list if an object was disappeared
    # try:

    if(average_dist > -1):
        #if lose a box
        if(lost_box != None):
            # multiTracker = cv2.legacy.MultiTracker_create()
            # for i, bbox in enumerate(boxes):
            #     try:
            #         if(num[i] == lost_box):
            #             cv2.waitKey()
            #             continue
            #         multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, bbox)
            #     except:
            #         None
            lost_box_store.append(lost_box)
            lost_box = None
    # except:
    #   None

    # get updated location of objects in subsequent frames
    success, boxes = multiTracker.update(frame)


    lost_yellow = []
    # draw tracked objects
    # check if object has [0, 0, 0, 0] then remove from track list
    for i, newbox in enumerate(boxes):
        for x in range(len(newbox)):
            if(newbox[x] < 0):
                newbox[x] = 0
        p1 = (int(newbox[0]), int(newbox[1]))
        p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
        cv2.rectangle(frame, p1, p2, colors[i], 2, 1)
        if(newbox[0] == 0 and newbox[1] == 0):
            if(num[i] != lost_box):
                lost_box = num[i]
            continue 
        cur_centroid.append(center(newbox))
        #cut tracking box and find if yellow landmark in it?
        cut = frame[p1[1] : p2[1], p1[0] : p2[0]]
        if(landmark_recog(cut) < 150):
            print("!!!!!!!!!!!!")
            lost_yellow.append(num[i])
            if(num[i] != 1):
                cv2.waitKey()
            # if(num[i] != lost_box):
            #     lost_box = num[i]
    

    # check if an object was over another object then remove it
    move = []
    def foward():
        for i, x in enumerate(cur_centroid):
            for y in cur_centroid:
                global lost_box
                if(0 < math.dist(x, y) < 20):
                    if(lost_box != i):
                        lost_box = i
                        move.append(int(dist[i]))
                        return None
    foward()

    # calculate distance between objects 
    dist = []
    temp_pre_centroid = pre_centroid.copy()
    temp_pre_centroid = dict(zip(temp_pre_centroid, num))
    #if a box dissapear, remove it from "num"
    # print("!!!", len(cur_centroid))
    if(len(cur_centroid) < len(pre_centroid)):
        if(lost_box != None and not(lost_box in lost_box_store)):
            lost_box_store.append(lost_box)
        # print("!!", lost_box_store)
        # print("!!!", lost_box)
        # print(len(cur_centroid), len(pre_centroid))
        temp_pre_centroid = {key:val for key, val in temp_pre_centroid.items() if val != lost_box_store[-1]}
        num.remove(lost_box_store[-1])
    temp_pre_centroid = list(temp_pre_centroid)
    for i in range(len(temp_pre_centroid)):
        dist.append(int(math.dist(cur_centroid[i], temp_pre_centroid[i])))

    average_dist = int(sum(dist) / len(dist))

    # console print
    # print("Centroid: \n", cur_centroid, "\n", pre_centroid)
    # print("Move: ", move)
    print("Average: ", average_dist)
    print("Lost: ", lost_box)
    try:
        print("Lost_Store: ", lost_box_store)
    except:
        None
    # print("Count: ", count)
    pre_centroid = cur_centroid.copy()
    pre_boxes = boxes.copy()
    # show frame
    # cv2.imshow('MultiTracker', imutils.resize(frame, width=1000))
    # cv2.waitKey(1)
    img_array.append(frame)
    count += 1
    
    # if(count > 20):
    #     aa = 0
    # print("Time: ", time.time() - start)
    # # print("Box", boxes)
    print("Centroid: ", pre_centroid)
    # print("Frame: ", count)

    return cur_centroid, lost_yellow, multiTracker

    # out = cv2.VideoWriter('newest.avi',cv2.VideoWriter_fourcc(*'DIVX'), 10, size)
    
    # for i in range(len(img_array)):
    #     out.write(img_array[i])
    # out.release()
    
