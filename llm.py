import requests, json, os
#print("LLMCMD_CONFIG_FILE_PATH: " + str(os.environ.get('LLMCMD_CONFIG_FILE_PATH')))
with open(os.getenv('LLMCMD_CONFIG_FILE_PATH') or 'config.json', 'r') as file:
    config = json.load(file)
#generate a response from llm
def generate(prompt, context, model=config.get('llm_prompt')):
    url = config.get('llm_prompt_url')
    data = {"model": model, "prompt": prompt, "stream": False, "system": context}
    response = requests.post(url, json=data)
    return response.text

#get_function a response from llm
def get_function(prompt, model=config.get('llm_function')):
    url = config.get('llm_prompt_url')
    data = {"model": model, "prompt": prompt, "stream": False, "raw": True}
    response = requests.post(url, json=data)
    return response.text

def chat(msg, model=config.get('llm_chat')):
    url = config.get('llm_chat_url')
    data = {"model": model, "messages": msg, "stream": False}
    response = requests.post(url, json=data)
    return response.text

def visual(prompt, imgs, model=config.get('llm_vision')):
    url = config.get('llm_prompt_url')
    data = {"model": model, "prompt": prompt, "images": imgs, "stream": False}
    response = requests.post(url, json=data)
    return response.text

def embeddings(prompt, model=config.get('llm_embeddings')):
    url = config.get('llm_embeddings_url')
    data = {"model": model, "prompt": prompt}
    response = requests.post(url, json=data)
    return response.json()['embedding']

if __name__=='__main__':
    print(generate('what is blackhole', 'you are talking to a 5 year old boy'))
    print(chat([{"role": "user", "content": "hi"}]))