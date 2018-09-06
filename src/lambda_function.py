import json

from webdriver_wrapper import WebDriverWrapper


def lambda_handler(event, context):
    url = event.get('queryStringParameters', {}).get('url', 'https://www.google.com/')
    print('Received url {} to parse'.format(url))

    driver = WebDriverWrapper()
    driver.get_url(url)

    first_title = driver.get_inner_html('(//h1)[1]') or 'nope'

    driver.close()

    return json.dumps({
        "isBase64Encoded": False,
        "statusCode": 200,
        "body": first_title
    })
