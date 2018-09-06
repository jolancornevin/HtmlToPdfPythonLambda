import logging
import json

from webdriver_wrapper import WebDriverWrapper


logger = logging.getLogger()


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

    driver = WebDriverWrapper()
    driver.get_url(url)

    first_title = driver.get_inner_html('(//h1)[1]') or 'nope'

    driver.close()

    return json.dumps({
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": first_title
    })
