from flask import Flask, request, jsonify
import source_code as sc

app = Flask(__name__)

@app.route('/api', methods=['GET'])
def main():
    result = {'syntaxValidation': '', 'MXRecord': '', 'smtpConnection': '', 'is Temporary': ''}
    email = str(request.args['Query'])

    # Syntax validation
    result['syntaxValidation'] = sc.is_valid_email(email)

    if result['syntaxValidation']:
        # MX record validation
        result['MXRecord'] = sc.has_valid_mx_record(email.split('@')[1])

        # SMTP validation
        if result['MXRecord']:
            result['smtpConnection'] = sc.verify_email(email)
        else:
            result['smtpConnection'] = False

        # Temporary domain check
        result['is Temporary'] = sc.is_disposable(email.split('@')[1])

    else:
        result['MXRecord'] = False
        result['smtpConnection'] = False
        result['is Temporary'] = False

    return jsonify(result)  # Return the result dictionary as JSON

if __name__ == '__main__':
    app.run(debug=True)