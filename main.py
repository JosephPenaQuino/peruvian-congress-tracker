"""

Example to install tesseract:
https://medium.com/@ahmedbr/how-to-implement-pytesseract-properly-d6e2c2bc6dda
"""
import re
import pdfplumber
import pytesseract
from PIL import Image
import pandas as pd
import os

# Function to perform OCR on an image
# def ocr_image(image_path):
#     return pytesseract.image_to_string(Image.open(image_path))

# Open the PDF file
# with pdfplumber.open("data/output-page1.pdf") as pdf:
#     # Initialize lists to store OCR output
#     ocr_text = []

#     # Extract images from all pages and perform OCR
#     for page in pdf.pages:
#         for i, image in enumerate(page.images):
#             image_path = f"page_{page.page_number}_image_{i}.png"
#             image_obj = page.to_image(resolution=300)
#             image_obj.save(image_path)
#             ocr_text.append(ocr_image(image_path))
#             os.remove(image_path)

# save ocr_text
# with open("ocr_text.txt", "w") as file:
#     file.write("\n".join(ocr_text))

# load ocr_text
with open("ocr_text.txt", "r") as file:
    ocr_text = file.readlines()

# Combine OCR text from all pages into a single string
text = '\n'.join(ocr_text)

# Split text into lines
lines = text.split('\n')

# Initialize lists to store table data
data = []

save = False

# Iterate through lines to extract table data
for line in lines:
    # Split line into columns based on the delimiter (e.g., tab or comma)
    if line.strip() == "":
        continue
    if "ACUNA PERALTA" in line:
        save = True
    if "Resultados de la ASISTENCIA" in line:
        save = False
    if not save:
        continue

    columns = re.split(r'(PRE|aus|LO|LE)', line)
    columns = [columns[i] + columns[i+1] for i in range(0, len(columns)-1, 2)]

    # If the line has three columns, consider it as part of the table
    print(columns)
    for column in columns:
        row = column.split(" ")
        data.append([row[0], " ".join(row[1:-1]), row[-1]])

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['Column 1', 'Column 2', 'Column 3'])

# Write DataFrame to CSV
df.to_csv('output.csv', index=False)
