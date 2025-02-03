import requests
import json
from API_Automation.E2E_Framework.logger_config import logger

def getDATA(url):
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }

    logger.info(f"Sending GET request to: {url}")
    try:
        response = requests.get(url, headers=headers)
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending GET request: {e}")
        raise

def postDATA(url, body):
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }

    logger.info(f"Sending POST request to: {url}")
    logger.info(f"Request Body: {json.dumps(body)}")

    try:
        response = requests.post(url, json=body, headers=headers)
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending POST request: {e}")
        raise


def putDATA(url, body):
    headers = {
        "Content-Type": "application/json",
        "accept": "*/*"
    }

    try:
        response = requests.put(url, json=body, headers=headers)
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Response Body: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending PUT request: {e}")
        raise


def patchDATA(url, body):
    headers = {
        "Content-Type": "application/json",
        "Accept": "*/*"
    }

    logger.info(f"Sending PATCH request to: {url}")
    logger.info(f"Request Body: {json.dumps(body, indent=2)}")

    try:
        response = requests.patch(url, json=body, headers=headers)
        logger.info(f"Response Status Code: {response.status_code}")
        logger.info(f"Raw Response Body: {response.text}")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"Error while sending PATCH request: {e}")
        raise


def validate_response_code(response, client_email):
    if response.status_code == 500:
        raise ValueError(f"Received status code 500 from the server for {client_email}.")
    if response.status_code not in [200, 201]:
        logger.warning(f"Non-200/201 status code received for {client_email}: {response.status_code}")
