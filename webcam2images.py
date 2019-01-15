# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:41:16 2019

@author: E442282
"""

import argparse
import sys,os
import cv2
import time

def getframerate(video):
    begin = time.time()
    num_frames=80
    for i in range(0, num_frames) :
        ret, frame = video.read()
#        print(i)
    end = time.time()
    seconds = end - begin
    frame_rate  = num_frames / seconds
    return frame_rate
    
def webcam2images(outputimagesfolder):
       vidcap = cv2.VideoCapture(0)
       frame_rate=getframerate(vidcap)# Get frame rate
       
       returnvalue,image = vidcap.read() #returns true/fals and an image
       count=0
       font                   = cv2.FONT_HERSHEY_SIMPLEX
       text_BL = (100,50)
       fontScale              = 0.5
       fontColor              = (0, 255, 0)
       lineType               = 1

       text_BL2 = (100,100)
       fontColor2              = (255, 255, 0)
     
       text_BL3 = (100,150)
       fontColor3              = (0, 255,255)
        
       while returnvalue:

         filename=os.path.join(outputimagesfolder,"image%d.jpg" % count)   
         returnvalue,image = vidcap.read()
         
         cv2.putText(image,'Click "c" to save image ',  text_BL,font,fontScale,fontColor,lineType)
         cv2.putText(image,'Click "q" to save image ',  text_BL2,font,fontScale,fontColor2,lineType)      
         cv2.putText(image,'Frame rate ' +str(frame_rate),  text_BL3,font ,fontScale,fontColor3,lineType)
         
         cv2.imshow('webcam2images',image)
         if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
             break
         if (cv2.waitKey(1) & 0xFF) == ord('c'):
             cv2.imwrite(filename, image)     # save frame as JPEG/png file 
         count += 1    
       cv2.destroyAllWindows()
       print('Completed Saving video frames')
       
def main(argv):
   ap = argparse.ArgumentParser()
   ap.add_argument("-o", "--output", required=False, default='.', help="output images directory")
   args = vars(ap.parse_args())
     
   outputimagesfolder = args['output'] 
   webcam2images(outputimagesfolder)
  
if __name__ == "__main__":
   main(sys.argv[1:])
   
   
   
   
   
   
   
   