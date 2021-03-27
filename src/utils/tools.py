from math import pi, radians, degrees, sqrt, acos, cos, sin


class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        """
        Ajout un point au point courrant
        """
        self.x += other.x
        self.y += other.y

    def __sub__(self, other):
        """
        Retourne la distance entre 2 points
        """
        return sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

    def distance_to_droite(self, droite):
        """
        Retourne la distance entre le point courrant et une doite
        """
        return abs(droite.a * self.x + droite.b * self.y + droite.c) / (sqrt(droite.a ** 2 + droite.b ** 2))

    def __eq__(self, point) -> bool:
        return self.x == point.x and self.y == point.y

    def __ne__(self, point) -> bool:
        return not self.__eq__(point)

    def rotation(self, center, angle):
        angle = radians(angle)
        self.x -= center.x
        self.y -= center.y
        self.x = self.x * cos(angle) + self.y * sin(angle) + center.x
        self.y = -self.x * sin(angle) + self.y * cos(angle) + center.y

    @staticmethod
    def milieu(point1, point2):
        return Point((point1.x + point2.x)/2, (point1.y + point2.y)/2)

    @staticmethod
    def get_points_distance(point, vec_norme, distance):
        vect = vec_norme.vect

        if vect[0] == 0 and vect[1] == 0:
            return None

        if vect[0] == 0:
            b = 0
            a = distance
        elif vect[1] == 0:
            a = 0
            b = distance
        else:
            b = distance / sqrt(vect[1]**2 / vect[0]**2 + 1)
            a = -vect[1] * b / vect[0]

        return Point(point.x + a, point.y + b), Point(point.x - a, point.y - b)

    def __str__(self) -> str:
        return f"({self.x}, {self.y})"


class Vecteur:

    def __init__(self, src, dest):
        self.vect = (dest.x - src.x, dest.y - src.y)

    @staticmethod
    def get_vect_from_angle(ang):
        """
        Construit un vecteur direction depuis un angle donné
        """
        ang = radians(ang)
        return Vecteur(Point(0, 0), Point(round(cos(ang), 2), round(sin(ang), 2)))

    def __mul__(self, other):
        """
        Calcule le produit scalaire de deux vecteur
        """
        return self.vect[0] * other.vect[0] + self.vect[1] * other.vect[1]

    def norme(self):
        """
        Calcule la norme d'un vecteur
        """
        return sqrt(self.vect[0]**2 + self.vect[1] ** 2)

    def angle(self, other):
        """
        Calcule l'angle entre deux vecteur (sans prendre en consideration l'orientation)
        """
        norme_ = self.norme() * other.norme()
        if(norme_ == 0):
            return 0
        return round(degrees(acos(round((self * other) / norme_, 5))), 2)

    def sign(self, other):
        """
        Permet de savoir le signe de l'angle entre les vecteurs
        """
        return self.vect[0] * other.vect[1] - self.vect[1] * other.vect[0]

    def angle_sign(self, other):
        """
        Retourne l'angle signe entre les deux vecteurs
        """
        ang = self.angle(other)
        return ang if self.sign(other) >= 0 else - ang


class Segment:

    def __init__(self, src, dest):
        self.src = src
        self.dest = dest

    def intersection(self, point, vec_unit):

        I = Vecteur(self.src, self.dest)
        J = vec_unit
        denominateur = I.vect[0] * J.vect[1] - I.vect[1] * J.vect[0]

        if denominateur == 0:
            return False

        k = -(self.src.x * J.vect[1] - point.x * J.vect[1] -
              J.vect[0] * self.src.y + J.vect[0] * point.y) / denominateur

        if 0 < k < 1:
            return True

        return False

    def to_droite(self):
        vec_unit = Vecteur(self.src, self.dest)
        vec_norm = Vecteur(
            Point(0, 0), Point(- vec_unit.vect[1], vec_unit.vect[0]))
        return Droite.get_droite(vec_norm, self.src)

    def distance_to_segment(self, other):
        droite = self.to_droite()
        return other.src.distance_to_droite(droite)


class Droite:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    @staticmethod
    def get_droite(vec_norm, point):
        a = vec_norm.vect[0]
        b = vec_norm.vect[1]
        c = - a * point.x - b * point.y
        return Droite(a, b, c)