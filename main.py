from pseudoGpt import PseudoGpt
from chatGptX import ChatGptX
from stt4sg import Stt4Sg
from pathlib import Path
from recorder import Recorder
from youtube import Youtube
from display import Display, State
from gpio import Gpio
import threading
import json


class Main:
    def __init__(self):
        self.recorder = Recorder()
        self.stt4sg = Stt4Sg()
        self.pseudoGpt = PseudoGpt()
        self.chatGpt = ChatGptX()
        self.youtube = Youtube()
        self.display = Display()
        self.gpio = Gpio()

        self.state = State.READY
        self.display.setState(State.READY)
        self.filePath = None
        self.playingTitle = ""

    def __del__(self):
        self.display.stop()

    def run(self):
        self.display.start()
        while True:
            if self.state == State.READY:
                if self.gpio.getButtonCenter():
                    self.state = State.RECORDING
                    self.display.setState(State.RECORDING)
                    
                    self.filePath = Path(__file__).parent / "recording.mp3"

                    self.recorder.startRecording(self.filePath)
            elif self.state == State.RECORDING:
                if not self.gpio.getButtonCenter():
                    self.state = State.PROCESSING
                    self.display.setState(State.PROCESSING)

                    self.recorder.stopRecording()
                    print("Done recording")
                    self.filePath = Path(__file__).parent / "recording.mp3"

            elif self.state == State.PROCESSING:
                self.display.setProcessingStatus("Transcribing audio...")
                transcript = self.stt4sg.getTranscript(self.filePath)
                print(f"Transcript: {transcript}")

                self.display.setProcessingStatus("Chatting with GPT...")
                prompt = """Der Benutzer will ein Lied hören. Konvertiere seine Kernaussage als JSON-Ausdruck {"artist": str, "title": str}. Verwende das Wort "NaN" falls etwas nicht genannt wurde. Folgendes ist die Formulierung: """
                answer = self.getGptAnswer(prompt + transcript)
                print(f"PseudoGpt: {answer}")

                self.display.setProcessingStatus("Searching on YouTube...")
                json_str = answer[answer.find('{'):answer.rfind('}') + 1]
                musicInfo = json.loads(json_str)
                print(musicInfo)

                query = ""
                if musicInfo["artist"] != "NaN" and type(musicInfo["artist"]) is not float:
                    query += musicInfo["artist"] + " "
                if musicInfo["title"] != "NaN" and type(musicInfo["title"]) is not float:
                    query += musicInfo["title"] + " "
                print(f"Play on Youtube: {query}")
                self.playingTitle = self.youtube.playMusic(query, True)
                if self.playingTitle == "":
                    self.playingTitle = self.youtube.playMusic(query, False)
                print(f"Playing: {self.playingTitle}")
                self.state = State.PLAYING
                self.display.setPlayingTitle(self.playingTitle)
                self.display.setState(State.PLAYING)

            elif self.state == State.PLAYING:
                if self.gpio.getButtonCenter():
                    self.state = State.READY
                    self.display.setState(State.READY)

                    self.youtube.stopMusic()
                    print("Done playing")


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
