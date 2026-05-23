@echo off
rmdir /s /q dist
python -m build
python -m twine upload --repository ytvideo2pdf dist/* --config .pypirc.local
