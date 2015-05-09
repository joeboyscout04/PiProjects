import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

file = open("SensorData.txt", "w") #stores data file in same directory as this program file

#time constant values from experimentation
#TODO: feedback loops to adjust these values?
airTimeConstant = 5
waterTimeConstant = 8

#Define function to measure charge time
def RC_Analog(Pin):
    counter=0
    sleepTime = 0.1

    #I've found that the capacitance change is really small, so let's multiply it to get numbers > 1.
    fudgeFactor = 10000
    start_time = time.time()
    #Discharge capacitor
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    time.sleep(sleepTime) #in seconds, suspends execution.
    GPIO.setup(13, GPIO.IN)
#Count loops until voltage across capacitor reads high on GPIO
    while (GPIO.input(13)==GPIO.LOW):
        counter=counter+1
    print counter
    end_time = time.time()
    return ((end_time - start_time)-sleepTime)*fudgeFactor


    #Main program loop
while True:
    time.sleep(1)
    ts = time.time()
    reading = RC_Analog(4) #store counts in a variable
    counter = 0
    time_start = 0
    time_end = 0
    
    print ts, reading  #print counts using GPIO4 and time
    file.write(str(ts) + " " + str(reading) + "\n") #write data to file

    #when the soil is 60% between air and water, it's too dry.
    soilTooDry = (waterTimeConstant - airTimeConstant)*0.6 + airTimeConstant
    dryPercentage = 0.6
    while (reading < soilTooDry):
        time_start = time.time()
        counter = counter + 1
        if counter >= 50:
            break
    time_end = time.time()
    if (counter >= 25 and (time_end - time_start) <= 60): # if you get 25 measurements that indicate dry soil in less than one minute, need to water
        print('Not enough water for your plants to survive! Please water now.') #comment this out for testing
    #else:
        #print('Your plants are safe and healthy, yay!')

GPIO.cleanup()
file.close()
