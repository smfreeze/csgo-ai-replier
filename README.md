# csgo-oogabooga-chatbot
A simple CSGO chatbot that automatically replies to messages in chat that uses the self-hosted oogabooga web ui for running LLMs.
<br>
As you are self-hosting the LLMs (that unsuprisingly use your GPU) you may see a performance decrease in CS:GO (although I cannot really notice it).
<br>
You could host the LLMs on another device (w/GPU) and use the public api feature in oogabooga to play without performance changes.
## Setup
### Program setup
cd into where you want to install it and then:
```
git clone https://github.com/smfreeze/csgo-oogabooga-chatbot.git
cd csgo-oogabooga-chatbot
pip3 install -r requirements.txt
```
### Oogabooga setup
