# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:41:16 2019

@author: E442282
"""

import argparse
import sys
import cv2
import os

def getzoomout(image):
    
    row, col= image.shape[:2]
    bordersize=100
    border=cv2.copyMakeBorder(image, top=bordersize, bottom=bordersize, left=bordersize,
                              right=bordersize, borderType= cv2.BORDER_CONSTANT,
                              value=[0,255,0] )
    return border

def video2images(inputvideofile,outputimagesfolder):
       vidcap = cv2.VideoCapture(inputvideofile)
       returnvalue,image = vidcap.read() #returns true/false and an image
       count = 0
       while returnvalue:
         returnvalue,image = vidcap.read()   
         if returnvalue==False:
             break
         filename=os.path.join(outputimagesfolder,"image%d.jpg" % count)
#         image=getzoomout(image)         
         cv2.imwrite(filename, image)     # save frame as JPEG/png file   
         print('Read next frame: ', returnvalue)
         cv2.imshow('video',image)

         if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit\
             break
             
         count += 1
       vidcap.release()  
       cv2.destroyAllWindows()
       print('\nCompleted Saving video frames to',outputimagesfolder)

def main(argv):
   ap = argparse.ArgumentParser()
   ap.add_argument("-i", "--input", required=True,  help="Input video file ")
   ap.add_argument("-o", "--output", required=False, default='.', help="output images directory")
   args = vars(ap.parse_args())
     
   inputvideofile = args['input']
   outputimagesfolder = args['output'] 
   
#   inputvideofile = 'popeye3.mp4' 
#   outputimagesfolder=r' C:\SAI\IIIT\2019_Spring\images' 
   video2images(inputvideofile,outputimagesfolder)

   
if __name__ == "__main__":
   main(sys.argv[1:])
   
   