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
	if cv2.getTrackbarPos('Red_max','frame')>127:
		print(">127")
	else:
		print("<127")


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
    vid = cv2.VideoCapture(0)
    cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)

    cv2.createTrackbar('Red_max','frame',data['limits']['R']['max'],255,change_color)
    cv2.createTrackbar('Red_min','frame',data['limits']['R']['min'],255,change_color)
    cv2.createTrackbar('Green_max','frame',data['limits']['G']['max'],255,change_color)
    cv2.createTrackbar('Green_min','frame',data['limits']['G']['min'],255,change_color)
    cv2.createTrackbar('Blue_max','frame',data['limits']['B']['max'],255,change_color)
    cv2.createTrackbar('Blue_min','frame',data['limits']['B']['min'],255,change_color)

    while(True):
        
        # Capture the video frame by frame
        ret, frame = vid.read()
    
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

try:
    f = open('limits.json',)
    data = json.load(f)
except:
    print(Fore.RED+"Could not read file as json\nClosing program..."+Style.RESET_ALL)
    sys.exit(1)

if __name__ == "__main__":
    main()