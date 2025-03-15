# Most Information Frame Extractor

Pass a YouTube Video link and get the screenshots of the frame which has the most information content (like if someone is explaining with the help of a PPT, capture screenshot when all the text of one slide of PPT has animated in)

Frame with most information it can possibly have
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/854332d4-5d59-4f11-aeff-e0fa0c8e1fcd)

This frame can have more information and thus not the most information frame
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/35eed63d-e490-441a-ab65-06ad336cb8aa)

> NOTE: The latest code can be found in the `v2` folder

## Running the code

- Clone the repository
- Install the requirements using `pip install -r requirements.txt`
- Create a folder named `data` in the `v2` folder
- `cd` into the `v2` folder
- Run the `main.py` file using `python main.py`

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

![alt text](images_for_readme/image-1.png)

# TODO

[v] Write everything again using modular approach and oops approach

[] https://claude.ai/chat/80e72a8e-3db4-4900-b64c-b63b7c891bcc try this curve smoothening

[] https://claude.ai/chat/5f0fb230-e2cf-4f13-b628-02b04c991b0e
Try suggestions mentioned here

## Obstacles

### Obstacle 1

Someone explaning on whiteboard:
![alt text](images_for_readme/image-2.png)

vkkjvu_peak_frames: Message Passing Systems (Part 2).mp4

possible solutions:

- smooth something
- dynamic thresholding or something like that

### Obstacle 2

In addition to text slides, footage of the person in between the video:
![alt text](images_for_readme/image-3.png)

okhdwp_peak_frames: How I Mastered System Design Interviews.mp4

possible solutions:

- skip the frame where no text and only a person is present

### Obstacle 3

Poor results with background on the screen

### Obstacle 4

https://claude.ai/chat/c89dfb2b-2e96-4912-b484-8adb242b5771

```
# Key Research Papers on Removing Obstacles from Multiple Photos

1. "Scene Completion Using Millions of Photographs" (Hays and Efros, 2007)
   - Pioneering work in using large image databases to fill in missing regions
   - Not specifically for obstacle removal, but laid groundwork for later research

2. "Shift-Map Image Editing" (Pritch et al., 2009)
   - Introduced a graph-cut based method for object removal and image retargeting
   - Can handle multiple input images to fill in removed regions

3. "PatchMatch: A Randomized Correspondence Algorithm for Structural Image Editing" (Barnes et al., 2009)
   - Fast algorithm for finding approximate nearest neighbor matches between image patches
   - Useful for image completion and object removal tasks

4. "Image Completion with Structure Propagation" (Sun et al., 2005)
   - Focuses on completing large missing regions in a single image
   - Uses structure propagation to maintain visual consistency

5. "Globally and Locally Consistent Image Completion" (Iizuka et al., 2017)
   - Uses deep neural networks for image completion
   - Can handle large missing regions and produce realistic results

6. "Context Encoders: Feature Learning by Inpainting" (Pathak et al., 2016)
   - Trains deep neural networks to predict missing content in images
   - Can be applied to obstacle removal tasks

7. "Deep Image Prior" (Ulyanov et al., 2018)
   - Shows that the structure of a neural network can be used as a prior for various image restoration tasks
   - Applicable to image inpainting and obstacle removal

8. "Generative Image Inpainting with Contextual Attention" (Yu et al., 2018)
   - Uses a two-stage network with contextual attention for image inpainting
   - Particularly effective for removing complex obstacles

9. "EdgeConnect: Generative Image Inpainting with Adversarial Edge Learning" (Nazeri et al., 2019)
   - Focuses on preserving edge structure when removing objects or filling in missing regions

10. "Multi-View Image Completion" (Thonat et al., 2016)
    - Specifically addresses the problem of completing missing regions using multiple input views
    - Useful for removing obstacles that appear in some, but not all, input images

These papers cover a range of approaches, from traditional computer vision techniques to modern deep learning methods. They address various aspects of the obstacle removal problem, including handling multiple input images, preserving structure and consistency, and generating realistic completions for removed regions.
```

Use multiple images of same thing to remove the obstacle and get clean screenshots
[] Go through the above research papers and try to adapt the techniques to this project

### Obstacle 5 - Diagrams

https://www.youtube.com/watch?v=9rp1pzYn3hY
Taking this video as an example, the diagrams are not being captured properly

