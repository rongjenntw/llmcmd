import re, json, os
import base64
from io import BytesIO
import pyautogui
from youtube_transcript_api import YouTubeTranscriptApi
import llmrag as cdu
import log
with open('config.json', 'r') as file:
    config = json.load(file)
youtube_transcript_dir = config.get('rag_doc_dir')
collection_name = config.get('rag_collection')
# Sample text
"""
[TOOL_CALLS] [{'name': 'get_current_weather', 'arguments': {'location': 'Tokyo', 'format': 'celsius'}}]

To open your web browser, you can call the 'open_browser' function without any parameters:
"""

def extract_function_from_raw_response (text):    # Regular expression pattern to extract the JSON-like substring
    pattern = r'\[TOOL_CALLS\] (\[.*?\])'
    match = re.search(pattern, text)
    if match:
        extracted_substring = match.group(1)
        print(f"Extracted substring: {extracted_substring}")
        return extracted_substring.replace("'",'"')
    else:
        print("No match found.")
        return "ERROR"

def transform_string_to_function_call(tool_calls):
    tool = json.loads(extract_function_from_raw_response(tool_calls))
    function_name = tool[0]['name']
    if('arguments' in tool[0]):
        arguments = tool[0]['arguments']
        args_str = ', '.join([f'{key}="{value}"' for key, value in arguments.items()])
        function_call_str = f'{function_name}({args_str})'
    else:
        function_call_str = f'{function_name}()'
    return function_call_str

def take_screenshot_base64():
    screenshot = pyautogui.screenshot(allScreens=True)
    buffered = BytesIO()
    screenshot.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    print("Screenshot taken and encoded to Base64.")
    return img_str

def extract_command (response_from_llm):
    # Regular expression pattern to extract text within <script> tags
    pattern = r'<script>(.*?)</script>'
    # Using re.search to find the text
    match = re.search(pattern, response_from_llm, re.DOTALL)
    # Extracting the matched text if it exists
    if match:
        extracted_text = match.group(1)
        print(f"Extracted text: {extracted_text}")
        return extracted_text
    else:
        print("No match found.")
        return "ERROR"

def execute(cmd):
    if ("yes" == input("Enter yes to execute: ")):
        os.system(cmd)

def get_youtube_video_id(url):
    # Define the regex pattern for YouTube video URLs
    pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    
    # Search for the pattern in the provided URL
    match = re.search(pattern, url)
    
    # If a match is found, return the video ID
    if match:
        return match.group(1)
    else:
        return None
    
def get_youtube_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['en','zh-Hant','zh-Hans'])
    return " ".join([entry['text'] for entry in transcript])

def save_text_to_file(file_path, content):
    if not os.path.exists(file_path):
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Text saved to {file_path}")
    else:
        print(f"File {file_path} already exists")
    
def add_to_rag(url):
    video_id = get_youtube_video_id(url)
    document = get_youtube_transcript(video_id)
    save_text_to_file(f"{youtube_transcript_dir}\\{video_id}.txt", document)
    cdu.add_youtub_transcript_to_db(video_id, collection_name)

def query_rag(query):
    response = cdu.query(query, collection_name)
    log.stdout(str(response))
    ids = response['ids']
    distances = response['distances']
    metadatas = response['metadatas']
    documents = response['documents']
    return ids, distances, metadatas, documents

"""
read_out is depreciated because gTTS require internat connection and 
the tex it sent to google for voice.  gTTS cannot speed adjustment
gTTS cannot change voice
"""
# def read_out (text, lang = 'en'):
#     tts = gTTS(text = text, lang = lang, slow=False)
#     soundfile = f"readout{lang}.mp3"
#     tts.save(soundfile)
    
#     playsound.playsound(sound=soundfile,  block = True)
#     os.remove(soundfile)

if __name__=='__main__':
    # video_id = input('video id: ')
    # save_text_to_file(f"{youtube_transcript_dir}\\{video_id}.txt", get_youtube_transcript(video_id))
    add_to_rag(input('youtube url: '))
    query = input("query: ")
    ids, distances, metadatas, documents = query_rag(query)
    print(metadatas)
    for document in documents:
        print(document)