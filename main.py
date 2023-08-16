from pseudoGpt import PseudoGpt
from stt4sg import Stt4Sg
from pathlib import Path
from recorder import Recorder
import json
import sys
import os 

sys.stderr = open(os.devnull, 'w')


class Main:
    def __init__(self):
        self.recorder = Recorder()
        self.stt4sg = Stt4Sg()
        self.gpt = PseudoGpt()


    def test1(self):
        file = Path(__file__).parent / "recording.mp3"
        self.recorder.startRecording(file)
        input("\n\nPress enter to stop recording")
        self.recorder.stopRecording()
        print("Done recording")

        transcript = self.stt4sg.getTranscript(file)
        print(f"Transcript: {transcript}")

        prompt = """Der Benutzer will ein Lied hören. Konvertiere seine Kernaussage als JSON-Ausdruck {"artist": str, "title": str}. Verwende das Wort "NaN" falls etwas nicht genannt wurde. Folgendes ist die Formulierung: """
        answer = self.gpt.generate(prompt + transcript)
        print(f"PseudoGpt: {answer}")

        json_str = answer[answer.find('{'):answer.rfind('}') + 1]
        musicInfo = json.loads(json_str)
        print(musicInfo)


if __name__ == "__main__":
    main = Main()
    main.test1()
