#!/usr/bin/python3
import argparse

import cv2
import numpy as np
from colorama import *
import sys
import json
import color_segmenter
parser = argparse.ArgumentParser(description='PSR argparse example.')
parser.add_argument('-j', '--json', default='limits.json', help="Full path to json file.")
args = vars(parser.parse_args())
print(args['json'])
try:
    f = open(args['json'],)
    print("gets f")
    data = json.load(f)
    print(data)

    color_segmenter.main(data)
except:
    print(Fore.RED+"Could not read file as json\nClosing program..."+Style.RESET_ALL)
    sys.exit(1)

img_1 = np.zeros([512, 512, 1], dtype=np.uint8)
img_1.fill(255)

im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
for c in contours:
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    cv2.circle(image, (cX, cY), 5, (255, 255, 255), -1)
    cv2.putText(img, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    cv2.imshow("Image", img)

def main():
    vid = cv2.VideoCapture(0)
