import logging
import os
import tempfile
from glob import glob

import gradio as gr
import numpy as np
import soundfile as sf
from kokoro import KModel, KPipeline

logger = logging.getLogger(__name__)
logging.basicConfig(filename="kokoro-ui.log", level=logging.INFO)

KOKORO_PATH = "Kokoro-82M"
MODEL = KModel(
    config=f"{KOKORO_PATH}/config.json", model=f"{KOKORO_PATH}/kokoro-v1_0.pth"
)


# Generate audio from user probvided inputs
def generate_audio(text, voice, speed):
    logger.info(
        f"generate_audio called with text: {text}\nvoice: {voice}\nspeed: {speed}"
    )

    pipeline = KPipeline(lang_code=voice[0], model=MODEL)
    filename = tempfile.mkstemp(suffix=".wav")[1]
    with sf.SoundFile(filename, "w", 24000, 1) as f:
        for _, _, audio in pipeline(
            text=text, voice=f"{KOKORO_PATH}/voices/{voice}.pt", speed=speed
        ):
            f.write(np.asarray(audio))
        logger.info(f"{f.frames} frames written to {filename}")
    return filename


# Organise languages and voices
DEFAULT_LANG = "a"
DEFAULT_VOICE = "af_bella"
LANG_MAP = {
    "a": ("English (US)", "a"),
    "b": ("English (UK)", "b"),
    "c": ("German", "c"),
    "e": ("Spanish", "e"),
    "f": ("French", "f"),
    "h": ("Hindi", "h"),
    "i": ("Italian", "i"),
    "j": ("Japanese", "j"),
    "p": ("Brazilian Portuguese", "p"),
    "z": ("Mandarin Chinese", "z"),
}

voices_dir = os.path.join(KOKORO_PATH, "voices")
voice_files = glob(os.path.join(voices_dir, "*.pt"))
voices = sorted([os.path.splitext(os.path.basename(f))[0] for f in voice_files])

voice_langs = dict.fromkeys([v[0] for v in voices]).keys()
languages = [
    (LANG_MAP.get(lang_prefix) or (lang_prefix, lang_prefix))
    for lang_prefix in voice_langs
]


# Repopulate voice options when language changes
def lang_changed(lang):
    newvoices = [vc for vc in voices if vc.startswith(lang)]
    logger.info(f"Language changed to {lang}")
    logger.info(f"New voices: {newvoices}")

    return gr.Dropdown(choices=newvoices, value=newvoices[0])


# Main interface
# with gr.Blocks(title="Kokoro TTS", css="footer{display:none !important}") as app:
with gr.Blocks(title="Kokoro TTS") as app:
    gr.Markdown("### 🎙️ Kokoro 82-M TTS (local)")
    with gr.Row():
        text = gr.Textbox(label="Text", lines=4, placeholder="Type here…")
    with gr.Row():
        lang = gr.Dropdown(choices=languages, value=DEFAULT_LANG, label="Language")
        voice = gr.Dropdown(
            choices=[vc for vc in voices if vc.startswith(DEFAULT_LANG)],
            value=DEFAULT_VOICE,
            label="Voice",
        )
        speed = gr.Slider(0.5, 2.0, value=1.0, label="Speed")

        lang.change(lang_changed, inputs=lang, outputs=voice)

    btn = gr.Button("Generate", variant="primary")
    audio = gr.Audio(label="Synthesized speech", autoplay=True)

    btn.click(generate_audio, [text, voice, speed], audio)

    # Custom footer HTML
    gr.HTML("""
    <style>
        footer[class*='svelte'] {
            display: none !important;
        }

        .my-footer {
            display: flex;
            flex-flow: row wrap;
            justify-content: center;
            align-items: center;
            gap: 16px;
        }

        .footer-sep {
            border: 1px solid #d3d3d3;
            align-self: stretch;
        }
            
        .footer-img {
            max-height: 32px;
            filter: invert(0.8);
        }
        @media (prefers-color-scheme: light) {
            .footer-img {
                filter: invert(0);
            }
        }
    </style>
    """)
    gr.HTML("""
    <div class="my-footer">
        <a href='https://ko-fi.com/freakabcd' target='_blank'>
            <img class="footer-img" src="/gradio_api/file=kofi_logo.png" alt="☕️ Support me if you can">
        </a>
        <div class="footer-sep"></div>
        <a href='https://github.com/freakabcd/kokoro-ui' target='_blank'>
            <img class="footer-img" src="/gradio_api/file=github_logo.png" alt="GitHub repository">
        </a>
    </div>
    """)

# Launch interface when file is run directly
if __name__ == "__main__":
    from datetime import datetime

    logger.info("\n\n=========================================")
    logger.info("Launching Kokoro UI…")
    logger.info(f"Current date and time is {datetime.now()}")
    app.launch(allowed_paths=[os.path.dirname(os.path.realpath(__file__))])
