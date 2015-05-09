__author__ = 'josephelliott'

import time
import datetime
from piglow import PiGlow
from pytz import timezone


def wakeSequence(wakeSeconds, seconds):

    #begin the wake sequence
    #start with just the orange LEDs
    orangeStart = 0
    orangeRampDuration = wakeSeconds
    orangeRamp = 255.0/orangeRampDuration #power per second

    #The then yellow at 10 min
    yellowStart = (wakeSeconds*(1/3.0))
    yellowRampDuration = wakeSeconds - yellowStart
    yellowRamp = 255.0/yellowRampDuration

    #then the white at 5 min
    whiteStart = (wakeSeconds*(2/3.0))
    whiteRampDuration = wakeSeconds - whiteStart
    whiteRamp = 255.0/whiteRampDuration


    if seconds >= orangeStart:
        orangeBrightness = int(orangeRamp*(seconds - (wakeSeconds - orangeRampDuration)))
        print("Orange brightness at %i" % orangeBrightness)
        if orangeBrightness <= 255:
            piglow.orange(orangeBrightness)

    if seconds >= yellowStart:

        yellowBrightness = int(yellowRamp*(seconds - (wakeSeconds - yellowRampDuration)))
        print("Yellow brightness at %i" % yellowBrightness)
        if yellowBrightness <= 255:
            piglow.yellow(yellowBrightness)

    if seconds >= whiteStart:
        whiteBrightness = int(whiteRamp*(seconds - (wakeSeconds - whiteRampDuration)))
        print("White brightness at %i" % whiteBrightness)
        if whiteBrightness <= 255:
            piglow.white(whiteBrightness)



#Run the script
piglow = PiGlow()

hours = 5
minutes = 45
timezone = timezone('US/Eastern')

#Takes 15 minutes to fully wake up
wakeDuration = datetime.timedelta(minutes=15)

#shut off after 10 min at full power
totalDuration = wakeDuration + datetime.timedelta(minutes=10)


try:
    while True:
        #set the wake time then enter the loop
        currentTime = datetime.datetime.now(timezone)

        wakeTime = currentTime.replace(hour=hours, minute=minutes, second=0)

        shutOffTime = wakeTime + totalDuration

        weekend = wakeTime.weekday() > 5 #Monday=0, Sunday=6.

        if wakeTime < currentTime < shutOffTime and (not weekend):
            seconds = currentTime - wakeTime
            print("Wake sequence at %i seconds" % seconds.seconds)
            wakeSequence(wakeDuration.seconds, seconds.seconds)

        else:
            #shut off after 10 min at full power
            print("Sleeping...zzzzz")
            piglow.all(0)

        # sleep for a bit, don't go too fast!
        time.sleep(1)


except KeyboardInterrupt:
    # set all the LEDs to "off" when Ctrl+C is pressed before exiting
    piglow.all(0)