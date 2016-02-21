import robot_utils as ru

ru.start()

ru.interface.startLogging('straightlinelog')

ru.move(40)
#ru.turnLeft(90)
#ru.move(40)
#ru.turnLeft(90)
#ru.move(40)
#ru.turnLeft(90)
#ru.move(40)
#ru.turnLeft(90)

ru.interface.stopLogging()

ru.done()
