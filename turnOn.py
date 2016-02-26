import Practical2.robot_utils as ru
import time

ru.start()

ru.turnLeft(10, wait=False)
time.sleep(0.5)
ru.turnRight(20, wait=False)
time.sleep(0.5)
ru.turnLeft(20, wait=False)
time.sleep(0.5)
ru.turnRight(20, wait=False)
time.sleep(1)

ru.done()
