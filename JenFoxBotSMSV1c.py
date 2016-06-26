import RPi.GPIO as GPIO
import datetime
import time
import smtplib
import os
GPIO.setmode(GPIO.BCM)

file = open("SensorData.txt", "w") #stores data file in same directory as this program file

#time constant values from experimentation
#TODO: feedback loops to adjust these values?
airTimeConstant = 3.45
waterTimeConstant = 5.00
#when the soil is 30% between air and water, it's too dry.
dryPercentage = 0.3
soilTooDry = (waterTimeConstant - airTimeConstant)*dryPercentage + airTimeConstant
time_start = datetime.datetime.now()
counter = 0
needsWatering = False

print('Hello World!')
#given a date, return yearmonthday
#April 4, 1987 -> 19870404
def year_month_day(date):

    return int(str(date.year) + str(date.month).zfill(2) + str(date.day).zfill(2))

def send_email():

    smtpUser = os.environ.get('SMTP_USER')
    smtpPass = os.environ.get('SMTP_PASSWORD')

    toAdd = os.environ.get('NOTIFY_USER_EMAIL')

    fromAdd = smtpUser
    subject = 'Plants Need Water!'
    header = "to: "
    body = "Your plants need water.  The Raspberry Pi moisture sensor detected the water level was too low."

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(smtpUser,smtpPass)
    s.sendmail(fromAdd,toAdd,header + '\n' + body)
    s.quit()
    return


#today's year, month and day.
#later check to see if yearmonthday is > current yearmonthday.  if so, flip daily_email to false.
todays_ymd = year_month_day(time_start)
daily_email_sent = False

#Define function to measure charge time
#Take a reading from the moisture sensor.
def RC_Analog(Pin):
    counter_inner=0
    sleep_time = 0.1

    #I've found that the capacitance change is really small, so let's multiply it to get numbers > 1.
    fudge_factor = 10000
    start_time = time.time()
    #Discharge capacitor
    GPIO.setup(13, GPIO.OUT)
    GPIO.output(13, GPIO.LOW)
    time.sleep(sleep_time) #in seconds, suspends execution.
    GPIO.setup(13, GPIO.IN)
#Count loops until voltage across capacitor reads high on GPIO
    while GPIO.input(13)==GPIO.LOW:
        counter_inner=counter_inner+1
    end_time = time.time()
    # print counter
    return ((end_time - start_time)-sleep_time)*fudge_factor




 #Main program loop
while True:

    time.sleep(1)
    ts = datetime.datetime.now()
    reading = RC_Analog(4) #store counts in a variable
    
    print ts, reading  #print counts using GPIO4 and time
    file.write(str(ts) + " " + str(reading) + "\n") #write data to file


    if not needsWatering and reading < soilTooDry:
        print("doesnt need water and reading too dry %s" % soilTooDry)
        counter = counter + 1
    elif needsWatering and reading >= soilTooDry:
        print("needs water and soil is wet %s" % soilTooDry)
        counter = counter + 1


    time_end = datetime.datetime.now()

    if needsWatering: # if you get 25 measurements that indicate dry soil in less than one minute, need to water
        print('Not enough water for your plants to survive! Please water now. counter: %s' % counter) #comment this out for testing
        if not daily_email_sent:
            send_email()
            daily_email_sent = True

    else:
        print('Your plants are safe and healthy, yay! counter: %s' % counter)

    #reset the counter every 60 seconds.
    #if more than 25 readings in 60 seconds are different, flip the state
    if (time_end - time_start).seconds > 60:
        if counter >= 25:
            print("Switch state!")
            needsWatering = not needsWatering
        time_start = datetime.datetime.now()
        counter = 0

    if todays_ymd < year_month_day(ts):

        todays_ymd = year_month_day(ts)
        daily_email_sent = False

GPIO.cleanup()
file.close()
