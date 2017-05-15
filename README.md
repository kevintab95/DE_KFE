# DE_KFE
Key Frame Extraction using Differential Evolution

Python scripts that implement DE for extraction of key frames from a video stream.

NOTE: This repository is intended as a backup for my final year project files.

Requirements:
* Python 2.7
* Additional Python libraries:
  * cv2
  * skimage
  * imageio

This repository contains five python scripts:

1. DE_SSIM.py

   This script uses Average SSIM as the fitness function.  
   Input: JPEG images (frames from a video)  
   Output: GIF image containing all the extracted key frames.
  
2. DE_Entropy.py

   This script uses Average Entropy Difference as the fitness function.  
   Input: JPEG images (frames from a video)  
   Output: GIF image containing all the extracted key frames.
  
3. DE_Euclidean.py

   This script uses Average Euclidean Distance as the fitness function.  
   Input: JPEG images (frames from a video)  
   Output: GIF image containing all the extracted key frames.
  
4. DE_LIVE.py

   This script uses Average Euclidean Distance as the fitness function. It extracts key frames from a live video,
   it will output a GIF image containing the extracted key frames periodically 
   (depending on how many frames to read and number of key frames required).  
   Input: JPEG images (output from capture_xframes)  
   Output: GIF image containing all the extracted key frames.
  
5. capture_xframes.py

   This script captures webcam stream and saves the frames as JPEG files.
  
