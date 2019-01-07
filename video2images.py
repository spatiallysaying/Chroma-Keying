# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:41:16 2019

@author: E442282
"""

import argparse
import sys
import cv2
import os

def video2images(inputvideofile,outputimagesfolder):
       vidcap = cv2.VideoCapture(inputvideofile)
       returnvalue,image = vidcap.read() #returns true/fals and an image
       count = 0
       while returnvalue:
         filename=os.path.join(outputimagesfolder,"image%d.jpg" % count)
         cv2.imwrite(filename, image)     # save frame as JPEG/png file      
         returnvalue,image = vidcap.read()
         print('Read next frame: ', returnvalue)
         cv2.imshow('video',image)
         if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
             break
         count += 1
       cv2.destroyAllWindows()
       print('Completed Saving video frames')
       
def main(argv):
   ap = argparse.ArgumentParser()
   ap.add_argument("-i", "--input", required=True,  help="Input video file ")
   ap.add_argument("-o", "--output", required=False, default='.', help="output images directory")
   args = vars(ap.parse_args())
     
   inputvideofile = args['input']
   outputimagesfolder = args['output'] 
   
   
#   inputvideofile = 'popeye3.mp4'  #Specify imput video file here
#   outputimagesfolder = r'C:\SAI\IIIT\2019_Spring' #Path to target images folder
   video2images(inputvideofile,outputimagesfolder)

   
if __name__ == "__main__":
   main(sys.argv[1:])
   
   