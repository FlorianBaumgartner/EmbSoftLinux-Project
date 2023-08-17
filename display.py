import board            # https://learn.adafruit.com/monochrome-oled-breakouts/python-setup
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import time

from adafruit_display_text.label import Label


# class Display:
#     def __init__(self):
#         i2c = board.I2C()
#         self.oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=digitalio.DigitalInOut(board.D4))
#         self.oled.fill(0)
#         self.oled.show()


oled_reset = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
oled.show()

t = time.time()
while True:
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
    font = ImageFont.load_default()

    text = f"{time.time():.2f}"
    (x, y, font_width, font_height) = font.getbbox(text)
    draw.text(
        (oled.width // 2 - font_width // 2, oled.height // 2 - font_height // 2),
        text,
        font=font,
        fill=255,
    )

    # Display image
    oled.image(image)
    oled.show()
    print(f"FPS: {1 / (time.time() - t):.2f}")
    t = time.time()
