import base64
import logging
import json

import pdfkit


logger = logging.getLogger()

configuration = pdfkit.configuration(wkhtmltopdf='./bin/vendor/wkhtmltopdf')


def error(title):
    """
    Return a valid API Gateaway error response.
    """
    logger.error(title)

    return json.dumps({
        "isBase64Encoded": False,
        "statusCode": 403,
        "body": title
    })


def lambda_handler(event, context):
    url = event.get('queryStringParameters', {}).get('url')

    if not url:
        return error("You must provide a GET url parameter")

    logger.info('Received url {} to parse'.format(url))

    pdf_file_from_url = pdfkit.from_url(url, False, configuration=configuration)

    return {
        "statusCode": 200,
        "body": base64.b64encode(pdf_file_from_url).decode('ascii'),
        "isBase64Encoded": True,
        "headers": {
            "Accept": "application/pdf",
            "Content-Type": "application/pdf",
            "Content-disposition": "attachment; filename=\"test_generation.pdf\""
        }
    }
