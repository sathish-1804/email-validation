# from flask import Flask, request, jsonify, send_file
# import csv
# from tempfile import NamedTemporaryFile
# import shutil
# import pandas as pd
# import source_code as sc
#
# app = Flask(__name__)
#
# ALLOWED_EXTENSIONS = {'csv', 'txt', 'xlsx'}
#
# def allowed_file(filename):
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
#
# def label_email(email):
#     if not sc.is_valid_email(email):
#         return "Invalid"
#     if not sc.has_valid_mx_record(email.split('@')[1]):
#         return "Invalid"
#     if not sc.verify_email(email):
#         return "Unknown"
#     if sc.is_disposable(email.split('@')[1]):
#         return "Risky"
#     return "Valid"
#
# def label_emails(input_file):
#     file_extension = input_file.split('.')[-1].lower()
#
#     if file_extension == 'csv':
#         return process_csv(input_file)
#     elif file_extension == 'txt':
#         return process_txt(input_file)
#     elif file_extension == 'xlsx':
#         return process_xlsx(input_file)
#     else:
#         raise ValueError("Unsupported file format. Please provide a CSV, TXT, or XLSX file.")
#
# def process_csv(input_file):
#     with open(input_file, 'r') as csvfile, \
#             NamedTemporaryFile(mode='w', delete=False) as temp_file:
#         reader = csv.reader(csvfile)
#         writer = csv.writer(temp_file)
#
#         # Write the header row to the output file
#         writer.writerow(['Email', 'Label'])
#
#         # Process each row in the input file
#         for row in reader:
#             email = row[0].strip()
#             label = label_email(email)
#             writer.writerow([email, label])
#
#     # Replace the input file with the output file
#     output_file = 'Output file.csv'
#     shutil.move(temp_file.name, output_file)
#     return output_file
#
# def process_txt(input_file):
#     with open(input_file, 'r') as txtfile, \
#             NamedTemporaryFile(mode='w', delete=False) as temp_file:
#         writer = csv.writer(temp_file)
#
#         # Write the header row to the output file
#         writer.writerow(['Email', 'Label'])
#
#         # Process each line in the input file
#         for line in txtfile:
#             email = line.strip()
#             label = label_email(email)
#             writer.writerow([email, label])
#
#     # Replace the input file with the output file
#     output_file = 'Output file.csv'
#     shutil.move(temp_file.name, output_file)
#     return output_file
#
# def process_xlsx(input_file):
#     df = pd.read_excel(input_file, header=None, names=['Email'])
#     df['Label'] = df['Email'].apply(label_email)
#     output_file = 'Output file.xlsx'
#     df.to_excel(output_file, index=False)
#     return output_file
#
# @app.route('/process_file', methods=['POST'])
# def process_file():
#     # Check if the 'file' key exists in the request
#     if 'file' not in request.files:
#         return jsonify({'error': 'No file provided'}), 400
#
#     file = request.files['file']
#     if file.filename == '':
#         return jsonify({'error': 'Empty filename'}), 400
#
#     if not allowed_file(file.filename):
#         return jsonify({'error': 'Invalid file format. Only CSV, TXT, and XLSX files are allowed.'}), 400
#
#     try:
#         # Save the uploaded file to a temporary location
#         temp_file = NamedTemporaryFile(delete=False)
#         file.save(temp_file.name)
#
#         # Process the file
#         output_file5 = label_emails(temp_file.name)
#
#         # Return the processed file
#         return send_file(output_file5, as_attachment=True)
#
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500
#
# if __name__ == '__main__':
#     app.run()

import csv
from tempfile import NamedTemporaryFile
import shutil
import pandas as pd
import source_code as sc

def label_email(email):
    if not sc.is_valid_email(email):
        return "Invalid"
    if not sc.has_valid_mx_record(email.split('@')[1]):
        return "Invalid"
    if not sc.verify_email(email):
        return "Unknown"
    if sc.is_disposable(email.split('@')[1]):
        return "Risky"
    return "Valid"

def label_emails(input_file):
    file_extension = input_file.split('.')[-1].lower()

    if file_extension == 'csv':
        process_csv(input_file)
    elif file_extension == 'xlsx':
        process_xlsx(input_file)
    elif file_extension == 'txt':
        process_txt(input_file)
    else:
        print("Unsupported file format. Please provide a CSV, XLSX, or TXT file.")

def process_csv(input_file):
    with open(input_file, 'r') as csvfile, \
            NamedTemporaryFile(mode='w', delete=False) as temp_file:
        reader = csv.reader(csvfile)
        writer = csv.writer(temp_file)

        # Write the header row to the output file
        writer.writerow(['Email', 'Label'])

        # Process each row in the input file
        for row in reader:
            email = row[0].strip()
            label = label_email(email)
            writer.writerow([email, label])

    # Replace the input file with the output file
    shutil.move(temp_file.name, 'Output file.csv')

def process_xlsx(input_file):
    df = pd.read_excel(input_file)
    df['Label'] = df['Email'].apply(label_email)
    df.to_excel('Output file.xlsx', index=False)

def process_txt(input_file):
    with open(input_file, 'r') as txtfile, \
            NamedTemporaryFile(mode='w', delete=False) as temp_file:
        writer = csv.writer(temp_file)

        # Write the header row to the output file
        writer.writerow(['Email', 'Label'])

        # Process each line in the input file
        for line in txtfile:
            email = line.strip()
            label = label_email(email)
            writer.writerow([email, label])

    # Replace the input file with the output file
    shutil.move(temp_file.name, 'Output file.csv')

# Example usage:
# label_emails('EmailList1.csv')  # CSV file
# label_emails('Email List2.xlsx')  # XLSX file
label_emails('Email List3.txt')  # TXT file
