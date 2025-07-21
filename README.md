# Kokoro-ui

This repository contains an extremely simple gradio UI for playing with Kokoro-82M. The currently released Kokoro model is a very small model and can be used on a CPU for text-to-audio (T2A) generation.

It should work without issues on Linux, MacOS and Windows. A working python3 installation is the more important prerequisite. Do *not* use Python 3.13 as some of the dependencies (numpy, etc.) will be built from sources and may fail installation. Python 3.12 is recommended.

### How to run
It is highly recommended to create/activate a conda or virtualenv environment. A venv flow is shown, you can execute the following commands on a shell/terminal:

```
# clone the repository
git clone https://github.com/freakabcd/kokoro-ui.git

# set up a venv
cd kokoro-ui
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

Download the Kokoro model weights and voices. Please do not ignore this step as the languages and voices within the UI are dynamically filled from whatever is available from within the Kokoro release!

```
python3 get_model_and_voices.py
```

Start the server and enjoy generating audio from text inputs. The server should default to this URL http://localhost:7860

```
python3 kokoro-ui.py
```

For Apple Silicon devices (M 1/2/3/4), you should enable MPS_FALLBACK to make use of the GPU and faster generation.

```
PYTORCH_ENABLE_MPS_FALLBACK=1 python3 kokoro-ui.py
```

Alternatively, you can enable this always by adding this to your `~/.zshrc`
```
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

If you want generate Japanese and Mandarin Chinese text to audio, you will need to install a few other dependencies.

```
pip install "misaki[en,ja,zh]"

# dictionary
python3 -m unidic download
```
