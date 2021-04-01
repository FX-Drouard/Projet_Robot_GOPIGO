from math import pi
from abc import abstractmethod


class Strategie(object):

    def __init__(self, robot):
        self.robot = robot
        self.is_stop = False
        self.is_start = False
        self.initiale_position = None

    def start(self):
        self.is_stop = False
        self.is_start = True

    def stop(self):
        self.is_stop = True
        self.is_start = False

    @abstractmethod
    def run(self):
        pass


class Avancer(Strategie):

    def __init__(self, robot, distance, vitesse):

        super().__init__(robot)
        self.distance = distance
        self.distance_parcouru = 0
        self.vitesse = vitesse

    def start(self):
        super().start()
        self.initiale_position = self.robot.get_motor_position()[0]
        self.robot.servo_rotate(90)

    def run(self):

        if self.is_stop:
            return

        if not self.is_start:
            self.start()

        diff = self.robot.get_motor_position()[0] - self.initiale_position

        print(diff)
        k = diff // 360
        r = diff % 360

        self.distance_parcouru += k * self.robot.WHEEL_CIRCUMFERENCE + \
            (r * self.robot.WHEEL_CIRCUMFERENCE) / 360

        if self.distance_parcouru >= self.distance or self.robot.get_distance() <= 150:
            self.robot.stop()
            self.stop()
            print("Arret de avancer : ", self.distance_parcouru,
                  self.robot.get_distance())
            return

        self.robot.set_motor_dps(
            self.robot.MOTOR_LEFT + self.robot.MOTOR_RIGHT, self.vitesse)


class Tourner(Strategie):

    GAUCHE = 1
    DROITE = 0

    def __init__(self, robot, angle, orientation, vitesse):
        super().__init__(robot)
        if orientation != self.DROITE and orientation != self.GAUCHE:
            orientation = self.GAUCHE
        self.orientation = orientation
        self.vitesse = vitesse
        self.distance = 2 * pi * robot.WHEEL_BASE_WIDTH * angle / 360
        self.distance_parcouru = 0

    def start(self):
        super().start()
        self.initiale_position = self.robot.get_motor_position()[
            self.orientation]

        if self.orientation == self.GAUCHE:
            self.robot.set_motor_dps(self.robot.MOTOR_LEFT,  0)
            self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, self.vitesse)
        else:
            self.robot.set_motor_dps(self.robot.MOTOR_LEFT,  self.vitesse)
            self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, 0)

    def run(self):

        if self.is_stop:
            return

        if not self.is_start:
            self.start()

        diff = self.robot.get_motor_position()[self.orientation] - \
            self.initiale_position
      
        k = diff // 360
        r = diff % 360

        self.distance_parcouru += k * self.robot.WHEEL_CIRCUMFERENCE + \
            (r * self.robot.WHEEL_CIRCUMFERENCE) / 360
        # print("dist :",self.distance_parcouru,"a dist = ", self.distance)
        if self.robot.get_distance() <= 5 or self.distance_parcouru  >= self.distance:
            self.robot.stop()
            self.stop()
            print("Arret de tourner")
            return

        if self.orientation == self.GAUCHE:
            self.robot.set_motor_dps(self.robot.MOTOR_LEFT,  0)
            self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, self.vitesse)
        else:
            self.robot.set_motor_dps(self.robot.MOTOR_LEFT,  self.vitesse)
            self.robot.set_motor_dps(self.robot.MOTOR_RIGHT, 0)


class Carre(Strategie):

    NB_MAX = 8

    def __init__(self, robot, cote, vitesse, orientation):
        self.avancer = Avancer(robot, cote, vitesse)
        self.tourner = Tourner(robot, 90, orientation, vitesse)
        self.cur = -1
        self.nb = 0

    def start(self):
        super().start()
        self.cur = 0
        self.nb = 0

    def stop(self):
        super().stop()
        self.cur = -1

    def run(self):

        if self.is_stop:
            return

        if not self.is_start:
            self.start()

        if self.nb == self.NB_MAX:
            self.stop()
            return

        if self.cur == 0:
            if not self.avancer.is_start:
                self.avancer.start()

            if not self.avancer.is_stop:
                self.avancer.run()
            else:
                self.cur = 1
                self.nb += 1

        else:
            if not self.tourner.is_start:
                self.tourner.start()

            if not self.tourner.is_stop:
                self.tourner.run()
            else:
                self.cur = 0
                self.nb += 1
