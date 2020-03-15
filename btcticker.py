#! /usr/bin/python3


"""
TODO:
Add simple logging using loguru? http://github.com/Delgan/loguru
Place text statically, not by division as below.
Price history in smaller text under main price.
Price time.
Use TinyDB?
Big price move in White, small Yellow.
Change font. Put it in script dir.
Make "package" for ppl to download and run on their phat.
Maybe make one for both phat and what. Args for type and colors.
"""

## Dependencies:
## Install python modules
# sudo pip3 search/install pillow, inky, fredokaone, bitcoin-price-api, loguru
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from font_fredoka_one import FredokaOne
from exchanges.bitfinex import Bitfinex

# Im using a yellow inky pHAT.
# If you use a wHAT change "InkyPHAT" to "InkyWHAT"
# And if you have another color, change "yellow" to "red" or "black".
inky_display = InkyPHAT("yellow")


# Set border color.
inky_display.set_border(inky_display.YELLOW)


# Set the image. Has to be a specific color palette and size.
# I used GIMP to edit one of the example images from the inky git.
# You need the inky-palete.gpl imported and active in GIMP. 
img = Image.open("/home/pi/code/btc-backdrop.png")
text = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)


# Get price. Yes, one line of code, thanks to bitcoin-price-api.
# And also format it to remove decimals.
btc = Bitfinex().get_current_price()
message = format(btc, ".0f")




# Set parameterss of text, placement, color, font.
font = ImageFont.truetype(FredokaOne, 42)
w, h = font.getsize(message)
x = (inky_display.WIDTH / 1.3) - (w / 1.3)
y = (inky_display.HEIGHT / 2.25) - (h / 2.25)
# My image has black background so im printing text in white.
# Swap WHITE here for RED, YELLOW or BLACK.
draw.text((x, y), message, inky_display.WHITE, font)


# Logging. Timestamped and success or error.
#


# Finally print it all
inky_display.set_image(img)
inky_display.show()

