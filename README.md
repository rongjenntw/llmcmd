# Command Line LLM
## This program provide means to interact with llm on terminal.  Start question with one or more of the following characters.
    ~ simple prompt
    @ ask llm question with rag data
    # translate response from English to Chinese
    ! read the response outloud

    @+ add youtube transcript to rag
    / ask llm to execute a command
    
### Installation:  
    pip install -r requirements.txt
    pyinstaller --onefile llmflows.py --name llmcmd

### Usage Single Command:
    llmcmd "~What is Python?"
    llmcmd "@How many programming languages are there?"
    llmcmd "#What is Python used for?"
    llmcmd "@+https://www.youtube.com/watch?v=r5pXu1PAUkI"
### Usage Interactive:
    llmcmd
    combo>~!#What is dark energy?
    Dark energy is a energy fill out the majority of the universe.
    [Translated to Chinese]
    [Readout Chinese]
### Usage Chat:
    llmcmd -c
      chat> what is python
      Python is a scripting language.
      chat>#
      [translated Python is a scripting language.]
      chat>!
      [read out Python is a scripting language.]
### TODO:
- [ ] Add support for other documents.
- [ ] Improve the translation functionality for Mac.
- [ ] Implement voice on MacOS.
