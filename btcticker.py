#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import argparse
from datetime import datetime
from pytz import timezone
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGroteskMedium
from exchanges.bitfinex import Bitfinex
"""
TODO:
Add simple logging using loguru? http://github.com/Delgan/loguru
Price history in smaller text under main price.
If btc-api dont support lastprice build a tinydb? also good to have
a price history locally anyways. Maybe use to chart a graph or smt.
Big price move in Yellow, small in White. Or use arrow icons.
- Add args for display type and color. Also currencypair. fallback defaults.
"""
"""
This program is made to run on the Raspberry Pi (Zero W) with the Pimoroni
e-ink display InkyPHAT.
Dependencies:
Install python modules
pip search/install inky, pillow, bitcoin-price-api, loguru, pytz
And a font package, either of the following for example:
font-hanken-grotesk, font-fredoka-one, font-font-awesome, nerdfonts
"""
# https://docs.python.org/2/howto/argparse.html
parser = argparse.ArgumentParser()
parser.add_argument("--color", "-c", type=str, required=True, choices=["red", "black", "yellow"], help="InkyPHAT Display Color")
parser.add_argument("--bordercolor", "-bc", type=str, required=False, choices=["black", "white", "red", "yellow"], help="Set border color.")
parser.add_argument("--pricecolor", "-pc", type=str, required=False, choices=["black", "white", "red", "yellow"], help="Set color of price.")
#parser.add_argument("--exchange", "-e")
#parser.add_argument("--currencypair", "-cp", type=str, required=False, choices=["btcusd", "btceur", "ethusd", "etheur"], help="Currency pair to print. ex. 'btcusd' or 'etheur'.")
#parser.add_argument("--daemon", "-d", type=str, required=False, help="Run in the background.")
#parser.add_argument("--updatetimer", "-t", type=int, required=False, choices=["5", "15", "30", "60"], help="How often to update in minutes. 5, 15, 30, 60".)
#--verbose
args = parser.parse_args()
color = args.color
bordercolor = args.bordercolor
pricecolor = args.pricecolor
#updatetimer = args.updatetimer
# What PHAT color u has?
inky_display = InkyPHAT(color)
# Set border color.
inky_display.set_border(inky_display.YELLOW)
# Set path to where this file is at.
PATH = os.path.dirname(__file__)
# Set time and format (google python datetime module for formatting info)
# Get time in UTC, and convert it to your timezone, then set localtime.
# This pretty much prints time over the full screen width
timeformat = "%H:%M:%S, %a, %b %d, %Y"
utctime = datetime.now(timezone("UTC"))
timezone = utctime.astimezone(timezone("Europe/Stockholm"))
localtime = timezone.strftime(timeformat)
# Get price. Yes, one line of code, thanks to bitcoin-price-api.
# Plan to use crypto-price-api (fork) and add more coins later.
# And also format it to remove decimals.
btc = Bitfinex().get_current_price()
price = format(btc, ".0f")

# config - make args and if none defaults

# currencypair and exchange
pair = "btcusd"
exchange = "bitfinex"

# Set fonts and font sizes
pricefont = ImageFont.truetype(FredokaOne, 36)
timefont = ImageFont.truetype(HankenGroteskMedium, 16)
msgfont = ImageFont.truetype(HankenGroteskMedium, 16)

# Placement of texts.
# x, y starts at top left corner. Display is 212x104px.
# getsize is the size of the text in px, depends on fontsize and amount of text.

wprice, xprice = pricefont.getsize(price)
pricex = 80
pricey = 27

wdate, hdate = timefont.getsize(localtime)
datex = 1
datey = 84

wpair, hpair = msgfont.getsize(pair)
pairx = 0                                                                # Top
pairy = 0                                                                # Left

wex, hex = msgfont.getsize(exchange)
exx = (inky_display.WIDTH - wex)                                         # Top
exy = (inky_display.HEIGHT - hex) - (inky_display.HEIGHT - hex)          # Right

#Debugging text size and placements
print("Price text size: ", wprice, "x", xprice, "px")
print("Price text placement: ", pricex, "x", pricey, "px")
print("Timedate text size: ", wdate, "x", hdate, "px")
print("Timedate text placement: ", datex, "x", datey, "px" )
print("Currency text size: ", wpair, "x", hpair, "px")
print("Currency text placement: ", pairx, "x", pairy, "px")
print("Exchange text size: ", wex, "x", hex, "px")
print("Exchange text placement: ", exx, "x", exy, "px")




# Set the image. Has to be a specific color palette and size.
# I used GIMP to edit one of the example images from the inky git.
# You need the inky-palete.gpl imported and active in GIMP.

"""Create a black background mask to write text and images on. I guess if using
full sized black, white, yellow, red .png image you dont need it? Maybe only for
placing small images?"""
# Set background mask as black image - actually draws 8-bit pixels all over.
bg_mask = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT), (inky_display.BLACK))
#bgimage = Image.open(os.path.join(PATH, "resources/black-backdrop.png"))
draw = ImageDraw.Draw(bg_mask)
# Icons
#usdicon = Image.open(os.path.join(PATH, "resources/usd-icon.png"))
#btcicon = Image.open(os.path.join(PATH, "resources/btc-icon.png"))
#sunicon = Image.open(os.path.join(PATH, "resources/icon-sun.png"))
#sunicon.paste(bgimage, (28, 36), bg_mask)


# My image has black background so im printing text in white.
# White seems to stick to the screen less. Yellow stays even after several cleaning cycles.
# Plan to make this an arg later.
# draw is what to draw on, the image backdrop

draw.text((pricex, pricey), price, inky_display.WHITE, pricefont)
draw.text((datex, datey), localtime, inky_display.WHITE, timefont)
draw.text((pairx, pairy), pair.upper(), inky_display.WHITE, msgfont)
draw.text((exx, exy), exchange.capitalize(), inky_display.WHITE, msgfont)

# Finally print it all
#inky_display.set_image(backdrop)
inky_display.set_image(bg_mask)
inky_display.show()
