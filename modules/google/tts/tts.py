from google.cloud import texttospeech
from tone_generator import play_file
import os


class TTS:

    def __init__(self):
        self.fileDir = os.path.dirname(os.path.realpath('__file__'))
        self.client = texttospeech.TextToSpeechClient.from_service_account_json(
            os.path.join(self.fileDir, 'modules/google/google.json'))
        self.voice = texttospeech.VoiceSelectionParams(language_code="en_US", name="en-US-Wavenet-G")
        self.audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    def say(self, tts_string):
        synth_input = texttospeech.SynthesisInput(text=tts_string)
        response = self.client.synthesize_speech(input=synth_input, voice=self.voice, audio_config=self.audio_config)
        with open(os.path.join(self.fileDir, 'modules/google/tts/1.mp3'), "wb") as out:
            out.write(response.audio_content)
        play_file(os.path.join(self.fileDir, 'modules/google/tts/1.mp3'))
