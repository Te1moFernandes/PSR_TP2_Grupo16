#!/usr/bin/python3
# import the opencv library
import cv2
import json
  
# define a video capture object

#callback para as trackbars
def change_color(x):
    	#condition to change color if trackbar value is greater than 127 
	if cv2.getTrackbarPos('Red_max','frame')>127:
		print(">127")
	else:
		print("<127")

def main():
    vid = cv2.VideoCapture(0)
    cv2.namedWindow("frame", cv2.WINDOW_AUTOSIZE)


    f = open('limits.json',)
    data = json.load(f)
    cv2.createTrackbar('Red_max','frame',255,255,change_color)
    cv2.createTrackbar('Red_min','frame',15,255,change_color)
    cv2.createTrackbar('Green_max','frame',255,255,change_color)
    cv2.createTrackbar('Green_min','frame',15,255,change_color)
    cv2.createTrackbar('Blue_max','frame',255,255,change_color)
    cv2.createTrackbar('Blue_min','frame',15,255,change_color)

    while(True):
        
        # Capture the video frame
        # by frame
        ret, frame = vid.read()
    
        # Display the resulting frame
        cv2.imshow('frame', frame)
        
        # the 'q' button is set as the
        # quitting button you may use any
        # desired button of your choice
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


    # After the loop release the cap object
    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()