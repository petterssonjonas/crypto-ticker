#!/usr/bin/env python
from PIL import Image
from inky import InkyPHAT

inky_display = InkyPHAT("yellow")

inky_display.set_border(inky_display.BLACK)

img = Image.open('/home/pi/code/btc-backdrop.png')

inky_display.set_image(img)
inky_display.show()
