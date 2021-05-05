from vector import Vector
from projectile import Projectile
import math
import pygame
import os
from personallib.camera import Camera

# Constants
WIN_WIDTH = 800
WIN_HEIGHT = 800
FRAMERATE = 120
ICON_IMG = pygame.image.load(os.path.join("imgs", "icon.png"))

# Pygame Setup
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Projectile Simulation")
pygame.display.set_icon(ICON_IMG)
clock = pygame.time.Clock()

# Objects
cam = Camera(win, 350, -350, 1)
projectiles = [Projectile(0, 0, 10, FRAMERATE), Projectile(0, 0, 10, FRAMERATE)]
active_projectiles = []

# Variables
running = True
f = (0, 0)
fm = 1
size = 10

def get_y(projectile, x, force):
    return projectile.get_curve(x, projectile.get_velocity_magnitude(force) * FRAMERATE, projectile.get_velocity_direction(force), 0) / FRAMERATE

# Main Loop
if __name__ == '__main__':
    while running:

        dt = clock.tick(FRAMERATE) * 0.001

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not projectiles[0].active:
                    projectiles[0].activate()
                    projectiles[0].add_force(f)    
                    active_projectiles.append(projectiles.pop(0))
                    projectiles.append(Projectile(0, 0, size, FRAMERATE))     
                elif event.button == 4:
                    fm = (min(fm + 100, 10000))
                elif event.button == 5:
                    fm = (max(fm - 100, 1))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    if event.key == pygame.K_UP:
                        size = min(size + 1, 25)
                    elif event.key == pygame.K_DOWN:
                        size = max(size - 1, 1)
                    for i in range(len(projectiles)):
                        projectiles.pop(0)
                        projectiles.append(Projectile(0, 0, size, FRAMERATE))
                    
        win.fill((255, 255, 255))

        mpos = pygame.mouse.get_pos()
        mpos = (mpos[0], win.get_size()[1] - mpos[1])
        length = math.hypot(mpos[0], mpos[1])
        unit = (mpos[0] / length, mpos[1] / length)
        f = (unit[0] * fm, unit[1] * fm)
        
        previous_point = (0, get_y(projectiles[0], 0, f))
        for x in range(1, 801):
            y = -get_y(projectiles[0], x * FRAMERATE, f)
            pos = (x, y)
            cam.draw_line(previous_point, pos, (0,0,0))
            previous_point = (x, y)
        
        for projectile in projectiles:
            projectile.draw(cam)

        for projectile in active_projectiles:
            projectile.simulate()
            projectile.draw(cam)
            if not cam.circle_in_bounds(projectile.pos.vector, projectile.size) and projectile.pos.y > 100:
                active_projectiles.pop(active_projectiles.index(projectile))

        pygame.display.update()