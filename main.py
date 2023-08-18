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
import time


class Main:
    def __init__(self):
        self.recorder = Recorder()
        self.stt4sg = Stt4Sg()
        self.pseudoGpt = PseudoGpt()
        self.chatGpt = ChatGptX()
        self.youtube = Youtube()
        self.display = Display()
        self.gpio = Gpio()
        self.gpio.start()

        self.state = State.READY
        self.display.setState(State.READY)
        self.filePath = None
        self.playingTitle = ""
        self.transcript = None

        self.demoTransscript = "Ich möchte gerne ein Lied von Meduza hören, und zwar Lose Control"

    def __del__(self):
        self.display.stop()
        self.gpio.stop()

    def run(self):
        self.display.start()
        self.button = False
        self.buttonOld = False
        while True:
            try:
                self.buttonOld = self.button
                self.button = self.gpio.getButtonCenter()
                if self.state == State.READY:
                    self.gpio.setLedGreen(True)
                    if self.button and not self.buttonOld:
                        self.gpio.setLedGreen(False)
                        self.state = State.RECORDING
                        self.display.setState(State.RECORDING)
                        
                        self.filePath = Path(__file__).parent / "recording.mp3"
                        self.recorder.startRecording(self.filePath)
                    if self.gpio.getButtonLeft():
                        self.filePath = None
                        self.transcript = self.demoTransscript
                        self.gpio.setLedGreen(False)
                        self.state = State.RECORDING
                        self.display.setState(State.RECORDING)

                elif self.state == State.RECORDING:
                    self.gpio.setLedRed(time.time() % 1.0 > 0.5)
                    if not self.button and self.buttonOld:
                        self.gpio.setLedRed(False)
                        self.state = State.PROCESSING
                        self.display.setState(State.PROCESSING)

                        self.recorder.stopRecording()
                        print("Done recording")
                        self.filePath = Path(__file__).parent / "recording.mp3"

                elif self.state == State.PROCESSING:
                    self.gpio.setBlinking(True)
                    self.display.setProcessingStatus("Transcribing audio...")
                    if self.filePath:
                        self.transcript = self.stt4sg.getTranscript(self.filePath)
                    print(f"Transcript: {self.transcript}")

                    self.display.setProcessingStatus("Chatting with GPT...")
                    prompt = """Der Benutzer will ein Lied hören. Konvertiere seine Kernaussage als JSON-Ausdruck {"artist": str, "title": str}. Verwende das Wort "NaN" falls etwas nicht genannt wurde. Folgendes ist die Formulierung: """
                    answer = self.getGptAnswer(prompt + self.transcript)
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
                    self.gpio.setBlinking(False)

                elif self.state == State.PLAYING:
                    if(self.button and not self.buttonOld) or self.youtube.getPlayStatus() == False:
                        self.state = State.READY
                        self.display.setState(State.READY)
                        self.youtube.stopMusic()
                        print("Done playing")
                        time.sleep(0.5)
                time.sleep(0.05)
            except KeyboardInterrupt:
                self.display.stop()
                self.gpio.stop()
                break


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
        return result['response']


if __name__ == "__main__":
    main = Main()
    main.run()
