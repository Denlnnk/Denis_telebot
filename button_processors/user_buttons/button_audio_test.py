import subprocess
import speech_recognition as sr
from abstcract_process.abstract_process import AbstractProcess


class AudioTest(AbstractProcess):

    def __init__(self):
        super().__init__()

    def process_message(self, message):
        r = sr.Recognizer()

        file_info = self.bot.get_file(message.voice.file_id)
        downloaded_file = self.bot.download_file(file_info.file_path)
        with open('user_voice.ogg', 'wb') as new_file:
            new_file.write(downloaded_file)

        src_filename = 'user_voice.ogg'
        dest_filename = 'user_voice_output.wav'

        process = subprocess.run(['/home/denis/Downloads/ffmpeg-5.1.2/Makefile', '-i', src_filename, dest_filename])
        if process.returncode != 0:
            raise Exception("Something went wrong")

        user_audio_file = sr.AudioFile("user_voice_output.wav")
        with user_audio_file as source:
            user_audio = r.record(source)
        text = r.recognize_google(user_audio, language='en-US')

        self.bot.send_message(message.chat.id, text)
