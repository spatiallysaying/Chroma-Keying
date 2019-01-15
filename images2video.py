"""
Created on Sun Jan  6 11:08:27 2019
@author: Durga Prasad
"""

import argparse
import sys
import cv2
import os
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

def images2video(inputimagesfolder,outputvideofile,frame_rate):
     
    #Filter folder for images
    included_extensions = ['jpg','jpeg', 'bmp', 'png', 'gif']
    file_names = [fn for fn in os.listdir(inputimagesfolder)
              if any(fn.endswith(ext) for ext in included_extensions)]
#    print(file_names)
    images_temp=[]
    images=[]
    #Get image paths
    for file in file_names:
        image_path=os.path.join(inputimagesfolder,file)        
        images_temp.append(image_path)
        
    #Sorth the paths according to numnerical sequence in which they are generated    
    for infile in sorted(images_temp, key=numericalSort):
        images.append(infile)

    # Get dimension of the images    
    image_path = images[0]
    frame = cv2.imread(image_path)
    cv2.imshow('video',frame)
    height, width, bands = frame.shape
    
    #Add these images to a video file
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    video  = cv2.VideoWriter(outputvideofile, fourcc, frame_rate, (width, height))
   
    for image in images:        
        frame = cv2.imread(image)
        video.write(frame) # Append frame to video

        cv2.imshow('images2video',frame)
        if (cv2.waitKey(1) & 0xFF) == ord('q'): # Hit `q` to exit
            break 
    video.release()
    cv2.destroyAllWindows()        
        
    print('Completed converting images to video')

       
def main(argv):
   ap = argparse.ArgumentParser()
   ap.add_argument("-i", "--input", required=True,  help="Input Images directory ")
   ap.add_argument("-o", "--output", required=False, default='output.mp4', help="output video file")
   ap.add_argument("-f", "--frame_rate", required=False, default=24.0, help="Frame rate of the video")
    
   args = vars(ap.parse_args())
     
   inputimagesfolder = args['input']
   outputvideofile = args['output'] 
   frame_rate=int(args['frame_rate'])
   
   print(inputimagesfolder)
   print(outputvideofile)
   images2video(inputimagesfolder,outputvideofile,frame_rate)
#   images2video(r'C:\SAI\IIIT\2019_Spring\images','output.mp4',24) 
   
if __name__ == "__main__":
   main(sys.argv[1:])