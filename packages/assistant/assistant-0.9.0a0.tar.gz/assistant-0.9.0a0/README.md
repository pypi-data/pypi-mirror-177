<p align="center">
Your very own Assistant. Because you deserve it.
</p>

<p align="center">  
Click the ⭐ if you like Assistant and <a href="https://twitter.com/intent/tweet?text=Assistant%20is%20my%20new%20favorite%20shell!&url=https://github.com/wasertech/assistant" target="_blank">tweet</a>.
</p>

## Requirements

You need `python 3.10.8` with the following requirements:

   - `Python 3.10.8`
      - [`Domain Management Tool`](https://gitlab.com/waser-technologies/technologies/dmt)

## Installation

To install `Assistant` use `pip`:

```bash
pip install assistant
# Or from source:
pip install -U git+https://gitlab.com/waser-technologies/technologies/assistant.git
```

## Start the service

```zsh
cp ./assistant.service.example /usr/usr/lib/systemd/user/assistant.service
cp ./assistant.listen.service.example /usr/usr/lib/systemd/user/assistant.listen.service
systemctl --user enable --now assistant.service
```

## Usage

Just call `Assistant` like any other shell.

```bash
❯ assistant --help
usage: assistant [-h] [-V] [-c COMMAND] [-i] [-l] [--rc RC [RC ...]] [--no-rc]
                 [--no-script-cache] [--cache-everything] [-D ITEM]
                 [--shell-type {b,best,d,dumb,ptk,ptk1,ptk2,prompt-toolkit,prompt_toolkit,prompt-toolkit1,prompt-toolkit2,prompt-toolkit3,prompt_toolkit3,ptk3,rand,random,rl,readline}]
                 [--timings]
                 [script-file] ...

Assistant: a clever shell implementation

positional arguments:
  script-file           If present, execute the script in script-file or (if
                        not present) execute as a command and exit.
  args                  Additional arguments to the script (or command)
                        specified by script-file.

optional arguments:
  -h, --help            Show help and exit.
  -V, --version         Show version information and exit.
  -c COMMAND            Run a single command and exit.
  -i, --interactive     Force running in interactive mode.
  -l, --login           Run as a login shell.
  --rc RC [RC ...]      RC files to load.
  --no-rc               Do not load any rc files.
  --no-script-cache     Do not cache scripts as they are run.
  --cache-everything    Use a cache, even for interactive commands.
  -D ITEM               Define an environment variable, in the form of
                        -DNAME=VAL. May be used many times.
  --shell-type {b,best,d,dumb,ptk,ptk1,ptk2,prompt-toolkit,prompt_toolkit,prompt-toolkit1,prompt-toolkit2,prompt-toolkit3,prompt_toolkit3,ptk3,rand,random,rl,readline}
                        What kind of shell should be used. Possible options:
                        readline, prompt_toolkit, random. Warning! If set this
                        overrides $SHELL_TYPE variable.
  --timings             Prints timing information before the prompt is shown.
                        This is useful while tracking down performance issues
                        and investigating startup times.


❯ assistant Hi
Hey, how are you today?

❯ assistant -c "what time is it"
The current time is 1:35 p.m.

❯ assistant -i -l --no-rc --no-script-cache -DPATH="PATH:/share/assistant/"

❯ assistant script.nlp
```

## Examples

The examples below are produced in interactive mode.

### Jaques à dit: répond

```assistant
❯ echo Hello
Hello
❯ say Hello World # This requires say to be installed
Hello World
❯ Hi Assistant.
Hello $USERNAME.
```

### List files

```assistant
❯ What do we have here?
I found a couple dozen files and directories.
Shall I care to print them all?
❯ Please. You can omit the hidden ones though.
Sure, there you go.
[FILES]
```

### Change directory

```assistant
❯ Projects
So rude.
Warpping to your Projects/ now.
❯ Thanks but I really wanted to open project Assistant to change that rude behavior.
Whatever you say.
Shall I use your editor to open this project?
❯ You know me so well.
I'll take that as a yes.
Using neovim to open your project Assistant.
```

### Exit the session

To exit the current session, you can type pretty much anything. As long as `Assistant` can reasonnably understand your intent.

*i.e.* :
```assistant
❯ exit
❯ Q
❯ :q
❯ quit
❯ stop()
❯ terminate
❯ This conversation is over.
❯ Stop this session.
```

## Using voice

### Text-To-Speech

Assistant can talk. Just install [`say`](https://gitlab.com/waser-technologies/technologies/say), authorize the system to speak. Make sure the service is running and Assistant should be able to connect to it.

### Speech-To-Text

Assistant can also understand when you talk. Just install [`listen`](https://gitlab.com/waser-technologies/technologies/listen), authorize the system to listen. Make sure `listen.service`, `assistant.service` and `assistant.listen.service` are enabled for Assistant to be able to pick up what you say.

By default, neither the accoustic model not the language model are ajusted for assistant, so it's a good idea to create a custom scorer using the STT Training Wizard.

```zsh
~/.assistant/trainers/stt.train
```

## Use Assistant as your default shell

> **This is not recommended in alpha!**

You sould be able to add the location of `assistant` at the end of `/etc/shells`. You'll then be able to set `Assistant` as your default shell using `chsh`.

```bash
sudo sh -c 'w=$(which assistant); echo $w >> /etc/shells'
chsh -s $(which assistant)
```
Log out and when you come back, `Assistant` will be your default shell.

## Contributions

You like the projet and want to improve upon it?

Checkout [`CONTRIBUTING.md`](CONTRIBUTING.md) to see how you might be able to help.

## Credits

Thanks to all the projects that make this possible:
- [Xonsh](https://github.com/xonsh/xonsh): the best snail in the jungle
- [RASA](https://github.com/RasaHQ/rasa): so Assistant can answer at all
- [coqui-STT](https://github.com/coqui-ai/STT): so you can speak too
- [coqui-TTS](https://github.com/coqui-ai/TTS): so Assistant can reply out-loud
- And many many many more.
