#!/usr/bin/python3
import argparse

import cv2
import numpy as np
from colorama import *
import sys
import json
import color_segmenter


def change_color(x):
    #condition to change color if trackbar value is greater than 127
    if cv2.getTrackbarPos('Red_max', 'frame', cv2.getTrackbarPos('Red_min', 'frame')):
        cv2.setTrackbarPos('Red_max', 'frame', cv2.getTrackbarPos('Red_min', 'frame'))
    if cv2.getTrackbarPos('Blue_max', 'frame') < cv2.getTrackbarPos('Blue_min', 'frame'):
        cv2.setTrackbarPos('Blue_max', 'frame', cv2.getTrackbarPos('Blue_min', 'frame'))
    if cv2.getTrackbarPos('Green_max', 'frame') < cv2.getTrackbarPos('Green_min', 'frame'):
        cv2.setTrackbarPos('Green_max', 'frame', cv2.getTrackbarPos('Green_min', 'frame'))

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


def main():
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

    img_1 = np.zeros([512, 512, 1], dtype=np.uint8)
    img_1.fill(255)
    windowname = 'frame'
    cv2.namedWindow(windowname, cv2.WINDOW_AUTOSIZE)
    cv2.createTrackbar('Red_max', windowname, data['limits']['R']['max'], 255, change_color)
    cv2.createTrackbar('Red_min', windowname, data['limits']['R']['min'], 255, change_color)
    cv2.createTrackbar('Green_max', windowname, data['limits']['G']['max'], 255, change_color)
    cv2.createTrackbar('Green_min', windowname, data['limits']['G']['min'], 255, change_color)
    cv2.createTrackbar('Blue_max', windowname, data['limits']['B']['max'], 255, change_color)
    cv2.createTrackbar('Blue_min', windowname, data['limits']['B']['min'], 255, change_color)

    video = cv2.VideoCapture(0)
    while True:
        ret, frame = video.read()
        cv2.imshow(windowname, frame)
        thresh = color_segmenter.segment(data, windowname, frame)

        # im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # for c in contours:
        #     M = cv2.moments(c)
        #     cX = int(M["m10"] / M["m00"])
        #     cY = int(M["m01"] / M["m00"])
        #     cv2.circle(video, (cX, cY), 5, (255, 255, 255), -1)
        #     cv2.putText(video, "centroid", (cX - 25, cY - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
        #     cv2.imshow("centroid", video)
        key = cv2.waitKey(1)
        # the 'q' button is set as the quitting button and w writes thresholds to file
        if key == ord('q'):
            break
        elif key == ord('w'):
            print("writes")
            write_to_file()


        # After the loop release the cap object
    video.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
