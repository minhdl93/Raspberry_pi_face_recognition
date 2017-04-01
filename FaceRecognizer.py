import cv2
import numpy as np
from imutils.video.pivideostream import PiVideoStream
from imutils.video import FPS
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import argparse
import imutils

#Load pretrained cascade face detection
face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')
#Load improved FPS video instead of the default Picamera
reader  = PiVideoStream().start()
time.sleep(0.2)
#Load the recognizer
rec = cv2.face.createLBPHFaceRecognizer()
#Load trained local binary pattern face data
rec.load("recognizer/trainingData.yml")
id=0
font = cv2.FONT_HERSHEY_SIMPLEX

#Face recognition function
def detectFace(faces,hog,img):
	for (x, y, w, h) in faces:
	   cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
	   result = cv2.face.MinDistancePredictCollector()
	   rec.predict(hog[y:y+h,x:x+w],result, 0)
	   id = result.getLabel()

	   conf = result.getDist()
	   if(conf<150):
		   if(id==1):
			   id="Ibrahim_"+str(conf)
		   elif(id==2):
			   id="Minh_"+str(conf)
		   else:
			   id="Hyeon_"+str(conf)
	   else:
			id="Unknow"
	   cv2.putText(img,str(id),(x,y+h),font,1,(255,255,255),2,cv2.LINE_AA)		
	   
	   
while(True):
	#read each frame in the real-time video
    frame = reader.read()
    img=frame
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	#Use histogram equalizer for adjusting face in different light condition
    equ = cv2.equalizeHist(gray) 
    faces = face_cascade.detectMultiScale(equ, 1.05, 5,minSize=(10,10))
	#If the face is not frontal face then rotate the face by +30/-30 degree 
    if len(faces)==0:
		rows,cols = equ.shape
		M = cv2.getRotationMatrix2D((cols/2,rows/2),30,1)
		dst = cv2.warpAffine(equ,M,(cols,rows))
		faces = face_cascade.detectMultiScale(dst, 1.05, 5,minSize=(10,10))
		if len(faces)==0:
			rows,cols = equ.shape
			M = cv2.getRotationMatrix2D((cols/2,rows/2),-30,1)
			dst = cv2.warpAffine(equ,M,(cols,rows))
			faces = face_cascade.detectMultiScale(dst, 1.05, 5,minSize=(10,10))
			detectFace(faces,dst,img)

		else:
			detectFace(faces,dst,img)

    else:
		detectFace(faces,equ,img)

    cv2.imshow('Face', img)
    if(cv2.waitKey(1)==ord('q')):
        break;

cap.release()
cv2.destroyAllWindows()
