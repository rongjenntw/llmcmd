# Command Line LLM
## This program provide means to interact with llm on terminal.  Start your prompt with one or more of the following characters.
    no prefix: run command on terminal
    / prefix to your prompt: ask llm to suggest an executable a command
    ~ prefix to your prompt: simple prompt
    @ prefix to your prompt: ask llm question referencing rag data
    @+ add youtube transcript to rag

    # translate response from English to Chinese or language defined in config.json prompt
    ! read the response outloud
    
### Installation:  
    pip install -r requirements.txt
    pyinstaller --onefile llmcmd.py --name llmcmd
    copy llmcmd and config.json to your desired execution directory
     or set environment variable LLMCMD_CONFIG_FILE_PATH to config.json path
    make optional changes to config.json
    you will need Ollama and Chroma DB installed and running 

### Usage Single Command:
    - ask a question
    llmcmd "~What is Python?"
    - ask a question with referencing RAG DB
    llmcmd "@How many programming languages are there?"    
    - add a youtube transcript to RAG DB
    llmcmd "@+https://www.youtube.com/watch?v=r5pXu1PAUkI"
    - add a text based webpage to RAG DB
    llmcmd "@+https://text.npr.org/g-s1-8534"
    - take a screenshot and ask LLM what it sees using the default prompt defined in config.json
    llmcmd "$"
    llmcmd "$your own prompt"
    - take a screenshots every 60 seconds for a duration and ask LLM to compare screenshot over time
      frame delay and duration can be changed in config.json 
    llmcmd "$+"
    llmcmd "$+your own prompt"
    - you can append ! to your action to readout and/or append # to do translation
      the language for translation can be changed in config.json
    llmcmd "~!#What is Python used for?"
    llmcmd "@!#What is Python used for?"
    llmcmd "$!#What is Python used for?"

### Usage Interactive:
    >llmcmd
    llmcmd>~!#What is dark energy?
    Dark energy is an energy fill out the majority of the universe.
    [Translated to Chinese or language defined in config.json]
    [Readout Chinese or language defined in config.json]
    llmcmd>@what is my first job in my resume
    Software engineer at UC
### Usage Chat:
    llmcmd -c
      chat> what is python
      Python is a scripting language.
      chat>#
      [translated Python is a scripting language.]
      chat>!
      [read out Python is a scripting language.]
### TODO:
- [ ] Add support for other document types.
- [ ] Improve the translation functionality for other languages.
- [ ] Implement voice on MacOS.
