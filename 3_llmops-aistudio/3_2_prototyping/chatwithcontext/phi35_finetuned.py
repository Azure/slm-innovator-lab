import urllib
import json
from promptflow import tool
from promptflow.connections import CustomConnection


def chat(question: str, context: str, connection: CustomConnection) -> str:
    
    # More information can be found here:
    # https://learn.microsoft.com/en-us/azure/ai-studio/how-to/deploy-models-phi-3?WT.mc_id=aiml-137032-kinfeylo&tabs=phi-3-5&pivots=programming-language-rest 
    # Phi-3.5-Mini-Instruct, Phi-3.5-MoE-Instruct, Phi-3-mini-4k-Instruct, Phi-3-mini-128k-Instruct, 
    # Phi-3-small-8k-Instruct, Phi-3-small-128k-Instruct and Phi-3-medium-128k-Instruct 
    # don't support system messages (role="system"). 
    # When you use the Azure AI model inference API, system messages are translated to user messages, 
    # which is the closest capability available. This translation is offered for convenience, 
    # but it's important for you to verify that the model is following the instructions 
    # in the system message with the right level of confidence.
    data = {
        "input_data": 
            [
                {"role": "user", "content": "You are an AI assistant who helps people find information. As the assistant, you answer questions not long, simple, short and in a personable manner using markdown and even add some personal flair with appropriate emojis. Add a witty joke that begins with “By the way,” or “By the way. The joke should be related to the specific question asked. For example, if the question is about tents, the joke should be specifically related to tents. Respond in Korean language. "}, 
                {"role": "user", "content": "Use the following context to provide a more personalized response to the customer:"},
                {"role": "user", "content": context},
                {"role": "user", "content": question}
            ],
        "params": {
                "temperature": 0.7,
                # "max_new_tokens": 4096,     # The maximum value is 4096.
                "max_new_tokens": 256,     
                "do_sample": True,
                "return_full_text": True
        }
    }

    body = str.encode(json.dumps(data))

    url = connection.endpoint
    # Replace this with the primary/secondary key, AMLToken, or Microsoft Entra ID token for the endpoint
    api_key = connection.key
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        response = response.read().decode()
        print(response)
        
        result = json.loads(response)["result"]
        
        return result
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