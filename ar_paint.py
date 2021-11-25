#!/usr/bin/python3
import argparse

import cv2
import numpy as np
from colorama import *
import sys
import json
from math import sqrt
from time import ctime


def find_centroid(th):
    ret = False
    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cX = 0
    cY = 0
    connectivity = 4  
    output = cv2.connectedComponentsWithStats(th, connectivity, cv2.CV_32S)
    max_area =- 1
    index = None
    if output[0] <= 1:
        return ret, None, None
    for i in range(1, output[0]):
        if output[2][i, cv2.CC_STAT_AREA] > max_area:
            index = i
            max_area = output[2][i, cv2.CC_STAT_AREA]
            ret = True
    return ret, output[3][index][0], output[3][index][1]


def limit_image(data, frame):
    

    lower_lim = np.array([int(data['limits']['B']['min']), int(data['limits']['G']['min']), int(data['limits']['R']['min'])])
    upper_lim = np.array([int(data['limits']['B']['max']), int(data['limits']['G']['max']), int(data['limits']['R']['max'])])
    
    final_thresh = cv2.inRange(frame, lower_lim, upper_lim)
    cv2.imshow('image', final_thresh)
    
    return final_thresh


def draw_with_mouse_pos(event, x, y, flags, param):
    global pos_1, color, width, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            if not sqrt((pos_1[0]-x)**2+(pos_1[1]-y)**2) > 20:
                cv2.line(param, pos_1, (x, y), color, width)
                cv2.imshow('canvas', param)
        pos_1 = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


def segment(data, windowname, frame):
    img_w_thresh = limit_image(data, frame)
    ret, cX, cY = find_centroid(img_w_thresh)
    # Display the resulting frame
    return ret, cX, cY


def main ():
    global windowname, color, width, pos_1
    use_mouse = False
    parser = argparse.ArgumentParser(description='PSR argparse example.')
    parser.add_argument('-j', '--json', default='limits.json', help="Full path to json file.")
    parser.add_argument('-usp', '--use_shake_prevention', action='store_true', help="If used, shake detection is activated")
    parser.add_argument('-uvab', '--use_video_as_board', action='store_true', help="Draws in the video capture instead of the white canvas")
    args = vars(parser.parse_args())
    try:
        f = open(args['json'], )
        data = json.load(f)
        print(data)
    except :
        print(Fore.RED + "Could not read file as json\nClosing program..." + Style.RESET_ALL)
        sys.exit(1)

    print("Press '+' to increase line width;")
    print("Press '-' to decrease line width;")
    print("Press 'w' to save current drawing;")
    print("Press 'g' to to change line color to green;")
    print("Press 'r' to to change line color to red;")
    print("Press 'b' to to change line color to blue;")
    print("Press 'c' to clear drawing;")
    if args['use_shake_prevention']:
        print("Press 'm' to toggle between mouse drawing and camera centroid drawing;")
    print(Fore.RED+"Press 'q' to quit the program"+Style.RESET_ALL)
    video = cv2.VideoCapture(0)

    img_1 = np.zeros([int(video.get(4)), int(video.get(3)), 3], dtype=np.uint8)
    img_1.fill(255)
    cv2.imshow("canvas", img_1)
    while True:
        ret, frame = video.read()
        cv2.imshow(windowname, frame)
        if not use_mouse:
            ret, cX, cY = segment(data, windowname, frame)
            if ret:
                if len(pos_1):
                        if args['use_shake_prevention'] and sqrt((pos_1[0]-cX)**2+(pos_1[1]-cY)**2)>20:
                            pos_1 = ()
                        if len(pos_1):                    
                            cv2.line(img_1, pos_1, (int(cX), int(cY)), color, width, -1)
                            cv2.imshow("canvas", img_1)
                pos_1 = (int(cX), int(cY))
        key = cv2.waitKey(1)
        # the 'q' button is set as the quitting button and w writes thresholds to file
        if key == ord('q'):
            break
        elif key == ord('w'):
            cv2.imwrite('Drawing_' + ctime().replace(' ', "_") + '.jpg', img_1)
        elif key == ord('+'):
            if width < 16:
                width += 2
        elif key == ord('-'):
            if width > 2:
                width -= 2
        elif key == ord('r'):
            color = (0, 0, 255)
        elif key == ord('b'):
            color = (255, 0, 0)
        elif key == ord('g'):
            color = (0, 255, 0)
        elif key == ord('c'):
            img_1.fill(255)
            cv2.imshow("canvas", img_1)
        elif args['use_shake_prevention'] and key == ord('m'):
            if use_mouse:
                use_mouse = False
            else:
                cv2.setMouseCallback('canvas', draw_with_mouse_pos, img_1)
                use_mouse = True
    # After the loop release the cap object
    video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


windowname = 'frame'
color = (255, 0, 0)
width = 2
pos_1 = ()
drawing = False

if __name__ == '__main__':
    main()
