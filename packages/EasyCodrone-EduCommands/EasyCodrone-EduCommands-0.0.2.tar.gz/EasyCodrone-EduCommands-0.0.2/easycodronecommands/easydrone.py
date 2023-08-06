from codrone_edu.drone import *
import time

drone = Drone()


def start():  # pairs the drone and makes it takeoff
    drone.pair()
    drone.takeoff()


def move(direction, power, duration):  # used to execute a move in one line of code
    if direction == "forward":
        drone.set_pitch(power)
    elif direction == "backward":
        drone.set_pitch(-power)
    elif direction == "left":
        drone.set_roll(-power)
    elif direction == "right":
        drone.set_roll(power)
    elif direction == "up":
        drone.set_throttle(power)
    elif direction == "down":
        drone.set_throttle(-power)
    if direction == "turn_left":
        drone.turn_degree(-power, duration)
    elif direction == "turn_right":
        drone.turn_degree(power, duration)
    drone.move(duration)


def combo_move_2(direction1, power1, direction2, power2, duration):  # allows multiple movements in one line of code
    if direction1 == "forward":
        drone.set_pitch(power1)
    elif direction1 == "backward":
        drone.set_pitch(-power1)
    elif direction1 == "left":
        drone.set_roll(-power1)
    elif direction1 == "right":
        drone.set_roll(power1)
    elif direction1 == "up":
        drone.set_throttle(power1)
    elif direction1 == "down":
        drone.set_throttle(-power1)
    elif direction1 == "turn_left":
        drone.turn_degree(-power1, duration)
    elif direction1 == "turn_right":
        drone.turn_degree(power1, duration)

    if direction2 == "forward":
        drone.set_pitch(power2)
    elif direction1 == "backward":
        drone.set_pitch(-power2)
    elif direction2 == "left":
        drone.set_roll(-power2)
    elif direction2 == "right":
        drone.set_roll(power2)
    elif direction2 == "up":
        drone.set_throttle(power2)
    elif direction2 == "down":
        drone.set_throttle(-power2)
    elif direction2 == "turn_left":
        drone.turn_degree(-power2, duration)
    elif direction2 == "turn_right":
        drone.turn_degree(power2, duration)
    drone.move(duration)


def combo_move_3(direction1, power1, direction2, power2, direction3, power3, duration):
    if direction1 == "forward":
        drone.set_pitch(power1)
    elif direction1 == "backward":
        drone.set_pitch(-power1)
    elif direction1 == "left":
        drone.set_roll(-power1)
    elif direction1 == "right":
        drone.set_roll(power1)
    elif direction1 == "up":
        drone.set_throttle(power1)
    elif direction1 == "down":
        drone.set_throttle(-power1)
    elif direction1 == "turn_left":
        drone.turn_degree(-power1, duration)
    elif direction1 == "turn_right":
        drone.turn_degree(power1, duration)

    if direction2 == "forward":
        drone.set_pitch(power2)
    elif direction1 == "backward":
        drone.set_pitch(-power2)
    elif direction2 == "left":
        drone.set_roll(-power2)
    elif direction2 == "right":
        drone.set_roll(power2)
    elif direction2 == "up":
        drone.set_throttle(power2)
    elif direction2 == "down":
        drone.set_throttle(-power2)
    elif direction2 == "turn_left":
        drone.turn_degree(-power2, duration)
    elif direction2 == "turn_right":
        drone.turn_degree(power2, duration)

    if direction3 == "forward":
        drone.set_pitch(power3)
    elif direction3 == "backward":
        drone.set_pitch(-power3)
    elif direction3 == "left":
        drone.set_roll(-power3)
    elif direction3 == "right":
        drone.set_roll(power3)
    elif direction3 == "up":
        drone.set_throttle(power3)
    elif direction3 == "down":
        drone.set_throttle(-power3)
    elif direction3 == "turn_left":
        drone.turn_degree(-power3, duration)
    elif direction3 == "turn_right":
        drone.turn_degree(power3, duration)
    drone.move(duration)


def combo_move_4(direction1, power1, direction2, power2, direction3, power3, direction4, power4, duration):
    if direction1 == "forward":
        drone.set_pitch(power1)
    elif direction1 == "backward":
        drone.set_pitch(-power1)
    elif direction1 == "left":
        drone.set_roll(-power1)
    elif direction1 == "right":
        drone.set_roll(power1)
    elif direction1 == "up":
        drone.set_throttle(power1)
    elif direction1 == "down":
        drone.set_throttle(-power1)
    elif direction1 == "turn_left":
        drone.turn_degree(-power1, duration)
    elif direction1 == "turn_right":
        drone.turn_degree(power1, duration)

    if direction2 == "forward":
        drone.set_pitch(power2)
    elif direction1 == "backward":
        drone.set_pitch(-power2)
    elif direction2 == "left":
        drone.set_roll(-power2)
    elif direction2 == "right":
        drone.set_roll(power2)
    elif direction2 == "up":
        drone.set_throttle(power2)
    elif direction2 == "down":
        drone.set_throttle(-power2)
    elif direction2 == "turn_left":
        drone.turn_degree(-power2, duration)
    elif direction2 == "turn_right":
        drone.turn_degree(power2, duration)

    if direction3 == "forward":
        drone.set_pitch(power3)
    elif direction3 == "backward":
        drone.set_pitch(-power3)
    elif direction3 == "left":
        drone.set_roll(-power3)
    elif direction3 == "right":
        drone.set_roll(power3)
    elif direction3 == "up":
        drone.set_throttle(power3)
    elif direction3 == "down":
        drone.set_throttle(-power3)
    elif direction3 == "turn_left":
        drone.turn_degree(-power3, duration)
    elif direction3 == "turn_right":
        drone.turn_degree(power3, duration)

    if direction4 == "forward":
        drone.set_pitch(power4)
    elif direction4 == "backward":
        drone.set_pitch(-power4)
    elif direction4 == "left":
        drone.set_roll(-power4)
    elif direction4 == "right":
        drone.set_roll(power4)
    elif direction4 == "up":
        drone.set_throttle(power4)
    elif direction4 == "down":
        drone.set_throttle(-power4)
    elif direction4 == "turn_left":
        drone.turn_degree(-power4, duration)
    elif direction4 == "turn_right":
        drone.turn_degree(power4, duration)
    drone.move(duration)


def set_lights(r, g, b, brightness):
    drone.set_drone_LED(r, g, b, brightness)
    drone.set_controller_LED(r, g, b, brightness)
    time.sleep(0.05)


def turn(direction, degrees, duration):
    if direction == "right":
        drone.turn_degree(degrees, duration)
    elif direction == "left":
        drone.turn_degree(degrees, duration)
