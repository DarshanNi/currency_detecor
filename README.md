# Currency Detector (Python + Flask)

A small Python web app that detects Indian currency note denomination from an uploaded image.

## Features
- Upload a note image from browser.
- OCR text extraction using `pytesseract`.
- Detects if note is likely Indian Rupee (INR).
- Infers denomination (₹10, ₹20, ₹50, ₹100, ₹200, ₹500, ₹2000).

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Ensure Tesseract OCR is installed on your OS:
> - Ubuntu/Debian: `sudo apt-get install tesseract-ocr`
> - Mac: `brew install tesseract`

## Run
```bash
python app.py
```

Open: `http://127.0.0.1:5000`

## Example output
If image is a valid ₹200 note, app should show:
- **Currency:** Indian Rupee (INR)
- **Denomination:** ₹200

## Notes
- OCR accuracy depends on image quality.
- If detection fails, try a clearer image with visible denomination text.
