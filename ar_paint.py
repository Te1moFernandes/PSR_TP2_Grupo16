#!/usr/bin/python3
import argparse

import cv2
import numpy as np
from colorama import *
import sys
import json
from math import sqrt


def draw_with_mouse(event, x, y, flags, param):
    pass


def find_centroid(th):
    ret=False
    contours, hierarchy = cv2.findContours(th, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cX=0
    cY=0
    connectivity = 4  
    output = cv2.connectedComponentsWithStats(th, connectivity, cv2.CV_32S)
    max_area=-1
    index=None
    if output[0]<=1:
        return ret, None, None
    for i in range(1,output[0]):
        if output[2][i,cv2.CC_STAT_AREA]>max_area:
            index=i
            max_area=output[2][i,cv2.CC_STAT_AREA]
            ret=True
    return ret, output[3][index][0], output[3][index][1]


def limit_image(data, B, G, R):
    _, thresh1 = cv2.threshold(B, data['limits']['B']['max'], 255, cv2.THRESH_BINARY_INV)
    _, thresh2 = cv2.threshold(B, data['limits']['B']['min'], 255, cv2.THRESH_BINARY)
    _, thresh3 = cv2.threshold(G, data['limits']['R']['max'], 255, cv2.THRESH_BINARY_INV)
    _, thresh4 = cv2.threshold(G, data['limits']['R']['min'], 255, cv2.THRESH_BINARY)
    _, thresh5 = cv2.threshold(R, data['limits']['G']['max'], 255, cv2.THRESH_BINARY_INV)
    _, thresh6 = cv2.threshold(R, data['limits']['G']['min'], 255, cv2.THRESH_BINARY)

    thresh_blue = cv2.bitwise_and(thresh1, thresh2)
    thresh_red = cv2.bitwise_and(thresh3, thresh4)
    thresh_green = cv2.bitwise_and(thresh5, thresh6)
    
    final_thresh = cv2.bitwise_and(thresh_blue, thresh_green)
    final_thresh = cv2.bitwise_and(final_thresh, thresh_red)
    cv2.imshow('image', final_thresh)
    
    return final_thresh

def segment(data, windowname, frame):
    
    B=frame[:,:,0] #blue channel
    G=frame[:,:,1] #green channel
    R=frame[:,:,2] #red channel
    img_w_thresh = limit_image(data, B, G, R)
    ret, cX, cY = find_centroid(img_w_thresh)
    # Display the resulting frame
    return ret, cX, cY

def main():
    global windowname, color, width
    parser = argparse.ArgumentParser(description='PSR argparse example.')
    parser.add_argument('-j', '--json', default='limits.json', help="Full path to json file.")
    parser.add_argument('-usp', '--use_shake_prevention', action='store_true', help="If used, shake detection is activated")
    args = vars(parser.parse_args())
    print(args)
    try:
        f = open(args['json'], )
        data = json.load(f)
        print(data)
    except:
        print(Fore.RED + "Could not read file as json\nClosing program..." + Style.RESET_ALL)
        sys.exit(1)


    video = cv2.VideoCapture(0)

    img_1 = np.zeros([int(video.get(4)), int(video.get(3)), 3], dtype=np.uint8)
    img_1.fill(255)
    cv2.imshow("canvas",img_1)
    cv2.setMouseCallback("canvas",draw_with_mouse)
    pos_1=()
    while True:
        ret, frame = video.read()
        cv2.imshow(windowname, frame)
        ret, cX, cY = segment(data, windowname, frame)
        if ret:
            if len(pos_1):
                    if args['use_shake_prevention'] and sqrt((pos_1[0]-cX)**2+(pos_1[1]-cY)**2)>20:
                        pos_1=()
                    if len(pos_1):                    
                        cv2.line(img_1, pos_1, (int(cX),int(cY)), color, width,-1)
                        cv2.imshow("canvas",img_1)
            pos_1=(int(cX),int(cY))
        key = cv2.waitKey(1)
        # the 'q' button is set as the quitting button and w writes thresholds to file
        if key == ord('q'):
            break
        elif key == ord('w'):
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
