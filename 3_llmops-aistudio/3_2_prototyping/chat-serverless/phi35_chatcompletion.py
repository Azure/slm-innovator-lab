import urllib
import json
from promptflow import tool
from promptflow.connections import CustomConnection
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from urllib.parse import urlparse, urlunparse

def chat(deployment_name:str, question: str, context:str, connection: CustomConnection) -> str:
    
    # Request data goes here
    # The example below assumes JSON formatting which may be updated
    # depending on the format your endpoint expects.
    # More information can be found here:
    # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
    endpoint_url = connection.endpoint
    parsed_url = urlparse(endpoint_url)
    new_url = urlunparse((parsed_url.scheme, parsed_url.netloc, '/models', '', '', ''))

    api_key = connection.key
    

    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")

    try:
        client = ChatCompletionsClient(
            endpoint=new_url, # you will run into a 500 error if you use this endpoint
            credential=AzureKeyCredential(api_key)
        )
        

        response = client.complete(
            messages=[
                SystemMessage(content="""
                You are an AI assistant who helps people find information. As the assistant, you answer questions not long, simple, short.
                Use the following context to provide a more personalized response to the customer. 
                """),

            
                UserMessage(content=f"""
                Context: {context}
                Question: {question}
                """),
            ],
            # Simply change the model name for the appropiate model "Phi-3.5-mini-instruct" or "Phi-3.5-vision-instruct"
            model=deployment_name, 
            temperature=0.8,
            max_tokens=256
        )

        result = response.choices[0].message.content
        return result
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

@tool
def my_python_tool(deployment_name:str, question: str, context:str, connection: CustomConnection) -> str:
    """
    Tool function to process input data and query the Phi-3 model.
    """
    return chat(deployment_name, question, context, connection)
