import board
import digitalio
from PIL import Image, ImageDraw, ImageSequence, ImageFont
import adafruit_ssd1306
import time
from pathlib import Path

oled_reset = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
oled.show()

def play_gif(gif_path, loop_count=0):
    with Image.open(gif_path) as img:
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        frame_durations = [frame.info['duration'] for frame in ImageSequence.Iterator(img)]
    
    scaled_frames = [frame.resize((128, 64), Image.BICUBIC) for frame in frames]
    thresholded_frames = [frame.point(lambda p: 255 if p > 70 else 0) for frame in scaled_frames]
    
    oled_frames = [frame.convert("1") for frame in thresholded_frames]
    oled_frames = oled_frames[1:]

    loop = 0
    while True:
        for idx, frame in enumerate(oled_frames):
            oled.image(frame)
            oled.show()
            # time.sleep(frame_durations[idx] / 1000.0)  # Convert duration to seconds
        
        # loop += 1
        # if loop_count and loop >= loop_count:
        #     break


# Play GIF indefinitely
file = Path(__file__).parent / "hole.gif"
play_gif(file)