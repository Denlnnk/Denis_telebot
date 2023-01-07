import os
import subprocess
import speech_recognition as sr
from telebot import types

from bot.processors.abstcract_process.abstract_process import AbstractProcess


class VoiceProcess(AbstractProcess):

    def __init__(self, first_name: str):
        super().__init__()
        self.first_name = first_name
        self.user_voice_folder = f'static/user_voices/{self.first_name}.ogg'
        self.user_voice_output = f'static/user_voices/{self.first_name}_output.wav'

    def process_message(self, message: types.Message):
        r = sr.Recognizer()

        file_info = self.bot.get_file(message.voice.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)

        with open(self.user_voice_folder, 'wb') as new_file:
            new_file.write(downloaded_file)

        src_filename = self.user_voice_folder
        wav_filename = self.user_voice_output

        process = subprocess.run(['ffmpeg', '-i', src_filename, wav_filename])
        if process.returncode != 0:
            raise Exception("Something went wrong")

        user_audio_file = sr.AudioFile(self.user_voice_output)
        with user_audio_file as source:
            user_audio = r.record(source)
        text = r.recognize_google(user_audio, language='en-US')

        os.remove(self.user_voice_folder)
        os.remove(self.user_voice_output)

        self.bot.send_message(message.chat.id, text)
