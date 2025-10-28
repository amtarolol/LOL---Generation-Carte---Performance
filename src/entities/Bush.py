import pygame
import os
import random

class Bush(pygame.sprite.Sprite):


    _images = {}

    def __init__(self, pos, bush_type=None):
        super().__init__()

       
        if bush_type is None:
            bush_type = random.choice(["Blue", "Green", "Red"])
        self.bush_type = bush_type

        # Charger ou récupérer l'image depuis le cache
        self.image = self._get_image(bush_type)
        self.rect = self.image.get_rect(center=pos)

        # Position logique
        self.pos = pygame.Vector2(pos)

    @classmethod
    def _get_image(cls, bush_type):

        if bush_type in cls._images:
            return cls._images[bush_type]

        # Chemin du fichier (ex: ./assets/bush/bush_blue.png)
        path = os.path.join("assets", "images","bush", f"bush_{bush_type}.png")

        try:
            image = pygame.image.load(path).convert_alpha()
        except FileNotFoundError:
            raise FileNotFoundError(f"Image de bush introuvable : {path}")

        # Redimension facultative (à ajuster selon ton pixel art)
        image = pygame.transform.scale(image, (32, 32))

        # Mise en cache
        cls._images[bush_type] = image
        return image

    # ---------------------------
    # Méthodes supplémentaires
    # ---------------------------
    @classmethod
    def get_size(cls):

        img = cls._get_image("Green")  # n'importe lequel
        return img.get_size()

