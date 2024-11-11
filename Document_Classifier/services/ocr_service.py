from PIL import Image
import pytesseract
import logging

logger = logging.getLogger(__name__)

class OCRService:
    def perform_ocr(self, file):
        try:
            logger.info("Performing OCR on the provided image file")
            img = Image.open(file)
            text = pytesseract.image_to_string(img)
            return text
        except Exception as e:
            logger.error("Error occurred during OCR processing", exc_info=True)
            raise e

import http.client

conn = http.client.HTTPSConnection("weatherbit-v1-mashape.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "Sign Up for Key",
    'x-rapidapi-host': "weatherbit-v1-mashape.p.rapidapi.com"
}

conn.request("GET", "/current?lon=80.053543&lat=12.82136&units=imperial&lang=en", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))