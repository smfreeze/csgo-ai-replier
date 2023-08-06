# csgo-oogabooga-chatbot
A simple free locally-run CSGO chatbot that replies to messages in chat for you.
<br>
Uses the (locally-run) oogabooga web ui for running LLMs and NOT ChatGPT.
<br>
As you are self-hosting the LLMs (that unsuprisingly use your GPU) you may see a performance decrease in CS:GO (although, for me at least, this is minor).
<br>
You COULD host the LLMs on another device (w/GPU) and use the oogabooga public api feature to play without performance changes.
# Setup
## Program setup
cd into where you want to install it and then:
```
git clone https://github.com/smfreeze/csgo-oogabooga-chatbot.git
cd csgo-oogabooga-chatbot
pip3 install -r requirements.txt
```
Make appropriate changes to Program.py in the config section

## Oogabooga setup
(Thanks [DeSinc](https://github.com/DeSinc/SallyBot) for writing this setup guide)
<br><br>
Warning: For the average 7B model, it requires a card with at least 6GB of VRAM. If you're running on CPU you need at least 6-8GB of ram.

If you're willing to run on the inferior smaller parameter count models like Pythia-2.8B-deduped or something then it'll work on less RAM/VRAM, but the output is untested and frankly likely to be bad.

Download and install [Oobabooga from their repo here](https://github.com/oobabooga/text-generation-webui). Their README has information on how to install it, with two methods: 1-click installer and manual. I heavily recommend the 1-click installer.

After downloading and unzipping the 1-click installer, run `start_windows.bat`. The installer is interactive and you will need to enter your GPU device when prompted, or select CPU mode. I do not recommend CPU mode.

The install script will also ask you if you want to install a model, it offers some suggested models however I recommend you search for a language model yourself on HuggingFace. Copy the model name to clipboard and paste it into the script.

Here's an example of what a username/modelname looks like on HuggingFace:

![Example of a model on HuggingFace](https://github.com/DeSinc/SallyBot/assets/36467674/becc58e0-8e96-42f2-bfca-79c1bcc86fae)

You can download a model afterwards with the downloader script, open the console in the text-generation-webui folder and run `python download-model.py <name of model>`.

After the installing has finished you need to set up the arguements in the `webui.py` file to allow SallyBot to communicate with Oobabooga. It can be found near the top of the file.

![Showing where to input args](https://github.com/DeSinc/SallyBot/assets/36467674/a7c6e8b0-6644-4c73-878b-9b2cb44c1d3a)

Arguments to be added here include:

`--chat` sets the web interface to chat mode which is better. This arg isn't necessary it just makes the web interface look nicer if you choose to browse to it on localhost:7862 in your web browser.

`--model <folder_name_of_model>` specifies which model Oobabooga should use, replace `<folder_name_of_model>` it is the name of the folder in text-generation-webui/models.

`--api` tells Oobabooga to allow SallyBot to integrate together.

`--loader exllama_hf` uses the much updated ExLLAMA model loader which is literally nearly 2x faster than the previously used loader. Might already be default by the time you see and run this.

`--listen-port 7862` is set to 7862 to not overlap with stable diffusion. `--api` opens a separate port for sallybot to interface with which runs on port 5000. Port 7862 can still be used to view the web interface if you like.

`--xformers` is a very good optimiser that reduces your vram usage for free. This argument is not required but very encouraged. It needs to be installed into Oobabooga to use. Run `cmd_windows.bat` and type `pip install xformers`, when it is done you can type exit.

`--wbits 4` and `--groupsize 128` specify details about the model. If you know what you're doing you can remove whichever ones you don't need. `--groupsize 128` if you are using a non 128 groupsize model, or `--wbits 4` if you are not running a 4-bit quantized model, for instance. Most of the consumer running ones are 4bit quantized to run on normal amounts of vram, so you'll need this arg to run those models.

Example of args:
`--model TheBloke/WizardLM-7B-uncensored-GPTQ --loader exllama_hf --api --listen-port 7862 --wbits 4 --groupsize 128`

![Image showing example of args](https://github.com/DeSinc/SallyBot/assets/36467674/eaa1caf1-0285-4c87-98f9-b45ba65d6df6)
<br>
`(SMFreeze here: I do not understand the difference between --api and --extension api, but I haven't really tested it because mine works fine with --api)`
<br>

If you'd like to modify the parameters for Oobabooga, it's this section here:
```python
request = {
        'user_input': user_input,
        'max_new_tokens': 750,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'chat',
        'character': character, # Change/add this in the oogabooga api (chat settings -> character)
        'instruction_template': 'Vicuna-v1.1', 
        'your_name': 'You',
        'regenerate': False,
        '_continue': False,
        'stop_at_newline': False,
        'chat_generation_attempts': 1,
        'chat-instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|You are a gamer|>".\n\n<|You hate the people speaking to you|>',
    }
```
(From OogaAPI.py in the getResponse() function)
