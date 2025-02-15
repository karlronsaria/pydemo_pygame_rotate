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

dir = os.path.dirname(os.path.abspath(__file__))
path = dir + "/res/toddhoward-smile.jpg"
size = (200, 200)


class Todd:
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


class FlyingTodd(Todd):
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


class DoubleTodd:
    def __init__(self, path, size, x, y, angle_update, x_update, y_update, screen_width, screen_height):
        self.todd1 = FlyingTodd(path, size, x, y, angle_update, x_update, y_update)
        self.todd2 = FlyingTodd(path, size, x + width, y + height, angle_update, x_update, y_update)

    def update(self):
        self.todd1.update()
        self.todd2.update()


pygame.init()
width, height = 500, 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Todds")

todd = Todd(dir + "/res/toddhoward-nod.jpeg", (1200, 900), width // 2 - 600, height // 2 - 450, 2)
todds = DoubleTodd(path, size, -100, -100, 7, -2, -2, width, height)

# todo

angle = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # todo

    screen.fill((0, 0, 0))
    todd.update()
    todds.update()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

