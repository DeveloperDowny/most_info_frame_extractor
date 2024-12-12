## Flow of the project

Cloud Function receives YouTube link and email via a HTTP POST request
Save meta data to firestore
Create a task for video download and splitting in google queue
Out of many replica, one google compute instance picks up the task (let's call this replica A). It downloads the video and splits it into chunks and creates tasks and add to google queue. it also updates the db to save total number of chunks made, and initialized a variable number of chunks processed till now to zero
Out of many replics, one google compute instance picks up task and performs OCR on the video frames and saves result frame by frame in the db and increments the field number of chunks processed till now by one
The db has triggers to check when number of chunks processed till now becomes equal to total number of chunks for the video and then it creates a task for aggregating OCR result and performing extraction and adds to google queue
After this control goes back to A again and it aggregates the result, processes it, extracts the most informative frames and creates a PDF and sends it to the email

User enters youtube video link
The video is downloaded and split and distributed to multiple replica service

Steps performed at each replica service:
Video is ingested frame by frame
New frame is compared with the previous frame using the following algorithm
If the frames are almost the same, the frame is skipped
If the frames are different, ocr is performed on the frame (for skipped frames, the ocr result is the same as the previous frame)
Length of the text is calculated for each frame
This gives a signal where the quantity that varies over time is the length of the text

After each video segment is processed:
Aggregate the signal to make one long signal for the complete video
Use peak detection algorithm to detect the most informative frames
Extract those frames from the video
Make PDF of those frames
Store it

