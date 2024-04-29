from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
from PIL import Image
import pytesseract
import os
import re
import smtplib
from email.mime.text import MIMEText

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
        
        return render_template('form.html', 
                               date=date.group(1) if date else "N/A", 
                               amount=amount.group(1) if amount else "N/A", 
                               receipt_no=receipt_no.group(1) if receipt_no else "N/A", 
                               description=description.group(1) if description else "N/A")
    else:
        return 'No receipt uploaded'

@app.route('/submit', methods=['POST'])
def submit_form():
    date = request.form.get('date')
    amount = request.form.get('amount')
    receipt_no = request.form.get('receipt_no')
    description = request.form.get('description')

    msg = MIMEText(f"Date: {date}\nAmount: {amount}\nReceipt No: {receipt_no}\nDescription: {description}")
    msg['Subject'] = 'Receipt Information'
    msg['From'] = 'checkrent757@gmail.com'
    msg['To'] = 'checkrent757@gmail.com'

    s = smtplib.SMTP('localhost')
    s.send_message(msg)
    s.quit()

    return 'Form submitted and email sent'

if __name__ == '__main__':
    app.run(debug=True, port=5001)