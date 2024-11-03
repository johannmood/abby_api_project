import requests
import os
import logging

# Configure logging for detailed debug information
logging.basicConfig(level=logging.DEBUG)

# Base URL for the Render-hosted API
BASE_URL = os.getenv("ABBY_API_URL", "https://abby-api.onrender.com")

def ask_abby(user_id, message):
    """
    Sends a message to the ABBY API and returns the response.

    Parameters:
    - user_id (str): The unique identifier for the user.
    - message (str): The message to send to ABBY.

    Returns:
    - dict: Response from ABBY API if successful.
    - None: If there's an error.
    """
    endpoint = f"{BASE_URL}/ask_abby"
    headers = {"Content-Type": "application/json"}
    payload = {
        "user_id": user_id,
        "message": message
    }

    try:
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()  # Raise an error for bad status codes
        logging.debug(f"Response received: {response.json()}")
        return response.json()  # Return the JSON response as a dictionary

    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        logging.error(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        logging.error(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        logging.error(f"An error occurred: {req_err}")

    return None  # Return None if any error occurs

# Example usage
if __name__ == "__main__":
    user_id = "user123"
    message = "Hello, ABBY! What can I do in Berlin today to connect with like-minded people?"

    # Call the ask_abby function and print the response
    response = ask_abby(user_id, message)
    if response:
        print(f"ABBY's response: {response['response']}")
    else:
        print("Failed to get a response from ABBY.")