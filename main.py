from pseudoGpt import PseudoGpt
from chatGptX import ChatGptX
from stt4sg import Stt4Sg
from pathlib import Path
from recorder import Recorder
from youtube import Youtube
import threading
import json


class Main:
    def __init__(self):
        self.recorder = Recorder()
        self.stt4sg = Stt4Sg()
        self.pseudoGpt = PseudoGpt()
        self.chatGpt = ChatGptX()
        self.youtube = Youtube()


    def run(self):
        file = Path(__file__).parent / "recording.mp3"
        self.recorder.startRecording(file)
        input("\n\nPress enter to stop recording")
        self.recorder.stopRecording()
        print("Done recording")

        transcript = self.stt4sg.getTranscript(file)
        print(f"Transcript: {transcript}")

        prompt = """Der Benutzer will ein Lied hören. Konvertiere seine Kernaussage als JSON-Ausdruck {"artist": str, "title": str}. Verwende das Wort "NaN" falls etwas nicht genannt wurde. Folgendes ist die Formulierung: """
        
        
        answer = self.getGptAnswer(prompt + transcript)
        print(f"PseudoGpt: {answer}")

        json_str = answer[answer.find('{'):answer.rfind('}') + 1]
        musicInfo = json.loads(json_str)
        print(musicInfo)

        query = ""
        if musicInfo["artist"] != "NaN" and type(musicInfo["artist"]) is not float:
            query += musicInfo["artist"] + " "
        if musicInfo["title"] != "NaN" and type(musicInfo["title"]) is not float:
            query += musicInfo["title"] + " "
        print(f"Play on Youtube: {query}")
        self.youtube.playMusic(query)

        input("\n\nPress enter to stop playing")
        self.youtube.stopMusic()

    def getGptAnswer(self, prompt):
        result = {}
        finished_event = threading.Event()

        def worker(target, name):
            res = target(prompt)
            if not finished_event.is_set():  # Check if no thread has finished yet.
                finished_event.set()
                result['response'] = res
                result['source'] = name

        pseudoGptThread = threading.Thread(target=worker, args=(self.pseudoGpt.generate, "pseudoGpt"))
        chatGptThread = threading.Thread(target=worker, args=(self.chatGpt.generate, "chatGpt"))

        pseudoGptThread.start()
        chatGptThread.start()
        finished_event.wait()       # Wait for one of the threads to finish.
        return result


if __name__ == "__main__":
    main = Main()
    main.run()
