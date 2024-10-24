import urllib
import json
from promptflow import tool
from promptflow.connections import CustomConnection
import requests

def chat(question: str, context:str, connection: CustomConnection) -> str:
    
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
                {"role": "user", "content": "You are an AI assistant who helps people find information. As the assistant, you answer questions not long, simple, short. Add a witty joke that begins with By the way, or By the way. The joke should be related to the specific question asked. For example, if the question is about tents, the joke should be specifically related to tents."},
                {"role": "user", "content": "Use the following context to provide a more personalized response to the customer:"},
                {"role": "user", "content": context},
                {"role": "user", "content": "tell me about your TrailMaster X4"},
                {"role": "assistant", "content": "The TrailMaster X4 is a rugged four-wheel off-road vehicle with a powerful engine and durable frame. "},
                {"role": "user", "content": question},
                {"role": "user", "content": "Answer in Korean language."},
                
            ],
        "parameters": {
                "temperature": 0.7,
                "max_new_tokens": 1024,
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
def my_python_tool(question: str, context:str, connection: CustomConnection) -> str:
    """
    Tool function to process input data and query the Phi-3 model.
    """
    return chat(question, context, connection)