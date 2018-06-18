import time

""" This module detects objects using the ultrasonic and sends feedback to the main(radar) module"""

def ultrasonicRead(GPIO, TRIG, ECHO):
    
    # settling the sensor
    GPIO.output(TRIG, False)
    # time.sleep(0.01)

    # send a signal
    GPIO.output(TRIG, True)
    time.sleep(0.0001)
    GPIO.output(TRIG, False)

    # catch a signal
    error = 0
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        error += 1
        if error > 1000:
            break
    if error > 1000:
        return -1

    end_time = time.time()
    while GPIO.input(ECHO) == 1:
        end_time = time.time()

    # calculate the distance 
    total_time = end_time - start_time
    distance = (34300 * total_time) / 2
    distance = round(distance, 2)
    # change the condition if the range is changed
    if distance <= 50:
        return distance
    else:
        return -1
