import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
import boto3
from boto3.dynamodb.conditions import Key
AWS_ACCESS_KEY = " "
AWS_SECRET_ACCESS = ' '

TABLE_NAME = 'cars'

from picamera.array import PiRGBArray
from picamera import PiCamera
import datetime 
from datetime import timedelta

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

tablename='cars'
Primary_Column_Name='reg'

columns=["timestp"]

client = boto3.client('dynamodb')

db=boto3.resource('dynamodb')
#dynamotable=dynamodb.table('cars')
table=db.Table('cars')

def capt():
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
             t=datetime.datetime.now() #current date time
             time_object=t.time()
             time_string=time_object.strftime("%H:%M:%S")
             t1=(t.strftime("%X"))
             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
             gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
             edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
             cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
             cnts = imutils.grab_contours(cnts)
             cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
             screenCnt = None
             for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                  screenCnt = approx
                  break
             if screenCnt is None:
               detected = 0
               print ("No contour detected")
             else:
               detected = 1
             if detected == 1:
               cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
             mask = np.zeros(gray.shape,np.uint8)
             new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
             new_image = cv2.bitwise_and(image,image,mask=mask)
             (x, y) = np.where(mask == 255)
             (topx, topy) = (np.min(x), np.min(y))
             (bottomx, bottomy) = (np.max(x), np.max(y))
             Cropped = gray[topx:bottomx+1, topy:bottomy+1]
             
             text = pytesseract.image_to_string(Cropped, config='--psm 11')
             
             print("Detected Number is:",text)
             
             cv2.imshow("Frame", image)
             cv2.imshow('Cropped',Cropped)
             response=table.put_item(
                 Item={
                     Primary_Column_Name:text,
                     columns[0]:time_string,
                     #columns[1]:t1
#                      'reg'=text,
#                      'time'=t
                     }
                 
                 )
             #cv2.waitKey(0)
             break
    cv2.destroyAllWindows()
    
###############################
def capt1():
    
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
        if key == ord("s"):
             time_object=datetime.datetime.now() #current date time
             #time_object=t.time()
#              print("timeobj")
#              print(time_object)
             time_string=time_object.strftime("%H:%M:%S") #TIME AS STRING TO send to db
#              
             time_object=datetime.datetime.strptime(time_string,"%H:%M:%S")
             
             t1=(time_object.strftime("%X"))
             gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #convert to grey scale
             gray = cv2.bilateralFilter(gray, 11, 17, 17) #Blur to reduce noise
             edged = cv2.Canny(gray, 30, 200) #Perform Edge detection
             cnts = cv2.findContours(edged.copy(), cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
             cnts = imutils.grab_contours(cnts)
             cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:10]
             screenCnt = None
             for c in cnts:
                peri = cv2.arcLength(c, True)
                approx = cv2.approxPolyDP(c, 0.018 * peri, True)
                if len(approx) == 4:
                  screenCnt = approx
                  break
             if screenCnt is None:
               detected = 0
               print ("No contour detected")
             else:
               detected = 1
             if detected == 1:
               cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 3)
             mask = np.zeros(gray.shape,np.uint8)
             new_image = cv2.drawContours(mask,[screenCnt],0,255,-1,)
             new_image = cv2.bitwise_and(image,image,mask=mask)
             (x, y) = np.where(mask == 255)
             (topx, topy) = (np.min(x), np.min(y))
             (bottomx, bottomy) = (np.max(x), np.max(y))
             Cropped = gray[topx:bottomx+1, topy:bottomy+1]
             
             text = pytesseract.image_to_string(Cropped, config='--psm 11')
             
             print("Detected Number is:",text)
             
             cv2.imshow("Frame", image)
             cv2.imshow('Cropped',Cropped)
#              response=table.get_item(
#                  Key={
#                      'reg':text
#                      }
#                  )
#              print(response)
             
             response = table.query(
                 KeyConditionExpression=Key('reg').eq(text),
                 ProjectionExpression='timestp'
                 
                 )
             items= response['Items']
             for item in items:
                 print(item)
                 print("timestamp of matched result from database")
                 tn=item
                 
                 tn1=item["timestp"]
                 print(tn1)
                 
                 datetime_obj2=datetime.datetime.strptime(tn1,"%H:%M:%S")
               
                 #t=t.total_seconds()
                 #datetime_obj2=datetime_obj2.total_seconds()
#                  time_object=time_object.second
#                  datetime_obj2=datetime_obj2.second
                 dif=time_object-(datetime_obj2)
                 diff=dif.total_seconds()
                 print("difference in time in seconds ")
                 print(diff)
                 print("speed in kmph")
                 speed=0.175/(diff/3600)
                 print(speed)
                 if(speed>80):
                     offenders.append(text)
             #print(ProjectionExpression)
             #datetime_obj=datetime.datetime.strptime(time_string,"%H:%M:%S")
             #params.ProjectionExpression ="time"    
             #cv2.waitKey(0)
             break
    cv2.destroyAllWindows()
    


offenders=[]
capt()
capt1()

