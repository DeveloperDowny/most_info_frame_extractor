<details open>
<summary>It's complex how videos are stored!</summary>
Videos are saved as a sequence of compressed images (frames) bundled together in a container format like MP4, MKV, or AVI. Alongside these images, additional data like audio tracks, subtitles, and metadata are stored in the same file. Let's break this down:

### 1. **Video Encoding and Storage**
   - **Frames**: Videos are essentially a sequence of images called frames. These are compressed using codecs like H.264 or H.265 to reduce file size while maintaining quality.
   - **Keyframes (I-frames)**: These are full, standalone images in the video stream. Other frames depend on keyframes for rendering.
   - **Delta Frames (P-frames and B-frames)**: These contain only the changes from the previous or future frames to save space. For example, if most of the scene is static, only the moving parts are encoded.

### 2. **How Seeking Works**
   - Videos are indexed by keyframes. When you seek to a particular timestamp or frame number:
     - The player finds the nearest preceding keyframe (I-frame).
     - It decodes from that keyframe up to your desired frame.
   - This is why seeking to an arbitrary frame often requires decoding multiple frames.

### 3. **Downloading Specific Frames**
   - **Frame Number to Timestamp**: You need to calculate the timestamp corresponding to the frame number. For example:
     \[
     \text{Time (in seconds)} = \frac{\text{Frame Number}}{\text{Frame Rate (FPS)}}
     \]
   - **Request Partial Content**: Video files support partial content requests using HTTP range headers. If the server allows it, you can fetch only the parts of the file containing your desired keyframe and decode it locally.

### 4. **Challenges in Downloading a Specific Frame**
   - **Precision**: Since most frames (P and B-frames) depend on other frames, you may need to download and decode more than just the target frame.
   - **Server Capabilities**: Not all servers support partial content requests. Streaming platforms often use DRM or proprietary protocols to prevent direct frame-level access.
   - **Tool/Library Support**: You would need software or libraries capable of seeking and extracting frames (e.g., FFmpeg).

### 5. **Possible Solutions**
   - **Use FFmpeg**: You can extract a specific frame programmatically:
     ```bash
     ffmpeg -i video.mp4 -vf "select=eq(n\,FRAME_NUMBER)" -vframes 1 output.jpg
     ```
   - **Stream APIs**: For some streaming services, APIs might allow fetching a specific segment of the video for frame extraction.

Would you like to explore practical examples or tools to achieve this?
</details>