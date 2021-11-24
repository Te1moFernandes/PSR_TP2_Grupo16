#!/usr/bin/python3
import argparse

import cv2
import numpy as np
from colorama import *
import sys
import json
import color_segmenter


def change_color(x):
    global windowname
    #condition to change color if trackbar value is greater than 127
    if cv2.getTrackbarPos('Red_max', windowname) < cv2.getTrackbarPos('Red_min', windowname):
        cv2.setTrackbarPos('Red_max', windowname, cv2.getTrackbarPos('Red_min', windowname))
    if cv2.getTrackbarPos('Blue_max', windowname) < cv2.getTrackbarPos('Blue_min', windowname):
        cv2.setTrackbarPos('Blue_max', windowname, cv2.getTrackbarPos('Blue_min', windowname))
    if cv2.getTrackbarPos('Green_max', windowname) < cv2.getTrackbarPos('Green_min', windowname):
        cv2.setTrackbarPos('Green_max', windowname, cv2.getTrackbarPos('Green_min', windowname))

def change_color_b_min(x):
    if cv2.getTrackbarPos('Blue_max', windowname) < cv2.getTrackbarPos('Blue_min', windowname):
        cv2.setTrackbarPos('Blue_min',windowname,cv2.getTrackbarPos('Blue_max', windowname))
def write_to_file(data):
    global windowname
    data['limits']['R']['max'] = cv2.getTrackbarPos('Red_max',windowname)
    data['limits']['R']['min'] = cv2.getTrackbarPos('Red_min',windowname)
    data['limits']['G']['max'] = cv2.getTrackbarPos('Green_max',windowname)
    data['limits']['G']['min'] = cv2.getTrackbarPos('Green_min',windowname)
    data['limits']['B']['max'] = cv2.getTrackbarPos('Blue_max',windowname)
    data['limits']['B']['min'] = cv2.getTrackbarPos('Blue_min',windowname)
    print("Escreveu as seguintes configurações:")
    print(data)
    with open('limits.json', 'w') as outfile:
        json.dump(data, outfile)


def main():
    global windowname, color, width
    parser = argparse.ArgumentParser(description='PSR argparse example.')
    parser.add_argument('-j', '--json', default='limits.json', help="Full path to json file.")
    args = vars(parser.parse_args())
    print(args['json'])
    try:
        f = open(args['json'], )
        print("gets f")
        data = json.load(f)
        print(data)
    except:
        print(Fore.RED + "Could not read file as json\nClosing program..." + Style.RESET_ALL)
        sys.exit(1)

    cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Red_max', windowname, data['limits']['R']['max'], 255, change_color)
    cv2.createTrackbar('Red_min', windowname, data['limits']['R']['min'], 255, change_color)
    cv2.createTrackbar('Green_max', windowname, data['limits']['G']['max'], 255, change_color)
    cv2.createTrackbar('Green_min', windowname, data['limits']['G']['min'], 255, change_color)
    cv2.createTrackbar('Blue_max', windowname, data['limits']['B']['max'], 255, change_color)
    cv2.createTrackbar('Bluemin', windowname, data['limits']['B']['min'], 255, change_color_b_min)

    video = cv2.VideoCapture(0)

    img_1 = np.zeros([int(video.get(4)), int(video.get(3)), 3], dtype=np.uint8)
    img_1.fill(255)
    cv2.imshow("canvas",img_1)
    pos_1=()
    while True:
        ret, frame = video.read()
        cv2.imshow(windowname, frame)
        ret, cX, cY = color_segmenter.segment(data, windowname, frame)
        if ret:
            if len(pos_1):
                cv2.line(img_1, pos_1, (int(cX),int(cY)), color, width,-1)
                cv2.imshow("canvas",img_1)
            pos_1=(int(cX),int(cY))
        key = cv2.waitKey(1)
        # the 'q' button is set as the quitting button and w writes thresholds to file
        if key == ord('q'):
            break
        elif key == ord('w'):
            print("writes")
            write_to_file(data)
        elif key == ord('+'):
            if width<16:
                width+=2
        elif key == ord('-'):
            if width>2:
                width-=2
        elif key == ord('r'):
            color=(0,0,255)
        elif key == ord('b'):
            color=(255,0,0)
        elif key == ord('g'):
            color=(0,255,0)
        elif key == ord('c'):
            img_1.fill(255)
            cv2.imshow("canvas",img_1)

        # After the loop release the cap object
    video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


windowname = 'frame'
color=(255,0,0)
width=2

if __name__ == '__main__':
    main()
