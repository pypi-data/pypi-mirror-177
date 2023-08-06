from codrone_edu.drone import *
import time

drone = Drone()


def start():  # pairs the drone and makes it takeoff
    drone.pair()
    drone.takeoff()


def move(direction, power, duration):  # used to execute a move in one line of code
    """

    :param direction: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power: int from -100 to 100, 360 to -360 for turns
    :param duration: positive float
    :return:
    """
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


def combo_move_2(direction1, power1, direction2, power2, duration):  # allows two movements in one line of code
    """

    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power1: int 100 to -100
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power2: int 100 to -100
    :param duration: positive float
    :return:
    """
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
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

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
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)
    drone.move(duration)


def combo_move_3(direction1, power1, direction2, power2, direction3, power3, duration):
    """

    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power1: int 100 to -100
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power2: int 100 to -100
    :param direction3: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power3: int 100 to -100
    :param duration: positive float
    :return:
    """
    # combine 3 movements into one line of code
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
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

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
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)

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
        drone.set_yaw(power3)
    elif direction3 == "turn_right":
        drone.set_yaw(-power3)
    drone.move(duration)


def combo_move_4(direction1, power1, direction2, power2, direction3, power3, direction4, power4, duration):
    """

    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power1: int 100 to -100
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power2: int 100 to -100
    :param direction3: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power3: int 100 to -100
    :param direction4: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power4: int 100 to -100
    :param duration: positive float
    :return:
    """
    # combine 4 movements into one line of code
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
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

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
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)

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
        drone.set_yaw(power3)
    elif direction3 == "turn_right":
        drone.set_yaw(-power3)

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
        drone.set_yaw(power4)
    elif direction4 == "turn_right":
        drone.set_yaw(-power4)
    drone.move(duration)


def set_lights(r, g, b, brightness):
    drone.set_drone_LED(r, g, b, brightness)
    drone.set_controller_LED(r, g, b, brightness)
    time.sleep(0.05)


def turn(direction, degrees, duration):
    """

    :param direction: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param degrees: int 360 to -360
    :param duration: positive float
    :return:
    """
    # turn at en exact angle
    if direction == "right":
        drone.turn_degree(-degrees, duration)
    elif direction == "left":
        drone.turn_degree(degrees, duration)


def accurate_move(direction, distance, power):
    """

    :param direction: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param distance: int in inches
    :param power: int 100 to -100
    :return:
    """
    # move for an exact distance
    if direction == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power)
        while distance_calc > distance:
            drone.move(0.05)
    elif direction == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power)
        while distance_calc < distance:
            drone.move(0.05)
    elif direction == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power)
        while distance_calc > distance:
            drone.move(0.05)
    elif direction == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power)
        while distance_calc < distance:
            drone.move(0.05)
    elif direction == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power)
        while distance_calc < distance:
            drone.move(0.05)
    elif direction == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power)
        while distance_calc < distance:
            drone.move(0.05)


def accurate_combo_move_2(direction1, distance1, power1, direction2, distance2, power2, duration):
    """

    :param power2: int 100 to -100
    :param duration: positive float
    :param power1: int 100 to -100
    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param distance1: distance in inches
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param distance2: distance in inches
    :return:
    """
    if direction1 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "turn_left":
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

    if direction2 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "turn_left":
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)
    drone.move(duration)


def accurate_combo_move_3(direction1, distance1, power1, direction2, distance2, power2, direction3, distance3, power3,
                          duration):
    """

    :param distance3: distance in inches
    :param distance2: distance in inches
    :param distance1: distance in inches
    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power1: int 100 to -100
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power2: int 100 to -100
    :param direction3: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power3: int 100 to -100
    :param duration: positive float
    :return:
    """
    # combine 3 movements into one line of code
    if direction1 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "turn_left":
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

    if direction2 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "turn_left":
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)

    if direction3 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power3)
        while distance_calc > distance3:
            drone.move(0.05)
    elif direction3 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power3)
        while distance_calc > distance3:
            drone.move(0.05)
    elif direction3 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "turn_left":
        drone.set_yaw(power3)
    elif direction3 == "turn_right":
        drone.set_yaw(-power3)
    drone.move(duration)


def accurate_combo_move_4(direction1, distance1, power1, direction2, distance2,  power2, direction3, distance3, power3,
                          direction4, distance4, power4, duration):
    """

    :param distance4:
    :param distance3:
    :param distance2:
    :param distance1:
    :param direction1: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power1: int 100 to -100
    :param direction2: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power2: int 100 to -100
    :param direction3: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power3: int 100 to -100
    :param direction4: str(forward, backward, left, right, up, down, turn_left, turn_right)
    :param power4: int 100 to -100
    :param duration: positive float
    :return:
    """
    # combine 4 movements into one line of code
    if direction1 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power1)
        while distance_calc > distance1:
            drone.move(0.05)
    elif direction1 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power1)
        while distance_calc < distance1:
            drone.move(0.05)
    elif direction1 == "turn_left":
        drone.set_yaw(power1)
    elif direction1 == "turn_right":
        drone.set_yaw(-power1)

    if direction2 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power2)
        while distance_calc > distance2:
            drone.move(0.05)
    elif direction2 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power2)
        while distance_calc < distance2:
            drone.move(0.05)
    elif direction2 == "turn_left":
        drone.set_yaw(power2)
    elif direction2 == "turn_right":
        drone.set_yaw(-power2)

    if direction3 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power3)
        while distance_calc > distance3:
            drone.move(0.05)
    elif direction3 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power3)
        while distance_calc > distance3:
            drone.move(0.05)
    elif direction3 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power3)
        while distance_calc < distance3:
            drone.move(0.05)
    elif direction3 == "turn_left":
        drone.set_yaw(power3)
    elif direction3 == "turn_right":
        drone.set_yaw(-power3)

    if direction4 == "forward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(power4)
        while distance_calc > distance4:
            drone.move(0.05)
    elif direction4 == "backward":
        distance_calc = drone.get_pos_z(unit="in")
        drone.set_pitch(-power4)
        while distance_calc < distance4:
            drone.move(0.05)
    elif direction4 == "left":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(-power4)
        while distance_calc > distance4:
            drone.move(0.05)
    elif direction4 == "right":
        distance_calc = drone.get_pos_x(unit="in")
        drone.set_roll(power4)
        while distance_calc < distance4:
            drone.move(0.05)
    elif direction4 == "up":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(power4)
        while distance_calc < distance4:
            drone.move(0.05)
    elif direction4 == "down":
        distance_calc = drone.get_pos_y(unit="in")
        drone.set_throttle(-power4)
        while distance_calc < distance4:
            drone.move(0.05)
    elif direction4 == "turn_left":
        drone.set_yaw(power4)
    elif direction4 == "turn_right":
        drone.set_yaw(-power4)
    drone.move(duration)
