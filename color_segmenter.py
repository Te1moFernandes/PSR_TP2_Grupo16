#!/usr/bin/python3
# import the opencv library
import cv2
import json
import sys
from colorama import *
import argparse

def change_color(x):
    global windowname
    #condition to change color if trackbar value is greater than 127
    if cv2.getTrackbarPos('Red_max', windowname) < cv2.getTrackbarPos('Red_min', windowname):
        cv2.setTrackbarPos('Red_max', windowname, cv2.getTrackbarPos('Red_min', windowname))
    if cv2.getTrackbarPos('Blue_max', windowname) < cv2.getTrackbarPos('Blue_min', windowname):
        cv2.setTrackbarPos('Blue_max', windowname, cv2.getTrackbarPos('Blue_min', windowname))
    if cv2.getTrackbarPos('Green_max', windowname) < cv2.getTrackbarPos('Green_min', windowname):
        cv2.setTrackbarPos('Green_max', windowname, cv2.getTrackbarPos('Green_min', windowname))

def write_to_file(data):
    global windowname
    data['limits']['R']['max'] = cv2.getTrackbarPos('Red_max', windowname)
    data['limits']['R']['min'] = cv2.getTrackbarPos('Red_min', windowname)
    data['limits']['G']['max'] = cv2.getTrackbarPos('Green_max', windowname)
    data['limits']['G']['min'] = cv2.getTrackbarPos('Green_min', windowname)
    data['limits']['B']['max'] = cv2.getTrackbarPos('Blue_max', windowname)
    data['limits']['B']['min'] = cv2.getTrackbarPos('Blue_min', windowname)
    print("Escreveu as seguintes configurações:")
    print(data)
    with open('limits.json', 'w') as outfile:
        json.dump(data, outfile)


def limit_image(B, G, R):
    _, thresh1 = cv2.threshold(B, cv2.getTrackbarPos('Blue_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh2 = cv2.threshold(B, cv2.getTrackbarPos('Blue_min', 'frame'), 255, cv2.THRESH_BINARY)
    _, thresh3 = cv2.threshold(G, cv2.getTrackbarPos('Red_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh4 = cv2.threshold(G, cv2.getTrackbarPos('Red_min', 'frame'), 255, cv2.THRESH_BINARY)
    _, thresh5 = cv2.threshold(R, cv2.getTrackbarPos('Green_max', 'frame'), 255, cv2.THRESH_BINARY_INV)
    _, thresh6 = cv2.threshold(R, cv2.getTrackbarPos('Green_min', 'frame'), 255, cv2.THRESH_BINARY)

    thresh_blue = cv2.bitwise_and(thresh1, thresh2)
    cv2.imshow('blue', thresh_blue)

    thresh_red = cv2.bitwise_and(thresh3, thresh4)
    cv2.imshow('red', thresh_red)

    thresh_green = cv2.bitwise_and(thresh5, thresh6)
    cv2.imshow('green', thresh_green)

    final_thresh = cv2.bitwise_and(thresh_blue, thresh_green)
    final_thresh = cv2.bitwise_and(final_thresh, thresh_red)
    cv2.imshow('image', final_thresh)
    return final_thresh

def segment(windowname, frame):
    R = frame[:, :, 0] #  blue channel
    G = frame[:, :, 1] #  green channel
    B= frame[:, :, 2] #  red channel
    img_w_thresh = limit_image(B, G, R)



def main():
    parser = argparse.ArgumentParser(description='PSR argparse example.')
    parser.add_argument('-j', '--json', default='limits.json', help="Full path to json file.")
    args = vars(parser.parse_args())

    try:
        f = open(args['json'], )
        data = json.load(f)
        print(data)
    except:
        print(Fore.RED + "Could not read file as json\nClosing program..." + Style.RESET_ALL)
        sys.exit(1)
    global windowname
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
        segment(windowname, frame)
        key = cv2.waitKey(1)
        if key == ord("q"):
            break
        elif key == ord('w'):
            print("writes")
            write_to_file(data)

windowname = 'frame'

if __name__ == "__main__":
    main()
