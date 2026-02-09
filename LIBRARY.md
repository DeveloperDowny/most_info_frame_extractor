# Python API reference

This library is primarily designed as a CLI, but you can call the core pipeline from Python. The programmatic API uses strategy factories and input strategies that mirror CLI behavior.

## Install

```bash
pip install ytvideo2pdf
```

## Minimal programmatic usage

```python
from ytvideo2pdf.enums import ExtractionType, OCRApprovalType, OCRType
from ytvideo2pdf.extraction_strategy.extraction_strategy_factory import ExtractionStrategyFactory
from ytvideo2pdf.ocr_strategy.ocr_strategy_factory import OCRStrategyFactory
from ytvideo2pdf.ocr_approval.factory import OCRApprovalStrategyFactory
from ytvideo2pdf.input_strategy.factory import InputStrategyFactory

ocr_strategy = OCRStrategyFactory.create_ocr_strategy(OCRType.TESSERACT.value)
extraction_strategy = ExtractionStrategyFactory.create_extraction_strategy(
    ExtractionType.PROMINENT_PEAKS
)
approval_strategy = OCRApprovalStrategyFactory.create_strategy(
    OCRApprovalType.PHASH
)

input_strategy = InputStrategyFactory.create_input_strategy(
    "youtube",
    ocr_strategy,
    extraction_strategy,
    approval_strategy,
    url="https://youtu.be/Z_MLrbI1s2E",
    cache_frames=False,
    skip_plot=True,
    metadata={},
)

internal_id = input_strategy.process()
print("Internal ID:", internal_id)
```

### Return value

`process()` returns an `internal_id` string (the working directory under `data/`). The PDF and metadata JSON are copied to `output/` in the current working directory.

## Core modules

### Enums

- `ytvideo2pdf.enums.ExtractionType`
  - `k_transactions`, `key_moments`, `timestamps`, `prominent_peaks`, `rate_change_threshold`
- `ytvideo2pdf.enums.OCRType`
  - `tesseract`, `easy_ocr`, `paddleocr`
- `ytvideo2pdf.enums.OCRApprovalType`
  - `phash`, `pixel_comparison`, `approve_all`, `reject_all`

### Factories

- `ExtractionStrategyFactory.create_extraction_strategy(extraction_type, **kwargs)`
  - `extraction_type` can be an enum or a string value.
  - `timestamps` and `threshold` are passed via `**kwargs` for the relevant strategies.
- `OCRStrategyFactory.create_ocr_strategy(ocr_type)`
  - `ocr_type` should be a string: `"tesseract" | "easy_ocr" | "paddleocr"`.
- `OCRApprovalStrategyFactory.create_strategy(approval_type)`
  - `approval_type` can be an enum or string value.

### Input strategies

Use the input strategy to load a YouTube video, local file, or cached frames.

- `YouTubeInput(video_url, ocr_strategy, extraction_strategy, ocr_approval_strategy, interval=3, ...)`
- `LocalFileInput(directory, ocr_strategy, extraction_strategy, ocr_approval_strategy, interval=3, ...)`
- `PickleInput(directory, ocr_strategy, extraction_strategy, ...)`

Create these via `InputStrategyFactory.create_input_strategy(...)`.

### Output artifacts

- `output/<video_name>.pdf`
- `output/<video_name>.json`
- Intermediate folders under `data/` (unless cleanup is enabled in CLI).

The JSON includes metadata such as extracted frame numbers, timestamps, and paths to artifacts.

## Notes

- OCR requires an external engine. Tesseract is the default. EasyOCR and PaddleOCR require their extra packages.
- The Python API is not yet versioned separately from the CLI. Minor releases may adjust behavior.
