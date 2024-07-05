import json, llmtools, functiondef
import llm, actions
import os
"""
all llm flows are here
"""

def simple_chat_flow():
    """
    simple chat with llm
    """
    msgs = []
    while True:
        msgs.append(
            {"role":"user", "content": input("you: ")}
        )
        response = llm.chat(msgs)
        respmsg = json.loads(response)['message']
        msgs.append(respmsg)
        print("bot: " + respmsg['content'])

def simple_prompt_flow(prompt, context):
    """
    simple prompt with system prompt (context) to llm
    """
    response = llm.generate(prompt, context)
    #print(json.loads(response))
    return json.loads(response)['response']

def translation_flow(prompt, source_lang, target_lang):
    """
    simple translation with llm
    """
    response = llm.generate(prompt, f"You translate user's prompt from {source_lang} to {target_lang}.", model = "qwen2")
    #print(json.loads(response))
    return json.loads(response)['response']

def command_flow (prompt):
    context = """
    You are a helpful computer assistant running on Windows 11 OS. 
    You reply executable script.
    Your script should be enclosed by <script> tags.  
    This is an example for shell script: <script>start cmd</script>
    Example for python script: <script>py -c "import os; os.system('start cmd')"</script>
    """
    response = simple_prompt_flow(prompt, context)
    command = actions.extract_command (response)
    actions.execute(command)

def web_search_flow():
    """
    search the web by invoking the web tool
    """

def web_news_flow():
    """
    get news from news websites
    """
    
def rag_flow(prompt):
    """
    search the most revelent content in the vector db and use it as context
    for the prompt
    """
    ids, distances, metadatas, documents = actions.query_rag(prompt)
    response = simple_prompt_flow(prompt, documents[0][0])
    print(ids, distances, metadatas)
    #print(documents[0][0]) #print context (metadata of the document)
    return response

def simple_function_call_flow(prompt):
    """
    invoke the most revelent function for answering 
    the user's question
    """
    prompt = f"[AVAILABLE_TOOLS]{functiondef.functions}[/AVAILABLE_TOOLS][INST]{prompt}[/INST]"
    response = llm.get_function(prompt)
    print(json.loads(response)['response'])
    eval ("llmtools." + actions.transform_string_to_function_call(json.loads(response)['response']))

def whats_on_my_screen (prompt = "describe what you see in this picture; pay attention to the text in the picture"):
    """
    take a screenshot of the screen and ask llm what it sees
    """
    screenshot = actions.take_screenshot_base64()
    response = llm.visual(prompt, [screenshot])
    print(json.loads(response)['response'])

def refine_prompt_flow():
    """
    rephrase user's quesetion by llm instructed to correct grammar and 
    clear confusion then send it to llm 
    """

def oneshot_prompt_flow():
    """
    rephrase user's quesetion by llm instructed to provide an example
     revelent to the question then send it to llm 
    """

def combo_flow():
    """
    regular prompt flow
    ~ simple prompt
    / execute a command
    @ rag query
    @+ add source to rag
    # translate response from one language to another
    ! read the response outloud
    """   
    user_prompt = input("> ")
    #count the occurrence of @#! characters of the first 3 characters of user_prompt
    char_count = sum([user_prompt[:3].count(c) for c in "~@#!"])
    to_translate = "#" in user_prompt[:3] and char_count>1
    to_read_out = "!" in user_prompt[:3] and char_count>1
    response = ""
    response_trans = ""
    if "/" == user_prompt[:1]:
        command_flow(user_prompt[1:])
    elif char_count == 0:
        os.system(user_prompt)
    elif "@+" == user_prompt[:2]:
        actions.add_to_rag(user_prompt[1:])
    elif "@" == user_prompt[:char_count]:
        response = rag_flow(user_prompt[char_count:])
        print(response)
    elif "#" == user_prompt[:1]:
        response = simple_prompt_flow(user_prompt[1:], "You are a helpful assistant.  You reply answers in plan text friendly for displaying on a terminal window.")
        print(response)
    elif "~":
        response = simple_prompt_flow(user_prompt, "You are a helpful assistant.  You reply answers in plan text friendly for displaying on a terminal window.")
        print(response)

    if (to_translate):
        response_trans = translation_flow(response, "English", "Chinese Traditional")
        print(response_trans)
    if (to_read_out):
        actions.read_out(response)
        if(to_translate):
            actions.read_out(response_trans, lang = 'zh-TW')

def main():
    while True:
        combo_flow()    

if __name__=="__main__":
    #simple_chat_flow()
    #simple_function_call_flow(' What is the weather like today in Tokyo ')
    #simple_function_call_flow('open my web browser')
    # whats_on_my_screen()
    while True:
        #simple_function_call_flow(input("> "))
        #command_flow(input("> "))
        combo_flow()