### Peak prominence method is not working

Enter YouTube video URL: https://www.youtube.com/watch?v=_8xHh1tk7jY
Downloading video: Oral Pathology  Salivary Gland Benign Diseases  INBDE, ADAT
Download completed successfully!
Downloaded video to data/ikgmbd
Processed 84 frames
Enter 'auto' to auto-calculate k or enter k: auto
Detected 1 significant transitions in the signal
Extracted frames to data/ikgmbd_extracted_frames
Saved PDF to data/ikgmbd.pdf for Oral Pathology  Salivary Gland Benign Diseases  INBDE ADAT.mp4




## Updates - Using Moving Averages to find the desired frames

![alt text](images_for_readme/image-4.png)

Got even better results with the moving averages method
What I did is plot the moving averages of the word count with small window size and large window size then found the intersection of the two curves and took the frame number at that point

![alt text](images_for_readme/image-6.png)

Before: 295 frames (has non-max info frames too)
After: 81 frames (has mostly max info frames, few non-max info frames still present)

# Fixes

class InnerTube:
"""Object for interacting with the innertube API."""
def **init**(self, client='ANDROID_CREATOR', use_oauth=False, allow_cache=True):

Regex change in the get throtling function thing

### Update (29/07/2024)

https://claude.ai/chat/179f256d-6896-4158-a3bf-9903b9e92e4e

Trying to use GPU for the processing

```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
xformers 0.0.25.post1 requires torch==2.2.2, but you have torch 2.0.1+cu117 which is incompatible.
```

might need to fix this

ImportError: PyAV is not installed, and is necessary for the video operations in torchvision.
pip install av

Follow this to look for gpu ocr
https://claude.ai/chat/478fef1c-5b8d-4001-89a7-780d07b4e60a

## Resources for upgrading to GPU

https://www.youtube.com/watch?v=oOIxHDwXY1s
https://www.cse.cuhk.edu.hk/~byu/CMSC5743/2020Fall/slides/T02-OCR-TensorRT.pdf

## Errors to Fix

```
(base) D:\DPythonProjects\yt_summarizer>C:/Users/Vedant/anaconda3/python.exe d:/DPythonProjects/yt_summarizer/gpu_v3.py
Using device: cuda
Enter the URL of the YouTube video (or folder path): pfhpem
Directory 'D:\DPythonProjects\yt_summarizer\data\pfhpem_frames' created successfully.
C:\Users\Vedant\anaconda3\Lib\site-packages\torchvision\io\video.py:161: UserWarning: The pts_unit 'pts' gives wrong results. Please use pts_unit 'sec'.
  warnings.warn("The pts_unit 'pts' gives wrong results. Please use pts_unit 'sec'.")
C:\Users\Vedant\anaconda3\Lib\site-packages\torchvision\transforms\functional.py:1603: UserWarning: The default value of the antialias parameter of all the resizing transforms (Resize(), RandomResizedCrop(), etc.) will change from None to True in v0.17, in order to be consistent across the PIL and Tensor backends. To suppress this warning, directly pass antialias=True (recommended, future default), antialias=None (current default, which means False for Tensors and True for PIL), or antialias=False (only works on Tensors - PIL will still use antialiasing). This also applies if you are using the inference transforms from the models weights: update the call to weights.transforms(antialias=True).
  warnings.warn(
Directory 'D:\DPythonProjects\yt_summarizer\data\pfhpem_frame_text_data' created successfully.
Directory 'D:\DPythonProjects\yt_summarizer\data\pfhpem_plot' created successfully.
OMP: Error #15: Initializing libiomp5md.dll, but found libiomp5md.dll already initialized.
OMP: Hint This means that multiple copies of the OpenMP runtime have been linked into the program. That is dangerous, since it can degrade performance or cause incorrect results. The best thing to do is to ensure that only a single OpenMP runtime is linked into the process, e.g. by avoiding static linking of the OpenMP runtime in any library. As an unsafe, unsupported, undocumented workaround you can set the environment variable KMP_DUPLICATE_LIB_OK=TRUE to allow the program to continue to execute, but that may cause crashes or silently produce incorrect results. For more information, please see http://www.intel.com/software/products/support/.
```

## Leads

