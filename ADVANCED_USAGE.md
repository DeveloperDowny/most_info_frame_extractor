# Advanced usage

This document covers power-user workflows: strategy tuning, caching, batch runs, and integration tips.

## Strategy selection

Available extraction strategies:

- `prominent_peaks`: detects peaks in OCR character count (good for slides).
- `k_transactions`: selects k transitions using a max-profit style optimization.
- `key_moments`: uses YouTube key moments when available.
- `timestamps`: extracts at specific seconds.
- `rate_change_threshold`: selects frames when character count jumps by a threshold.

Examples:

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --extraction=rate_change_threshold --threshold=15
```

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --extraction=timestamps --timestamps="30, 95.5, 120"
```

## Caching frames (avoid re-OCR)

Use `--cache-frames` to save processed frames to a pickle folder (`*_python_object`). You can then rerun with the `pickle` input to avoid re-running OCR.

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --cache-frames --no-cleanup
```

Then reuse cached frames:

```bash
ytvideo2pdf --input=pickle --dir="<internal_id>_python_object" --extraction=prominent_peaks
```

## Plotting the OCR signal

Enable plots to debug thresholds and strategy tuning:

```bash
ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E" --no-skip-plot --no-cleanup
```

Plots are saved under `<internal_id>_plot/`.

## Tuning frame sampling interval (Python)

The CLI samples frames every 3 seconds. In Python you can change this via the input strategy constructor:

```python
from ytvideo2pdf.input_strategy.youtube import YouTubeInput

strategy = YouTubeInput(
    video_url="https://youtu.be/Z_MLrbI1s2E",
    ocr_strategy=ocr_strategy,
    extraction_strategy=extraction_strategy,
    ocr_approval_strategy=approval_strategy,
    interval=2,
)
```

## Troubleshooting

- If OCR results are empty, verify Tesseract is installed and on PATH.
- If extraction returns too few frames, try `prominent_peaks` with a lower prominence or `rate_change_threshold` with a lower threshold.
- Use `--no-cleanup` to keep intermediate artifacts for debugging.
