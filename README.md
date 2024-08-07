# Most Information Frame Extractor

Pass a YouTube Video link and get the screenshots of the frame which has the most information content (like if someone is explaining with the help of a PPT, capture screenshot when all the text of one slide of PPT has animated in)

Frame with most information it can possibly have
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/854332d4-5d59-4f11-aeff-e0fa0c8e1fcd)

This frame can have more information and thus not the most information frame
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/35eed63d-e490-441a-ab65-06ad336cb8aa)

# How

The approach I have taken in this code is to perform frame-by-frame analysis of a video to extract text using Optical Character Recognition (OCR) and save only the frames that contain significant changes or improvements in the text content.

The main steps involved in this approach are:

1. Frame Reading: The script reads frames from the video file at a specified interval (e.g., every second, every frame, etc.) using OpenCV's cv2.VideoCapture.
2. Frame Difference Calculation: For each frame, the script calculates the difference between the current frame and the previous frame using OpenCV's point processing techniques. If the difference is below a specified threshold, the frame is considered to have insignificant changes and is skipped.
3. Optical Character Recognition (OCR): If the frame difference is significant, the script performs OCR on the frame using Tesseract OCR engine to extract the text content from the frame.
4. Text Difference Calculation: The extracted text from the current frame is compared with the text from the previous frame using a sequence matcher (difflib.SequenceMatcher). If the text difference is below a specified threshold, the current frame is considered to contain an improvement or new information compared to the previous frame.
5. Frame Saving: If the text difference is significant, the script saves the previous frame with a frame number or timestamp burned onto it, using OpenCV's image writing functions.
6. Iteration: The process repeats for each frame, updating the previous frame and previous text with the current frame and text if the text difference is significant.

This approach allows the script to analyze the video frame-by-frame, identify frames with significant visual and textual changes, and save only those frames that contain improved or new text information. By adjusting the thresholds for frame difference and text difference, the script can be fine-tuned to capture the desired level of changes in the video content.

I used the concept of point processing on images to compare difference in image on pixel level and proceed to compare using text content of the current and previous frame only if the difference is significant on image pixel level.

![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/b27dccf8-62d5-48e8-875a-748a8e4671f6)

This way I reduced the redundancy by almost half; 87 frames (see left in the img) with only text content difference comparison and 47 frames (see right in the img) with the aforementioned optimization technique

There is a huge scope of improvement in this project and I would love to work on improving this...But since I have other projects to do as well, I couldn't work on it more for now.

If you would like to contribute/collaborate on this project, kindly ping me at vedantpanchal1345@gmail.com

# Made in 3hrs with Claude.ai

Start Time:
‎04 ‎May ‎2024, ‏‎14:07:39
![alt text](image.png)

End Time:
Sat May 4 17:11:13 2024 +0530
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/8e491cf1-10a9-405a-9f40-19986c69ffe9)

https://claude.ai/chat/b8d512fa-ad56-4134-9637-ad94a68a4bc6

Link to the claude chat:
https://aiarchives.org/id/2tB6EgjI2Y6GAxvJgqT0

# Continuing with the work

- mapping the graph
- saving only the frame after which the info content drops

# Update

- Now using a peak word count approach
- It has got even better accuracy with thresholding (currently manual, plan to make it automatic)

![alt text](image-1.png)

# TODO

[v] Write everything again using modular approach and oops approach

[] https://claude.ai/chat/80e72a8e-3db4-4900-b64c-b63b7c891bcc try this curve smoothening

[] https://claude.ai/chat/5f0fb230-e2cf-4f13-b628-02b04c991b0e
Try suggestions mentioned here

# Obstacles

### Obstacle 1
Someone explaning on whiteboard:
![alt text](image-2.png)

vkkjvu_peak_frames: Message Passing Systems (Part 2).mp4

possible solutions:
- smooth something
- dynamic thresholding or something like that

### Obstacle 2
In addition to text slides, footage of the person in between the video:
![alt text](image-3.png)

okhdwp_peak_frames: How I Mastered System Design Interviews.mp4

possible solutions:
- skip the frame where no text and only a person is present

### Obstacle 3
Poor results with background on the screen


# Using Moving Averages to find the desired frames

![alt text](image-4.png)

Got even better results with the moving averages method
What I did is plot the moving averages of the word count with small window size and large window size then found the intersection of the two curves and took the frame number at that point

![alt text](image-6.png)

Before: 295 frames (has non-max info frames too)
After: 81 frames (has mostly max info frames, few non-max info frames still present)