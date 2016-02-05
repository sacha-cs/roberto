import robot_utils as ru

ru.setupInterface()

while(True):
    result1 = ru.interface.getSensorValue(1)
    if result1:
        if (result1[0] == 1):
            print "bump"
    #result2 = ru.interface.getSensorValue(2)
        #ru.move(-10)
    #else:
        #ru.move(10)

ru.done()
