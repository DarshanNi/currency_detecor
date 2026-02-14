from __future__ import annotations

import re
from pathlib import Path

from flask import Flask, render_template, request
from PIL import Image
import pytesseract

app = Flask(__name__)
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Common INR denominations found on notes.
INR_DENOMINATIONS = [10, 20, 50, 100, 200, 500, 2000]


def detect_currency_from_image(image_path: Path) -> dict[str, str | int | None]:
    """Run OCR on image and infer currency + denomination from extracted text."""
    image = Image.open(image_path)
    ocr_text = pytesseract.image_to_string(image)
    normalized = " ".join(ocr_text.lower().split())

    currency = None
    if any(token in normalized for token in ["rupee", "rupees", "भारतीय", "रुपये", "india", "reserve bank"]):
        currency = "Indian Rupee (INR)"

    denomination = None
    for value in INR_DENOMINATIONS:
        if re.search(rf"\b{value}\b", normalized):
            denomination = value
            break

    # fallback: choose the first denomination-like number in OCR text
    if denomination is None:
        all_numbers = [int(num) for num in re.findall(r"\b\d{1,4}\b", normalized)]
        for num in all_numbers:
            if num in INR_DENOMINATIONS:
                denomination = num
                break

    return {
        "ocr_text": ocr_text.strip() or "(No text detected)",
        "currency": currency,
        "denomination": denomination,
    }


@app.route("/", methods=["GET", "POST"])
def index():
    result = None
    error = None

    if request.method == "POST":
        file = request.files.get("image")
        if not file or file.filename == "":
            error = "Please upload a currency image first."
        else:
            save_path = UPLOAD_DIR / file.filename
            file.save(save_path)
            try:
                result = detect_currency_from_image(save_path)
            except Exception as exc:  # pylint: disable=broad-except
                error = f"Could not process image: {exc}"

    return render_template("index.html", result=result, error=error)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
