
# URL Input
```bash
cd /home/vedant/Desktop/glimpsify/most_info_frame_extractor/
export PYTHONPATH=.
export BASE_DIR=/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives/playlist23/
export URL="https://www.youtube.com/watch?v=rKnD7rLT0lI"
python /home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py --input=youtube --url=${URL} --cleanup
```

# URL List of Playlist URL Input
```bash
cd /home/vedant/Desktop/glimpsify/most_info_frame_extractor/
export PYTHONPATH=.
export FOLDER_NAME=playlist23
export LOG_FILE_NAME="/home/vedant/Desktop/glimpsify/most_info_frame_extractor/logs/linkedin-sne.log"
export BASE_DIR=/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/archives/${FOLDER_NAME}
export URL="https://www.linkedin.com/safety/go?url=https%3A%2F%2Fyoutu.be%2FAPVCgkqWcQ4%3Fsi%3DGKqI7D7dUEhgcBOi&trk=flagship-messaging-web&messageThreadUrn=urn%3Ali%3AmessagingThread%3A2-NTBhOWRkZDYtZTUxNS00ZTVjLTkzN2YtZjViNDRiNDFmODU3XzEwMA%3D%3D&lipi=urn%3Ali%3Apage%3Ad_flagship3_messaging_conversation_detail%3B%2F6H6t2uIT7uERS6CyCWZxg%3D%3D"
python /home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/scripts/process_url_list.py --playlist-url=${URL}
```