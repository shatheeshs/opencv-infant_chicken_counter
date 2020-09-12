import cv2
import sys
import numpy as np

#take BGR values from command line
blue=sys.argv[1]
green=sys.argv[2]
red=sys.argv[3]


#change the video footage name here!!!!
cap = cv2.VideoCapture('introResized.mp4')

widthFrame=720
heightFrame=404

color=np.uint8([[[blue,green,red]]])
hsv_color=cv2.cvtColor(color,cv2.COLOR_BGR2HSV)

#initialize hsv values according to BGR color space
hue=hsv_color[0][0][0]
sat=hsv_color[0][0][1]
val=hsv_color[0][0][2]

#print correct range of hsv wrt Yellow Color
print("Lower bound is :"),
print("[" + str(hue-10) + ", 30, 30]\n")
 
print("Upper bound is :"),
print("[" + str(hue + 10) + ", 255, 255]")

#initialize Yellow Color range in HSV color space
lower_range = np.array([(hue-10), 30, 30], dtype=np.uint8)
upper_range = np.array([(hue + 10), 255, 255], dtype=np.uint8)



while(cap.isOpened()):

	ret, frame = cap.read()

	#video end exception
	try:
		totalPixels = frame.shape[0] * frame.shape[1]

	except AttributeError:
		print('Video footage is over..')
		break

	#basic imageProcessing
	# resizedFrame=cv2.resize(frame,(widthFrame,heightFrame),cv2.INTER_CUBIC)
	hsvImage=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
	filteredImage= cv2.GaussianBlur(hsvImage,(3,3),0)
	mask = cv2.inRange(filteredImage, lower_range, upper_range)
	nonzero = cv2.countNonZero(mask)
	ratioYellow = (nonzero / float(totalPixels))*100
	
	#output to command line
	print('TotalPixels: '+ str(totalPixels) +' YellowPixels: '+ str(nonzero) + ' YellowPixelRatio: '  + str(round(ratioYellow,2))+"%")


	cv2.imshow('BINARY_colorspace_footage',mask)
	cv2.imshow('HSV_colorspace_footage',hsvImage)
	cv2.moveWindow("HSV_colorspace_footage", 0,0);
	cv2.moveWindow("BINARY_colorspace_footage", 600,250);

	if cv2.waitKey(1) & 0xFF == ord('q'):
		print('Application is Closed')
		break

#releasing the video cap
cap.release()
cv2.destroyAllWindows()