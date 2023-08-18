import board            # https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageSequence
import adafruit_ssd1306
import time
import threading
from enum import Enum
from pathlib import Path


class State(Enum):
    READY = "Ready"
    RECORDING = "Recording"
    PROCESSING = "Processing"
    PLAYING = "PLAYING"


class Display:
    def __init__(self):
        i2c = board.I2C()
        self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=None)#digitalio.DigitalInOut(board.D4))
        self.running = False
        self.terminated = False
        self.thread = None
        self.state = State.READY

        self.defaultFont = ImageFont.load_default()
        self.largeFont = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)

        self.recordStartTime = time.time()
        self.processingStatus = ""
        self.playingTitle = ""
        self.playingTitlePosition = None
        
        self.symbolMic = Image.open(Path(__file__).parent / "GUI" / "mic.png").convert("1")  # Convert to 1-bit image
        self.symbolMic = ImageOps.invert(self.symbolMic)
        desired_size = (self.oled.width // 4, self.oled.width // 4)  # e.g. one-third of the width
        self.symbolMic = self.symbolMic.resize(desired_size, Image.BILINEAR)

        self.gifProcessing = self._convertGif(Path(__file__).parent / "GUI" / "processing.gif", resize=(40, 40), threshold=70, invert=True)
        self.gifProcessingIndex = 0

        self.gifPlaying = self._convertGif(Path(__file__).parent / "GUI" / "speaker.gif", resize=(40, 40), threshold=70, invert=True)
        self.gifPlayingIndex = 0

    def start(self):
        self.oled.fill(0)
        self.oled.show()
        self.running = True
        self.terminated = False
        self.thread = threading.Thread(target=self._run)
        self.thread.start()

    def stop(self):
        self.running = False
        while not self.terminated:
            time.sleep(0.1)
        self.oled.fill(0)
        self.oled.show()

    def setState(self, state):
        self.state = state
        if(self.state == State.RECORDING):
            self.recordStartTime = time.time()
        if(self.state == State.PROCESSING):
            self.gifProcessingIndex = 0
        if(self.state == State.PLAYING):
            self.playingTitlePosition = None
            self.gifPlayingIndex = 0

    def setProcessingStatus(self, status):
        self.processingStatus = status

    def setPlayingTitle(self, title):
        self.playingTitle = title
        self.playingTitlePosition = None

    def _run(self):
        while self.running:
            if self.state == State.READY:
                image = self._displayStateReady()
            elif self.state == State.RECORDING:
                image = self._displayStateRecording()
            elif self.state == State.PROCESSING:
                image = self._displayStateProcessing()
            elif self.state == State.PLAYING:
                image = self._displayStatePlaying()
            
            self.oled.image(image)
            try:
                self.oled.show()
            except OSError:
                print("Could not communicate with display.")

        self.terminated = True


    def _displayStateReady(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        text = "Hold button to Record"
        (x, y, font_width, font_height) = self.defaultFont.getbbox(text)
        draw.text(
            (self.oled.width // 2 - font_width // 2, font_height),
            text,
            font=self.defaultFont,
            fill=255,
        )
        mic_position = ((self.oled.width - self.symbolMic.width) // 2, self.oled.height - self.symbolMic.height - 5)
        image.paste(self.symbolMic, mic_position)
        return image


    def _displayStateRecording(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        recordTime = time.time() - self.recordStartTime
        text = f"Recording: {recordTime:.1f} s"
        (x, y, font_width, font_height) = self.defaultFont.getbbox(text)
        draw.text(
            (self.oled.width // 2 - font_width // 2, font_height),
            text,
            font=self.defaultFont,
            fill=255,
        )
        size = 9
        yOffset = 12
        if time.time() % 1.0 < 0.5:
            draw.ellipse((self.oled.width // 2 - size, self.oled.height // 2 - size + yOffset, self.oled.width // 2 + size, self.oled.height // 2 + size + yOffset), fill=255)
        return image


    def _displayStateProcessing(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        text = self.processingStatus
        (x, y, font_width, font_height) = self.defaultFont.getbbox(text)
        draw.text(
            (self.oled.width // 2 - font_width // 2, font_height),
            text,
            font=self.defaultFont,
            fill=255,
        )

        gif_frame = self.gifProcessing[self.gifProcessingIndex]
        self.gifProcessingIndex += 1
        if self.gifProcessingIndex >= len(self.gifProcessing):
            self.gifProcessingIndex = 0
        if gif_frame.mode != "1":
            gif_frame = gif_frame.convert("1")
        gif_position = ((self.oled.width - gif_frame.width) // 2, font_height * 2)
        image.paste(gif_frame, gif_position)
        return image


    def _displayStatePlaying(self):
        image = Image.new("1", (self.oled.width, self.oled.height))
        draw = ImageDraw.Draw(image)

        yOffset = -34
        text = self.playingTitle
        (x, y, font_width, font_height) = self.largeFont.getbbox(text)
        if self.playingTitlePosition is None:
            self.playingTitlePosition = self.oled.width
        self.playingTitlePosition -= 2
        if self.playingTitlePosition + font_width < 0:
            self.playingTitlePosition = self.oled.width
        draw.text((self.playingTitlePosition, (self.oled.height - font_height - 1 + yOffset)), text, font=self.largeFont, fill=255)

        gif_frame = self.gifPlaying[self.gifPlayingIndex]
        self.gifPlayingIndex += 1
        if self.gifPlayingIndex >= len(self.gifPlaying):
            self.gifPlayingIndex = 0
        if gif_frame.mode != "1":
            gif_frame = gif_frame.convert("1")
        gif_position = ((self.oled.width - gif_frame.width) // 2, 28)
        image.paste(gif_frame, gif_position)
        return image
    
    def _convertGif(self, path, resize=None, threshold=127, invert=False):
        with Image.open(path) as img:
            frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
            frame_durations = [frame.info['duration'] for frame in ImageSequence.Iterator(img)]
        
        if resize:
            scaled_frames = [frame.resize((resize), Image.NEAREST) for frame in frames]
        if invert:
            thresholded_frames = [frame.point(lambda p: 0 if p > threshold else 255) for frame in scaled_frames]
        else:
            thresholded_frames = [frame.point(lambda p: 255 if p > threshold else 0) for frame in scaled_frames]
        return thresholded_frames


if __name__ == "__main__":
    display = Display()
    display.start()
    input("Press enter to change to State Recording")
    display.setState(State.RECORDING)
    input("Press enter to change to State Processing")
    display.setState(State.PROCESSING)
    display.setProcessingStatus("Processing: 1/3")
    time.sleep(0.1)
    display.setProcessingStatus("Processing: 2/3")
    time.sleep(0.1)
    display.setProcessingStatus("Processing: 3/3")
    input("Press enter to change to State Playing")
    display.setState(State.PLAYING)
    display.setPlayingTitle("This is a long title that will scroll")
    input("Press enter to change to State Ready")
    display.setState(State.READY)
    input("Press enter to stop")
    display.stop()
