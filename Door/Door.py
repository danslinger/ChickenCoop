import RPi.GPIO as GPIO
import time
import logging

logging.basicConfig(file="/home/pi/doorLog.log",format='%(asctime)s:%(message)s', level=logging.DEBUG)

class Door(object):
    """
    All parameters are GPIO pin numbers.
    """
    def __init__(self, topReed, bottomReed, motor1, motor2):
        super(Door, self).__init__()
        self.topReed = topReed
        self.bottomReed = bottomReed
        self.motor1 = motor1
        self.motor2 = motor2
        self.setupGPIO()
        # self.logger = logging.getLogger() 
        # self.logger.basicConfig(file="/home/pi/doorLog.log",format='%(asctime)s:%(message)s', level=logging.DEBUG)

    def setupGPIO(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.topReed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.bottomReed, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.motor1, GPIO.OUT)
        GPIO.setup(self.motor2, GPIO.OUT)

        GPIO.output(self.motor1, False)
        GPIO.output(self.motor2, False)

    def openDoor(self):
        """
        Opens the door

        Should add a timer so the door doesn't continuously run in the
        event the top reed switch breaks or is inoperative
        If motor stops because of the timer, should log that door
        was stopped via timer and not switch

        Might want to log everything regardless...
        """
        # print "Opening the door"
        if self.doorState(self.topReed) == True:  #this means door is open
            # log something that door is all ready open
            # print "Door is all ready open... I think"
            # self.logger.info("Door was commanded to open, but was all ready open.")
            return "Door was commanded to open, but was already open"
        while self.doorState(self.topReed) != True:
            GPIO.output(self.motor1, True)
            GPIO.output(self.motor2, False)
        #stop door
        GPIO.output(self.motor1, False)
        GPIO.output(self.motor2, False)
        # print "Door should be open now"
        # self.logger.info("Door opened.")
        return "Door opened"

    def closeDoor(self):
        """ 
        Same thing as with openDoor() for timer 
        And for logging things...
        """
        # print "closing the door"
        startTime = time.time()
        if self.doorState(self.bottomReed) == True:
            #door is closed already.  Log that
            # print "Door is already closed... I think"
            # self.logger.info("Door was commanded to closed, but was all ready closed.")
            return "Door was commanded to close, but was already closed"
        while self.doorState(self.bottomReed) != True:
            GPIO.output(self.motor1, False)
            GPIO.output(self.motor2, True)
            if time.time() - startTime > 20:
                GPIO.output(self.motor1, False)
                GPIO.output(self.motor2, False)
                # self.logger.info("Door did not close.  Timeout occurred")
                return "Door did not close.  Timeout occurred"

        # print "found bottom reed"
        GPIO.output(self.motor1, False)
        GPIO.output(self.motor2, True)
        # Short delay to make sure door is closed
        # Use 6 to make sure latches... latch.  Use a shorter value (1?) to just make sure its down.
        time.sleep(2)   
        
        GPIO.output(self.motor1, False)
        GPIO.output(self.motor2, False)
        # self.logger.info("Door closed.")
        return "Door closed"

    def doorState(self, doorPin):
        """
        Checks whether the reed switch on the door is open or not
        When a magnet is present (near the switch) it should return True
        When magnet is away, it should return False
        Assumes pin setup as GPIO.setup(pinNumber, GPIO.IN, pull_up_down = GPIO.PUD.UP)
        """
        if GPIO.input(doorPin):
            return False
        else:
            return True

    def cleanup(self):
        GPIO.cleanup()

    def getDoorStatus(self):
        if self.doorState(self.bottomReed) == True:
            return "Door is closed"
        elif self.doorState(self.topReed) == True:
            return "Door is open"
        else:
            return "Door is part-way open"