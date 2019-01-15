# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 14:41:16 2019

@author: E442282
"""

import argparse
import os,sys
import cv2

import numpy as np

"""
https://stackoverflow.com/questions/36817133/identifying-the-range-of-a-color-in-hsv-using-opencv

Choose any range around your target value. for example yellow has hue val 60 degrees. 
(Use https://www.tydac.ch/color/)
So your hue range might be from 60/2 - 10 to 60/2 + 10 OR 
from 60/2-5 to 60/2+5 depends on how far you want to go away from perfect yellow.

For HSV, Hue range is [0,179], Saturation range is [0,255] and Value range is [0,255]. This is true for OpenCV,could be different for GIMP

https://www.learnopencv.com/color-spaces-in-opencv-cpp-python/

"""

import re

'''
To maintain images sequence , sort the file names numerically
#https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python

'''
def numericalSort(value):
    numbers = re.compile(r'(\d+)')
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


def video2images(inputvideofile,outputimagesfolder):
       vidcap = cv2.VideoCapture(inputvideofile)
       returnvalue,image = vidcap.read() #returns true/fals and an image
       count = 0
       while returnvalue:
         filename=os.path.join(outputimagesfolder,"image%d.jpg" % count)
         cv2.imwrite(filename, image)     # save frame as JPEG/png file      
         returnvalue,image = vidcap.read()
#         print('Read next frame: ', returnvalue)
#         cv2.imshow('video',image)
#         if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
#             break
         count += 1
       cv2.destroyAllWindows()
       print('\nCompleted Saving video frames to ',outputimagesfolder)
    

def createdirectory(dirName):
        # Create target Directory if don't exist
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("\nDirectory " , dirName ,  " Created ")
    else:    
        print("\nDirectory " , dirName ,  " Using existing directory")

def generateimages(videofile):
    head, tail = os.path.split(videofile)
    temp=tail.split('.')[0]
    outputimagesfolder=os.path.join(head,temp)
    createdirectory(outputimagesfolder)
    print('Created ', outputimagesfolder)
    video2images(videofile,outputimagesfolder)
    
    #Filter folder for images
    included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(outputimagesfolder)
              if any(fn.endswith(ext) for ext in included_extensions)]
#    print(file_names)
    images_temp=[]
    images=[]
    #Get image paths
    for file in file_names:
        image_path=os.path.join(outputimagesfolder,file)        
        images_temp.append(image_path)
        
    #Sorth the paths according to numnerical sequence in which they are generated    
    for infile in sorted(images_temp, key=numericalSort):
        images.append(infile)
    return  images


       
def chromakey(green_video,target_video,output_video):
    
    green_images=generateimages(green_video)
    
    target_images=generateimages(target_video)
    
    #Make sure that the number of frames in source and target are same
    target_images=target_images[:len(green_images)]
    
#    print(len(green_images))
#    print(len(target_images))
           
    lower_green = np.array([50])
    upper_green = np.array([70]) 
    
    #Chroma Keyed video - widht and height as that of source/target video
    frame = cv2.imread(green_images[0])   
    height, width, bands = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
#    video = cv2.VideoWriter(output_video, fourcc, 24, (width, height))
    video = cv2.VideoWriter(output_video, fourcc, 24, (640, 360))
    
    
    for green_image_path,target_frame_path in zip(green_images,target_images):
        
        green_frame  = cv2.imread(green_image_path)  
        target_frame = cv2.imread(target_frame_path)

        rows,cols,channels = green_frame.shape
        # cols-1 and rows-1 are the coordinate limits.
        
        #Translating fore- ground to match background video context
        M = np.float32([[1,0,200],[0,1,100]])
        green_frame = cv2.warpAffine(green_frame,M,(cols,rows), borderMode=cv2.BORDER_CONSTANT,
                                   borderValue=(0,255,0))

        # BGR to HSV
        hsv = cv2.cvtColor(green_frame, cv2.COLOR_BGR2HSV)
        # HSV bands
        h = hsv[:,:,0]
        #s = hsv[:,:,1]
        #v = hsv[:,:,2]
        
        #Threshold the HSV image to get only green color
        #hue_mask_source is 255 where color between lower_green & upper_green [background]
        #otherwise it is zero [foreground]
        hue_mask_source = cv2.inRange(h, lower_green, upper_green) 
        		
        #Generate Panchromatic image by inverting the values of FG and BG of hue_mask_source
        #Background is 0
        #Foreground is 255
        hue_masked_source_image=np.where(hue_mask_source != 0,0,255)
        

#        rgb = cv2.cvtColor(green_frame, cv2.COLOR_BGR2RGB)
#        blues = rgb[:,:,0]
#        greens = rgb[:,:,1]
#        reds = rgb[:,:,2]
#        
#        hue_masked_source_image=((greens<220)|(reds>=greens)|(blues>=greens))*255
#

        
#        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#        blues = rgb[:,:,0]
#        greens = rgb[:,:,1]
#        reds = rgb[:,:,2]
#        
#        hue_masked_source_image=((greens<60)|(reds>=greens)|(blues>=greens))*255


        
        # From original green screen image, identify the foreground identified by using hue_mask_source as cookie cutter
        masked_image = np.copy(green_frame)
        masked_image[hue_masked_source_image == 0] = [0, 0, 0]

        #Make a hole in the target image to the extent of source FG boundary
        output_video_frame = target_frame.copy()
        output_video_frame=cv2.resize(output_video_frame,(640,360))
        output_video_frame[hue_masked_source_image != 0] = [0, 0, 0]
        #Add Source FG and background image
        output_video_frame = output_video_frame + masked_image
        
        output_video_frame=cv2.resize(output_video_frame,(640,360))
        video.write(output_video_frame) # Append frame to video
#        cv2.imshow('Chroma Key',output_video_frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break
      
    video.release()
    cv2.destroyAllWindows() 
    print('\nCompleted Chorma keying')
     
       
def main(argv):
   ap = argparse.ArgumentParser()
   ap.add_argument("-s", "--source", required=True,  help="Source green screen background videofile ")
   ap.add_argument("-t", "--target", required=True,  help="Target video file ")   
   ap.add_argument("-o", "--output", required=False, default='merged.mp4', help="matted video")
   args = vars(ap.parse_args())
     
   green_video = args['source']
   target_video = args['target'] 
   output_video = args['output'] 


#   green_video=os.path.join(r'C:\SAI\IIIT\2019_Spring\cv0_ver1','fg.mp4')
#   target_video=os.path.join(r'C:\SAI\IIIT\2019_Spring\cv0_ver1','bg.mp4')
#   output_video=os.path.join(r'C:\SAI\IIIT\2019_Spring\cv0_ver1','baby_with_bunny.mp4')
#    

    
   print('Started Chroma Keying..')
   chromakey(green_video,target_video,output_video)

if __name__ == "__main__":
   main(sys.argv[1:])
   




















   