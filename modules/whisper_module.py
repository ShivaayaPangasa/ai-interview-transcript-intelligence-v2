import os
import queue
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import whisper


# =====================================
# FFMPEG PATH
# =====================================

os.environ["PATH"] += os.pathsep + r"C:\Users\Shivaaya\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-8.1.1-full_build\bin"


# =====================================
# GLOBALS
# =====================================

audio_queue = queue.Queue()

recording_stream = None

audio_chunks = []

sample_rate = 16000


# =====================================
# CALLBACK
# =====================================

def audio_callback(indata, frames, time, status):

    if status:
        print(status)

    audio_queue.put(
        indata.copy()
    )


# =====================================
# START RECORDING
# =====================================

def start_recording():

    global recording_stream
    global audio_chunks

    audio_chunks = []

    recording_stream = sd.InputStream(

        samplerate=sample_rate,

        channels=1,

        callback=audio_callback
    )

    recording_stream.start()

    print("Recording started...")


# =====================================
# STOP RECORDING
# =====================================

def stop_recording(

    output_file="temp_audio/answer.wav"
):

    global recording_stream
    global audio_chunks

    if recording_stream is None:

        return None

    recording_stream.stop()

    recording_stream.close()

    while not audio_queue.empty():

        audio_chunks.append(

            audio_queue.get()

        )

    audio = np.concatenate(
        audio_chunks,
        axis=0
    )

    os.makedirs(
        "temp_audio",
        exist_ok=True
    )

    write(
        output_file,
        sample_rate,
        audio
    )

    print(
        f"Audio saved to {output_file}"
    )

    return output_file


# =====================================
# WHISPER
# =====================================

def transcribe_audio(

    audio_file="temp_audio/answer.wav"
):

    print(
        "Loading Whisper model..."
    )

    model = whisper.load_model(
        "base"
    )

    print(
        "Transcribing audio..."
    )

    result = model.transcribe(
        audio_file
    )

    transcript = result["text"]

    print(
        "\nTranscript:"
    )

    print(transcript)

    return transcript