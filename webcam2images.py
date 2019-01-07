# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:41:16 2019

@author: E442282
"""

import argparse
import sys
import cv2
import os

def webcam2images(outputimagesfolder):
       vidcap = cv2.VideoCapture(0)
       returnvalue,image = vidcap.read() #returns true/fals and an image
       count=0
       while returnvalue:

         filename=os.path.join(outputimagesfolder,"image%d.jpg" % count)   
         returnvalue,image = vidcap.read()
         
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
   
   