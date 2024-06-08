# Email Validation Tool
This is a Streamlit application for email validation. The tool allows users to verify the validity of email addresses and analyze email-related data.

## Features:
**Single Email Verification**: Users can enter an email address to check its validity. The tool performs syntax validation, checks MX records, establishes SMTP connection, and checks if the domain is a temporary one. The result is displayed along with key metrics like syntax validation, MX record status, and temporary domain status.

**Bulk Email Processing**: Users can upload a CSV, XLSX, or TXT file containing a list of email addresses. The tool processes each email in the file and performs validation similar to single email verification. After processing, users can download the results, including email addresses and their validation labels.

**Domain Information**: For valid email addresses, the tool provides additional domain information such as registrar, server, and country using the WHOIS database.

## Installation
To run the Email Validation Tool locally, follow these steps:

```
Clone the repository:
git clone https://github.com/sathish-1804/email_validation_tool.git

Change the directory to the cloned repository:
cd email_validation_tool

Install the required dependencies:
pip install -r requirements.txt
```

To launch the Email Validation Tool, run the following command:
```
streamlit run main.py
```

The tool will be accessible at http://localhost:8501 in your web browser.

**Note**: 
- The tool performs email validation using various methods such as syntax validation, MX record checks, and SMTP connection.
- Bulk email processing allows users to upload a file and process multiple email addresses simultaneously.
- Domain information retrieval is provided through the WHOIS database for valid email addresses.
- The tool's functionality can be customized or extended based on specific requirements.
- Ensure that the data source (CSV, XLSX, or TXT file) contains the necessary columns for processing.
