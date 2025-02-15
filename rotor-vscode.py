import os
import pygame


# link
# - url: <https://stackoverflow.com/questions/4183208/how-do-i-rotate-an-image-around-its-center-using-pygame>
# - retrieved: 2025_02_14
def rot_center(image, rect, angle):
    """rotate a Surface, maintaining position."""
    new_image = pygame.transform.rotate(image, angle)
    rect = new_image.get_rect(center=rect.center)
    return new_image, rect


class Card:
    def __init__(self, path, size, x, y, angle_update):
        self.image = pygame.image.load(path).convert_alpha()
        self.surf = pygame.transform.scale(self.image, size)
        self.original = self.surf
        self.rect = self.image.get_rect()
        self.angle = 0

        self.angle_update = angle_update

        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.surf, self.rect = rot_center(self.original, self.rect, self.angle)
        self.angle += self.angle_update

        screen.blit(self.surf, self.rect)


class FlyingCard(Card):
    def __init__(self, path, size, x, y, angle_update, x_update, y_update):
        super().__init__(path, size, x, y, angle_update)

        self.x_update = x_update
        self.y_update = y_update

    def update(self):
        self.rect.x += self.x_update
        self.rect.y += self.y_update

        w, h = screen.get_size()

        if self.rect.x < -self.rect.width:
            self.rect.x = w + self.rect.width

        if self.rect.y < -self.rect.height:
            self.rect.y = h + self.rect.height

        super().update()


class DoubleCard:
    def __init__(self, path, size, x, y, angle_update, x_update, y_update, screen_width, screen_height):
        self.card1 = FlyingCard(path, size, x, y, angle_update, x_update, y_update)
        self.card2 = FlyingCard(path, size, x + width, y + height, angle_update, x_update, y_update)

    def update(self):
        self.card1.update()
        self.card2.update()


pygame.init()
width, height = 800, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("What")

dir = os.path.dirname(os.path.abspath(__file__))
card = Card(dir + "/res/rotating-background.png", (500, 365), width // 2 - 750, height // 2 - 500, 1)
cards = DoubleCard(dir + "/res/rotating-background-2.png", (333, 243), -100, -100, 2, -2, -2, width, height)

# todo

angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # todo

    screen.fill((0, 0, 0))
    card.update()
    cards.update()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

