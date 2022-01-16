import pygame
import Mover
import Vector
import random
import math
import time

Screen_Size = 1024
block_size = 4
WHITE = (200, 200, 200)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((Screen_Size, Screen_Size))
pygame.display.set_caption("Orbitals")

'''
path = str(os.path.dirname(__file__))

player_IMG = pygame.image.load(f'{path}/Sprites/Tile_Selector.png').convert()
player_IMG.set_colorkey((0, 0, 0, 0))
# Use the upper-left pixel color as transparent
'''
block_scale = int(Screen_Size/block_size)

clock = pygame.time.Clock()

pygame.init()

pos2 = Vector.Vector(620, 620)
pos = Vector.Vector(420, 420)
vel = Vector.Vector(1, -1)
vel2 = Vector.Vector(-1, 1)
accel = Vector.Vector(0, 0)
accel2 = Vector.Vector(0, 0)

mover = Mover.Mover(pos, vel, accel, 4)
mover2 = Mover.Mover(pos2, vel2, accel2, 4)

running = True

# tic = time.perf_counter()
# toc = time.perf_counter()
# print(f"ran two diffuse in {toc - tic:0.4f} seconds")

scroll = 0.5

'''
not used stuff
x, y = pygame.mouse.get_pos()

    direction_to_accel = Vector.Vector((x - mover.pos.x), (y - mover.pos.y))
    direction_to_accel.normalise_this()
    direction_to_accel.multi(scroll)

    direction_to_accel2 = Vector.Vector((x - mover2.pos.x), (y - mover2.pos.y))
    direction_to_accel2.normalise_this()
    direction_to_accel2.multi(scroll)

    mover.update_accel(direction_to_accel)
    mover2.update_accel(direction_to_accel2)
'''

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                up_vel = Vector.Vector(0, -1)
                mover.vel.add(up_vel)
            if event.key == pygame.K_a:
                left_vel = Vector.Vector(-1, 0)
                mover.vel.add(left_vel)
            if event.key == pygame.K_s:
                down_vel = Vector.Vector(0, 1)
                mover.vel.add(down_vel)
            if event.key == pygame.K_d:
                right_vel = Vector.Vector(1, 0)
                mover.vel.add(right_vel)
            if event.key == pygame.K_x:
                x, y = mover.vel.x, mover.vel.y
                cancel_vel = Vector.Vector(-x, -y)
                mover.vel.add(cancel_vel)
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 5: scroll = max(scroll - 0.1, 0)
            if event.button == 4: scroll = min(scroll + 0.1, 5)

    pygame.display.update()
    screen.fill((0, 0, 0))

    mover.gravity(mover2.pos, mover2.mass)
    mover2.gravity(mover.pos, mover.mass)

    mover.update()
    mover.render(screen)

    mover2.update()
    mover2.render(screen)

    '''
    for points in cast_to:
        rect2 = pygame.rect.Rect((points[0] * block_size, points[1] * block_size, block_size, block_size))
        pygame.draw.rect(screen, WHITE, rect2)
    '''

    clock.tick(30)