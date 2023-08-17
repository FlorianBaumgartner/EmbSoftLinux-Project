import board
import digitalio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306


oled_reset = digitalio.DigitalInOut(board.D4)
i2c = board.I2C()
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c, addr=0x3C, reset=oled_reset)
oled.fill(0)
oled.show()


image = Image.new("1", (oled.width, oled.height))

draw = ImageDraw.Draw(image)
draw.rectangle((0, 0, oled.width, oled.height), outline=0, fill=0)
font = ImageFont.load_default()

# Draw Some Text
text = "Hello World!"
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
