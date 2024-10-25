import urllib
import json
from promptflow import tool
from promptflow.connections import CustomConnection
import requests

def chat(input_data: str, connection: CustomConnection) -> str:
    
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    endpoint_url = connection.endpoint
    api_key = connection.key
    

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = {
        "messages": 
            [
                {"role": "user", "content": "Tell me Microsoft's brief history."},
                {"role": "assistant", "content": "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell a BASIC interpreter for the Altair 8800."},
                {"role": "user", "content": input_data},
                {"role": "user", "content": "Keep the answer simple."},
            ],
        "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 256,
                "do_sample": True,
                "return_full_text": False
        }
    }

    try:
        response = requests.post(endpoint_url, json=data, headers=headers)
        response.raise_for_status()
        result = response.json()
        result = result["choices"][0]['message']['content']
        return result
    except requests.exceptions.RequestException as e:
        print(e)
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

@tool
def my_python_tool(input_data: str, connection: CustomConnection) -> str:
    """
    Tool function to process input data and query the Phi-3 model.
    """
    return chat(input_data, connection)