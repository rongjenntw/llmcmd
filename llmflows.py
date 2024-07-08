import json, voiceutils, functiondef
import sys
import llm, actions, log
import os
"""
all llm flows are here
"""
with open('config.json', 'r') as file:
    config = json.load(file)
def simple_chat_flow(system_prompt = "You are a helpful assistant."):
    """
    simple chat with llm
    enter '!' to read out the previous response from the chat bot
    enter '#' to translate the previous response from the chat bot to Chinese
    enter '#!' to read out the previous response from the chat bot in Chinese
    """
    msgs = [{"role": "system", "content": system_prompt}]
    prevresp = "Beginning of conversation"
    actor = voiceutils.BOB
    while True:
        user_prompt = input("chat> ")
        char_count, prevresp, actor = prompt_actions(user_prompt, prevresp, actor)
        if(char_count == 0):
            msgs.append(
                {"role":"user", "content": user_prompt}
            )
            response = llm.chat(msgs)
            respmsg = json.loads(response)['message']
            msgs.append(respmsg)
            prevresp = respmsg['content']
            print(prevresp)
            actor = voiceutils.BOB

def simple_prompt_flow(prompt, context):
    """
    simple prompt with system prompt (context) to llm
    """
    response = llm.generate(prompt, context)
    #print(json.loads(response))
    return json.loads(response)['response']

def revelent_questions_flow(prompt):
    """
    Convert the user's request to revelent questions.
    This is useful for understanding the user's intent and 
    generating relevant questions to ask about their request.
    For example:
    user: I want a pizza
    bot: What kind of pizza do you prefer? (Italian, Vegetarian, etc.)
    user: Italian
    bot: What type of crust would you like? (Deep Dish, Stuffed, etc.)
    user: Deep Dish
    bot: What size do you prefer? (Small, Medium, Large)
    user: Small
    bot: What toppings would you like? (Cheese, Olives, Pepperoni)
    """

def translation_flow(prompt, source_lang, target_lang):
    """
    simple translation with llm
    """
    response = llm.generate(prompt, f"You translate user's prompt from {source_lang} to {target_lang}.", model = "qwen2")
    #print(json.loads(response))
    return json.loads(response)['response']

def command_flow (prompt):
    context = f"""
    You are a helpful computer assistant running on {config.get('command_flow_os')}. 
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
    if (documents[0]):
        context = documents[0][0]
    else:
        context = "no records found"
    print("rag reference", ids, distances, metadatas)
    response = simple_prompt_flow(prompt, context)
    #print(documents[0][0]) #print context (metadata of the document)
    return response

def function_call_flow(prompt):
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

def combo_flow(user_promot=None):
    """
    regular prompt flow
    ~ simple prompt
    / execute a command
    @ rag query
    @+ add source to rag
    # translate response from one language to another
    ! read the response outloud
    """   
    user_prompt = user_promot or input("combo> ")
    #prevresp = "Beginning of conversation"
    actor = voiceutils.BOB
    #char_count, prevresp, actor = prompt_actions(user_prompt, prevresp, actor)
    char_count = sum([user_prompt[:3].count(c) for c in "~@#!"])
    response = ""
    #response_trans = ""
    if "/" == user_prompt[:1]:
        command_flow(user_prompt[1:])
    elif char_count == 0:
        if user_prompt[:3] == 'cd ':
            os.chdir(user_prompt[3:])
        else:
            os.system(user_prompt)
    elif "~" == user_prompt[:1]:
        response = simple_prompt_flow(user_prompt, "You are a helpful assistant.  You reply answers in plan text friendly for displaying on a terminal window.")
        log.stdout(response, log.DEBUG)
    elif "@+" in user_prompt[:2]:
        actions.add_to_rag(user_prompt[1:])
    elif "@" in user_prompt[:char_count]:
        response = rag_flow(user_prompt[char_count:])
        log.stdout(response, log.DEBUG)

    char_count, prevresp, actor = prompt_actions(user_prompt, response, actor)

    print(prevresp)
    return prevresp

"""
! = read out action
# = translation action
"""
def prompt_actions(user_prompt, prevresp, actor):
    char_count = sum([user_prompt[:3].count(c) for c in "~@#!"])
    to_translate = "#" in user_prompt[:3] and char_count>0
    to_read_out = "!" in user_prompt[:3] and char_count>0
    if (to_translate):
        prevresp = translation_flow(prevresp, "English", "Chinese Traditional")
        log.stdout(prevresp, log.DEBUG)
        actor = voiceutils.JENNY
    #print(prevresp)
    if (to_read_out):
        voiceutils.read_out(prevresp, actor)
    return char_count, prevresp, actor

def main():
    while True:
        combo_flow()

def chat():
    simple_chat_flow()

if __name__=="__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "-c":
            chat()
        else:
            combo_flow(sys.argv[1])
    else:
        main()