https://claude.ai/chat/75126ab2-61fe-4da6-98ab-235af098df7c

### 𝘔𝘢𝘹𝘪𝘮𝘪𝘻𝘦 𝘗𝘳𝘰𝘧𝘪𝘵 𝘣𝘺 𝘉𝘶𝘺𝘪𝘯𝘨 𝘢𝘯𝘥 𝘚𝘦𝘭𝘭𝘪𝘯𝘨 𝘢 𝘚𝘵𝘰𝘤𝘬 𝘢𝘵 𝘮𝘰𝘴𝘵 𝘒 𝘛𝘪𝘮𝘦𝘴

![alt text](images_for_readme/image-7.png)
![alt text](images_for_readme/image-8.png)

Nice results

### You need to take time as weight and scale the char count too

![alt text](images_for_readme/image-9.png)

The OCR can make mistake and mistakenly score the next frame with more data as having less data than the previous frame. And this data when passed to the Maximise Profit function can give wrong results. So, we need to scale the char count with time as weight to get better results.

![alt text](images_for_readme/image-10.png)
Popup in the video can also wrongly come in the OCR char count

### Using specialized software for person-free frames:

Photoshop: Use the "Stack Mode" feature in the "Statistics" script.
GIMP: Use the "Median Stack" plugin.
ImageMagick: Use the command-line tool with the "median" option.

https://claude.ai/chat/c2bc0976-d763-4056-97dc-431b22d8675b

### How many slides there could be?

```
The number of slides in a 10-minute educational video can vary significantly depending on several factors:

Presentation style: Some educators prefer to spend more time explaining each slide, while others may use more slides with less time on each.
Subject matter: Complex topics might require fewer slides with more explanation, while simpler topics could allow for more rapid progression.
Visual content: Slides with graphs, images, or diagrams may need more time for explanation compared to text-only slides.
Audience level: Presentations for beginners might move slower than those for advanced students.
Teaching objectives: Some lessons might focus on discussion, requiring fewer slides, while others might be more information-dense.

Given these variables, a rough estimate for a 10-minute video could range from:

Minimum: About 5-10 slides (spending 1-2 minutes per slide)
Average: Around 15-20 slides (spending 30-40 seconds per slide)
Maximum: Up to 30-40 slides (spending 15-20 seconds per slide)

The average of 15-20 slides is often considered a good balance for maintaining audience engagement without overwhelming them with information. However, these numbers can vary based on the specific needs of the lesson and the educator's style.
Would you like me to elaborate on any aspect of this estimate?
```

https://claude.ai/chat/30e10190-d4ba-47c8-9c75-38db02a8f090

### Strategy Design Pattern

- As the input can be of different types, we can use the strategy design pattern to make the code more modular and scalable

https://claude.ai/chat/9187f1d3-133a-4126-bc01-61238998ea51

### Post Processing to Remove Redundant Frames

![alt text](images_for_readme/image-11.png)

- create a swappable post processor
- the post processor does pixel wise or some other kind of comparison to remove redundant frames

### Finding Prominent Peaks

https://claude.ai/chat/110cfe52-6cbc-4bb1-95b0-bdc830de908e

```
This is a common problem in signal processing, especially when dealing with noisy data. Here are a few approaches you could use:

1. Peak Prominence Method
- Instead of just looking at local maxima, consider the "prominence" of each peak
- A peak's prominence is the height difference between the peak and the highest point between it and a higher peak

2. Smoothing the Signal
- Apply smoothing techniques before finding peaks to reduce noise:
  - Moving average
  - Gaussian smoothing
  - Savitzky-Golay filter (particularly good for preserving peak shapes)

3. Peak Width Method
- Consider peaks that have a minimum width
- This helps eliminate narrow noise spikes

This implementation provides several key features:

1. Multiple detection methods:
   - Pure prominence-based detection
   - Width-based detection
   - Smoothed signal with prominence detection
   - Savitzky-Golay filtered signal with peak detection

2. Configurable parameters:
   - Minimum prominence threshold
   - Minimum peak width
   - Smoothing window size
   - Polynomial order for Savitzky-Golay filter

3. Peak analysis functionality that provides statistics about detected peaks

To use this for your specific case, I'd recommend:

1. Start with the 'smooth_savgol' method, as it's generally good at preserving peak shapes while removing noise
2. Adjust the window_size parameter based on your signal's characteristics:
   - Larger window = more smoothing but might miss closer peaks
   - Smaller window = less smoothing but might detect noise
3. Tune the prominence parameter to match the minimum significant peak height you care about
```

