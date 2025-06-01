
# URL Input
```bash
cd /home/vedant/Desktop/glimpsify/most_info_frame_extractor/
export PYTHONPATH=.
export FOLDER_NAME=docloader
export LOG_FILE_NAME="/home/vedant/Desktop/glimpsify/most_info_frame_extractor/logs/for-doc-loader.log"
export BASE_DIR=/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives/${FOLDER_NAME}
export URL="https://www.youtube.com/watch?v=6mSx_KJxcHI"
python /home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py --input=youtube --url=${URL}
```

python /home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py --input=youtube --url=${URL} --cleanup

# URL List of Playlist URL Input
```bash
cd /home/vedant/Desktop/glimpsify/most_info_frame_extractor/
export PYTHONPATH=.
export FOLDER_NAME=playlist23
export LOG_FILE_NAME="/home/vedant/Desktop/glimpsify/most_info_frame_extractor/logs/linkedin-sne.log"
export BASE_DIR=/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives/${FOLDER_NAME}
export URL="https://youtube.com/playlist?list=PLBlnK6fEyqRgMCUAG0XRw78UA8qnv6jEx&si=JkXp2HB8fbVASCf1"
python /home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/scripts/process_url_list.py --playlist-url=${URL}
```