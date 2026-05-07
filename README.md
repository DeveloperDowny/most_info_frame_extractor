# Glimpsify (ytvideo2pdf)

Glimpsify extracts slide-like frames from educational videos and builds a PDF of the key visuals (diagrams, formulas, charts). It is optimized for lecture-style videos where text appears on screen over time.

## Demo
Try it out here: https://colab.research.google.com/drive/1xz6uHeY0QAzMTR8DbXJY8BSvNmKhI24Q?usp=sharing

## Quick start

1. Install OCR engine (required for text detection)
   - Windows: install Tesseract OCR and make sure `tesseract` is on PATH.
   - macOS: `brew install tesseract`
   - Debian/Ubuntu: `sudo apt-get install tesseract-ocr`

2. Install the package

```bash
pip install ytvideo2pdf
```

3. Run the CLI

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E"
```

## Common usage

Extract from a local folder (expects a single video file in the directory):

```bash
ytvideo2pdf --input=local --dir="C:\path\to\video_dir"
```

Run with a specific extraction strategy:

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --extraction=prominent_peaks
```

Extract a fixed number of frames:

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --k=10
```

Extract frames at explicit timestamps (seconds):

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --extraction=timestamps --timestamps="30, 95.5, 120"
```

## What you get

- A PDF file in `output/` with the extracted frames.
- A JSON metadata file alongside the PDF (same name, `.json`).
- Intermediate folders (unless `--no-cleanup`) for extracted frames and cached objects.

## Key features

- Multiple extraction strategies to pick the most informative frames.
- OCR-based signal processing (Tesseract by default).
- Optional caching of processed frames for reuse.
- Optional plots of the OCR signal (for debugging and tuning).

## CLI options (summary)

- `--input`: `youtube | local | pickle`
- `--url`: YouTube video or playlist URL (for `youtube` input)
- `--dir`: local directory path (for `local` or `pickle` input)
- `--ocr`: `tesseract | easy_ocr | paddleocr`
- `--ocr_approval`: `phash | pixel_comparison | approve_all | reject_all`
- `--extraction`: `prominent_peaks | k_transactions | key_moments | timestamps | rate_change_threshold`
- `--k`: number of frames to extract, or `auto`
- `--timestamps`: comma-separated seconds (for `timestamps` extraction)
- `--threshold`: integer threshold for `rate_change_threshold`
- `--cache-frames/--no-cache-frames`
- `--skip-plot/--no-skip-plot`
- `--cleanup/--no-cleanup`

For Python API usage, see `LIBRARY.md`.
