#!/usr/bin/python3
import argparse
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

img_1 = np.zeros([512,512,1],dtype=np.uint8)
img_1.fill(255)