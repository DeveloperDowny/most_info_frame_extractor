# Contributing

Thanks for contributing. This project is a Python package with a Typer-based CLI.

## Development setup

1. Create a virtual environment (Python 3.9+).
2. Install editable dependencies:

```bash
pip install -e .
```

Optional OCR backends:

```bash
pip install -e ".[easyocr]"
pip install -e ".[paddleocr]"
```

Tesseract is required for the default OCR strategy.

## Running the CLI locally

```bash
python -m ytvideo2pdf --input=youtube --url="https://youtu.be/Z_MLrbI1s2E"
```

## Project layout

- `src/ytvideo2pdf/main.py`: CLI entrypoint and option parsing.
- `src/ytvideo2pdf/input_strategy/`: input sources (YouTube, local, pickle).
- `src/ytvideo2pdf/extraction_strategy/`: frame selection strategies.
- `src/ytvideo2pdf/ocr_strategy/`: OCR engines.
- `src/ytvideo2pdf/ocr_approval/`: OCR approval/dedup strategies.
- `src/ytvideo2pdf/utils/`: utilities and pipeline helpers.

## Outputs and artifacts

The pipeline writes to:

- `data/`: working directories and intermediate artifacts.
- `output/`: final PDF and JSON metadata.

Do not commit generated outputs or large media files.

## Coding guidelines

- Keep logic in `src/ytvideo2pdf` and avoid adding side effects to import paths.
- Prefer small, testable functions with clear inputs/outputs.
- When adding new strategies, update the factories and enums.
