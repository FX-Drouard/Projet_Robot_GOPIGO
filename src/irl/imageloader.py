from time import sleep


class ImageLoader:
    """
        Classe qui caputre constament l'image du robot et permet de reccupere l'image à un instant donnée
    """

    def __init__(self, robot):
        self.robot = robot
        self.image = None
        self.run = True

    def boucle(self, fps):
        """
        float -> void
        La boucle de capture des images dans le thread
        """
        while self.run:
            self.image = self.robot.get_image()
            sleep(1./fps)

    def stop(self):
        """
        void -> void
        Permet d'arreter la boucle du thread
        """
        self.run = False

    def get_image(self):
        """
        void -> Image
        Retourne l'image capturée
        """
        return self.image
