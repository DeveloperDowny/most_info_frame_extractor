# 🎬 Glimpsify: Extract PPT Slides from any Educational Video

**A Video-to-PDF Frame Extraction Tool**

❌ Watch an entire 34 minutes long lecture video on YouTube? Naah 👎 \
✅ Get PDF notes of screenshots of important parts of the video instead? Hell yessss! 👌

That's what Glimpsify does! 💻

You pass it YouTube link 🔗 of the lecture video 🎥 and it gives you the PDF notes 📑 of the key parts of the video.
Yes with all the visuals - diagrams, charts, formulas - which no summarizer in the market gives!

See sample PDF: \
https://drive.google.com/drive/folders/1XOIjQs7dnYCBK1dg3ZzK8PPhx09H58-f?usp=drive_link

## Quick start

0. Tesseract OCR must be installed on your system for text detection to work.
   - For Windows, download the installer from [here](https://sourceforge.net/projects/tesseract-ocr.mirror/) and follow the installation instructions.
   - For macOS, you can install it using Homebrew:
     ```bash
     brew install tesseract
     ```
   - For Linux (Debian/Ubuntu), use the following command:
     ```bash
      sudo apt-get install tesseract-ocr
     ```
1. Install the package
   - `pip install ytvideo2pdf`
2. Run the CLI to get PDF notes
   - `ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E?si=ZrVBfIa0apzkuUKD"`

### 📚 Perfect For:

- **Students**: Creating last-minute revision PDFs from lecture videos
- **Educators**: Extracting slide content from recorded presentations
- **Researchers**: Analyzing visual content in educational materials
- **Professionals**: Converting training videos to reference documents
- **Content Creators**: Generating thumbnails and key moments

## LinkedIn Posts

I actively post on LinkedIn about my project. You can find link to the posts here:

- https://www.linkedin.com/posts/vedantpanchal_neso-academy-never-provides-their-ppts-activity-7254912964451811328-0a7H
- https://www.linkedin.com/posts/vedantpanchal_edtech-youtubesummarization-glimpsify-activity-7301972904718528512-LGoy

## Extracting Most Information Frame

Pass a YouTube Video link and get the screenshots of the frame which has the most information content (like if someone is explaining with the help of a PPT, capture screenshot when all the text of one slide of PPT has animated in)

Frame with most information it can possibly have
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/854332d4-5d59-4f11-aeff-e0fa0c8e1fcd)

This frame can have more information and thus not the most information frame
![image](https://github.com/DeveloperDowny/most_info_frame_extractor/assets/60831483/35eed63d-e490-441a-ab65-06ad336cb8aa)