### Scipy Module

Explore the `scipy` module for peak detection and signal processing

### Similar Research Papers

- Lecture Presentations Multimodal Dataset:
Towards Understanding Multimodality in Educational Videos - https://openaccess.thecvf.com/content/ICCV2023/papers/Lee_Lecture_Presentations_Multimodal_Dataset_Towards_Understanding_Multimodality_in_Educational_Videos_ICCV_2023_paper.pdf
- Automated analysis and indexing of lecture videos - https://dr.lib.iastate.edu/server/api/core/bitstreams/d970b9dd-4b3a-4ca8-b75b-645aa693413e/content
- SliTraNet: Automatic Detection of Slide Transitions in Lecture Videos
using Convolutional Neural Networks - https://openlib.tugraz.at/download.php?id=621f329186973&location=browse
- Content Based Lecture Video Retrieval Using
Speech and Video Text Information - https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6750040
- Content Based Lecture Video Retrieval Using
Speech and Video Text Information - https://ieeexplore.ieee.org/stamp/stamp.jsp?arnumber=6750040
- Investigating Correlations of Automatically Extracted
Multimodal Features and Lecture Video Quality - https://arxiv.org/pdf/2005.13876
-Lecture2Notes: Summarizing Lecture Videos by Classifying
Slides and Analyzing Text - https://haydenhousen.com/media/lecture2notes-paper-v1.pdf


### Duplicate Removal

- https://haydenhousen.com/media/lecture2notes-paper-v1.pdf

3.2.3 Duplicate Image Removal
The system uses a variety of methods to remove duplicate slides and obtain a set of unique frames containing
the best representation of each slide in the presentation. One method that is applied at various steps of the procedure
(during black border removal, perspective crop, and clustering) is image hashing. Standard hashing algorithms will
output completely different hashes on images that differ by one-byte but still depict the same content. Image hashing
algorithms produce similar output hashes given similar inputs. The system supports 4 hashing methods: average,
perception (the default), difference, and wavelet hashing. These algorithms analyze the image structure based on
luminance (without color information). This process will only remove extremely similar images and thus can safely be
applied without any false-positives. However, since the presenter moving slightly will cause the algorithm to detect two
unique images even though they contain the same slide, we employ clustering (see Section 3.2.4) and feature matching
(see Section 3.4.1) algorithms.

### Text Detection Algorithms
- EAST (Efficient and Accurate Scene Text Detector) [94] text
detection algorithm.
- You can use this to deny ocr on frames where there is no text

### Correction of the OCR Results
- All Tesseract outputs are spell checked with SymSpell [26], a symmetric delete
spelling correction algorithm
- https://haydenhousen.com/media/lecture2notes-paper-v1.pdf

### Peak Detection Algorithms
- Prominence is the answer
- https://github.com/MonsieurV/py-findpeaks gives comparison of different peak detection algorithms

### A Clustering Algorithm for Key Frame Extraction Based on Density Peak
- https://www.scirp.org/journal/paperinformation?paperid=89449

## Updates

### Update 22/09/2024

![image](https://github.com/user-attachments/assets/36aaa0f5-b690-48c2-8d78-7e86e5688b66)

- Created `pipe_v2.py` to modularize logic
- The OCR part is now made swappable
- Currently supporting `tesseract` and `easyocr`
- Way better results that previous `peak_frames` method
- Before -> 19 frames | After -> 16 frames

  ![image](https://github.com/user-attachments/assets/7a06f82c-ec3c-4ff6-b6b2-61e02df7f3cd)

### Update: Key Moments Strategy Added (13/10/2024)

- We all know that YouTube provides the key moments in the video. So, I thought why not use that to get the key moments in the video and then extract the frames from those key moments.
- Issues with this approach:

  - The key moments are not always accurate
  - The key moments are not always present
  - The key moments are not always present at the most informative frames

- ![alt text](images_for_readme/image-12.png)
  (left: key moments strategy, right: transactions strategy) \
  You can see here that the left one misses the most informative frames that the right one captures
