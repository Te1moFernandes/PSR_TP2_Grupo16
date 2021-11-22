#!/usr/bin/python3
# import the opencv library
import cv2
import json
import sys
from colorama import *
# define a video capture object

#callback para as trackbars

def change_color(x):
        #condition to change color if trackbar value is greater than 127
    if cv2.getTrackbarPos('Red_max','frame')<cv2.getTrackbarPos('Red_min','frame'):
        cv2.setTrackbarPos('Red_max','frame',cv2.getTrackbarPos('Red_min','frame'))
    if cv2.getTrackbarPos('Blue_max','frame')<cv2.getTrackbarPos('Blue_min','frame'):
        cv2.setTrackbarPos('Blue_max','frame',cv2.getTrackbarPos('Blue_min','frame'))
    if cv2.getTrackbarPos('Green_max','frame')<cv2.getTrackbarPos('Green_min','frame'):
        cv2.setTrackbarPos('Green_max','frame',cv2.getTrackbarPos('Green_min','frame'))


def write_to_file():
    global data
    data['limits']['R']['max'] = cv2.getTrackbarPos('Red_max','frame')
    data['limits']['R']['min'] = cv2.getTrackbarPos('Red_min','frame')
    data['limits']['G']['max'] = cv2.getTrackbarPos('Green_max','frame')
    data['limits']['G']['min'] = cv2.getTrackbarPos('Green_min','frame')
    data['limits']['B']['max'] = cv2.getTrackbarPos('Blue_max','frame')
    data['limits']['B']['min'] = cv2.getTrackbarPos('Blue_min','frame')
    print(data)
    with open('limits.json', 'w') as outfile:
        json.dump(data, outfile)


def limit_image(B, G, R, final_threshred=None):
    _, thresh1 = cv2.threshold(B,cv2.getTrackbarPos('Blue_max','frame'),255,cv2.THRESH_BINARY_INV)
    _, thresh2 = cv2.threshold(B,cv2.getTrackbarPos('Blue_min','frame'),255,cv2.THRESH_BINARY)
    _, thresh3 = cv2.threshold(G,cv2.getTrackbarPos('Red_max','frame'),255,cv2.THRESH_BINARY_INV)
    _, thresh4 = cv2.threshold(G,cv2.getTrackbarPos('Red_min','frame'),255,cv2.THRESH_BINARY)
    _, thresh5 = cv2.threshold(R,cv2.getTrackbarPos('Green_max','frame'),255,cv2.THRESH_BINARY_INV)
    _, thresh6 = cv2.threshold(R,cv2.getTrackbarPos('Green_min','frame'),255,cv2.THRESH_BINARY)

    thresh_blue=cv2.bitwise_and(thresh1,thresh2)
    thresh_red=cv2.bitwise_and(thresh3,thresh4)
    thresh_green=cv2.bitwise_and(thresh5,thresh6)
    final_thresh=cv2.bitwise_and(thresh_blue,thresh_green)
    cv2.imshow('image_blue',thresh_blue)
    cv2.imshow('image_green',thresh_green)
    cv2.imshow('image_red',thresh_red)
    final_thresh=cv2.bitwise_and(final_thresh,thresh_red)
    cv2.imshow('image',final_thresh)
    return final_thresh

def main(data):
    vid = cv2.VideoCapture(0)
    windowname = 'frame'
    cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Red_max',windowname,data['limits']['R']['max'],255,change_color)
    cv2.createTrackbar('Red_min',windowname,data['limits']['R']['min'],255,change_color)
    cv2.createTrackbar('Green_max',windowname,data['limits']['G']['max'],255,change_color)
    cv2.createTrackbar('Green_min',windowname,data['limits']['G']['min'],255,change_color)
    cv2.createTrackbar('Blue_max',windowname,data['limits']['B']['max'],255,change_color)
    cv2.createTrackbar('Blue_min',windowname,data['limits']['B']['min'],255,change_color)

    while True:
        
        # Capture the video frame by frame
        ret, frame = vid.read()
        (B, G, R) = cv2.split(frame)
        img_w_thresh= limit_image(B, G, R)
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # the 'q' button is set as the quitting button and w writes thresholds to file
        key=cv2.waitKey(1)
        if key == ord('q'):
            break
        elif key == ord('w'):
            print("writes")
            write_to_file()


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()
