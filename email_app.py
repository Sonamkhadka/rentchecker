from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os
import re

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'receipt' in request.files:
        receipt = request.files['receipt']
        filename = secure_filename(receipt.filename)
        upload_path = os.path.join(os.getcwd(), 'uploads', filename)
        receipt.save(upload_path)
        
        img = Image.open(upload_path)
        text = pytesseract.image_to_string(img)
        date_pattern = r'Date: (\d{2}/\d{2}/\d{4})'
        amount_pattern = r'Amount: (\d+\.\d{2})'
        receipt_no_pattern = r'Receipt No: (\d+)'
        description_pattern = r'Description: (.*)'
        
        date = re.search(date_pattern, text)
        amount = re.search(amount_pattern, text)
        receipt_no = re.search(receipt_no_pattern, text)
        description = re.search(description_pattern, text)
        
        return render_template('receipt.html', 
                               date=date.group(1) if date else "N/A", 
                               amount=amount.group(1) if amount else "N/A", 
                               receipt_no=receipt_no.group(1) if receipt_no else "N/A", 
                               description=description.group(1) if description else "N/A")
    else:
        return 'No receipt uploaded'

if __name__ == '__main__':
    app.run(debug=True, port=5001)