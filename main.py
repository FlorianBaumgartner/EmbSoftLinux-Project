from pseudoGpt import PseudoGpt
from stt4sg import Stt4Sg
from pathlib import Path


class Main:
    def __init__(self):
        self.stt4sg = Stt4Sg()
        self.gpt = PseudoGpt()


    def test1(self):
        file = Path(__file__).parent / "test.mp3"
        transcript = self.stt4sg.getTranscript(file)
        prompt = f"Fasse mir den folgenden Text zusammen (auf Deutsch): {transcript}"
        answer = self.gpt.generate(prompt)
        print(answer)


if __name__ == "__main__":
    main = Main()
    main.test1()
