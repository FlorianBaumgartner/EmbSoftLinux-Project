import threading
from pathlib import Path
import pyaudio
import wave
import os

class Recorder:
    def __init__(self, channels=1, samplerate=44100, chunk=1024):
        self.channels = channels
        self.sample_rate = samplerate
        self.chunk = chunk

        self.isRecording = False
        self.isTerminated = False
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.tempPath = None
        self.outputPath = None

    def __del__(self):
        self.audio.terminate()

    def startRecording(self, path):
        self.outputPath = path
        self.tempPath = path.parent / f"{path.stem}.wav"
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.stream = self.audio.open(format=pyaudio.paInt16, channels=self.channels, rate=self.sample_rate, input=True, frames_per_buffer=self.chunk)
        self.frames = []

        self.isRecording = True
        self.isTerminated = False
        threading.Thread(target=self._record).start()
    
    def stopRecording(self):
        self.isRecording = False
        while not self.isTerminated: pass
        self.stream.stop_stream()
        self.stream.close()
        self._save(self.tempPath)
        self._convert(self.tempPath, self.outputPath)

    def _record(self):
        while self.isRecording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        self.isTerminated = True

    def _save(self, path):
        with wave.open(str(path), 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.audio.get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
    
    def _convert(self, inputPath, outputPath):
        os.system(f"lame {inputPath} {outputPath}")
        os.remove(inputPath)


if __name__ == "__main__":
    file = Path(__file__).parent / "test.mp3"

    recorder = Recorder()
    recorder.startRecording(file)
    input("Press enter to stop recording")
    recorder.stopRecording()
