import requests
import uuid
import utils.api as api

# Add your key and endpoint
key = api.azure_key
endpoint = "https://api.cognitive.microsofttranslator.com"

# location, also known as region.
# required if you're using a multi-service or regional (not global) resource. It can be found in the Azure portal on the Keys and Endpoint page.
location = "eastasia"

path = '/translate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'from': 'en',
    'to': 'zh-Hans'
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}


def translate_by_azure(text: str):
    """返回微软 Azure 英译中结果

    Args:
        text (str): 原文

    Returns:
        str: 译文
    """
    # You can pass more than one object in body.
    body = [{'text': text}]

    response = requests.post(
        constructed_url, params=params, headers=headers, json=body).json()

    return response[0]['translations'][0]['text']


def translate_to_en_by_azure(text: str):
    """返回微软 Azure 中译英结果

    Args:
        text (str): 原文

    Returns:
        str: 译文
    """
    # You can pass more than one object in body.
    body = [{'text': text}]

    params2 = {
        'api-version': '3.0',
        'from': 'zh-Hans',
        'to': 'en'
    }

    response = requests.post(
        constructed_url, params=params2, headers=headers, json=body).json()

    return response[0]['translations'][0]['text']
