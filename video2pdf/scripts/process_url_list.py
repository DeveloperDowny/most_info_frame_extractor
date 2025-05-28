import subprocess
import time

# from video2pdf.utils.helper import Helper
from video2pdf.utils.helper import Helper


# from video2pdf.utils.helper import Helper


def main(urls):
    for url in urls:
        try:
            subprocess.run(["python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
                            "--input=youtube", f"--url={url}", "--cleanup"])
            time.sleep(10)
        except:
            print("Exception occurred for: ", url)


if __name__ == "__main__":
    playlist_url = "https://youtube.com/playlist?list=PLHENddstfsnpEHBWgt9yddEVDfcpQdUg7&si=t0DCVsJaguKzBoPP"
    # playlist_url = "https://youtube.com/playlist?list=PL4gu8xQu0_5KiYnRlueicckEmpFAiRD5Y&si=XeTFcmjXdbE4irJW"
    urls = Helper.get_video_urls_from_playlist(playlist_url)
    # urls = ["https://www.youtube.com/watch?v=j2-9yymHfeU&list=TLGGEGsAE2D2xJgxNTA1MjAyNQ"]
    # urls = urls[:1]
    main(urls)
