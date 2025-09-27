import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

import pandas as pd


def process_video(row):
    internal_id, _, _, raw_timestamps = row

    # Skip invalid IDs
    if len(internal_id) != 6:
        return f"Skipped {internal_id}: Invalid ID length"

    try:
        # Process timestamps
        timestamps = eval(raw_timestamps)
        timestamps = list(map(str, timestamps))
        timestamps_str = ",".join(timestamps)

        # Prepare command
        args = [
            "python", "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/video2pdf/main.py",
            "--input=local",
            f"--dir={internal_id}",
            "--ocr=tesseract",
            "--extraction=timestamps",
            "--timestamps", timestamps_str,
            "--ocr_approval=reject_all"
        ]

        # Execute command
        result = subprocess.run(args, capture_output=True, text=True)

        if result.returncode == 0:
            return f"Success: {internal_id}"
        else:
            return f"Failed: {internal_id} - Return code: {result.returncode}"

    except Exception as e:
        return f"Exception for {internal_id}: {str(e)}"


def main():
    input_file = "/home/vedant/Desktop/glimpsify/most_info_frame_extractor/experiments/27/ref_timestamps_with_internal_id.csv"
    # Load your dataframe
    df = pd.read_csv(input_file)  # Replace with your actual data source

    # Get optimal number of workers (use all available CPU cores)
    max_workers = min(8, os.cpu_count())
    print(f"Running with {max_workers} workers")

    # Process videos in parallel
    results = []
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_video, row) for row in df.values]

        # Print progress
        total = len(futures)
        completed = 0

        for future in futures:
            result = future.result()
            results.append(result)
            completed += 1
            if completed % 10 == 0 or completed == total:
                print(f"Progress: {completed}/{total} ({completed / total * 100:.1f}%)")

    # Summarize results
    successes = sum(1 for r in results if r.startswith("Success"))
    failures = sum(1 for r in results if r.startswith("Failed"))
    skipped = sum(1 for r in results if r.startswith("Skipped"))
    exceptions = sum(1 for r in results if r.startswith("Exception"))

    print(f"\nSummary:")
    print(f"  Successful: {successes}")
    print(f"  Failed: {failures}")
    print(f"  Skipped: {skipped}")
    print(f"  Exceptions: {exceptions}")

    # Log detailed results
    with open("parallel_processing_log.txt", "w") as f:
        for result in results:
            f.write(f"{result}\n")


if __name__ == "__main__":
    main()
