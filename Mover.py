import math
import Vector
import pygame

# Gravitational constant, kept as 1 for simplicity could change
G = 100


class Mover:
    def __init__(self, position, velocity, acceleration, size):
        self.pos = position
        self.vel = velocity
        self.acl = acceleration
        self.size = size
        self.mass = self.size * self.size

    def update(self):
        self.vel.add(self.acl)
        self.pos.add(self.vel)
        self.acl.multi(0)

    def update_accel(self, new_accel):
        self.acl = new_accel

    def force_acting(self, force):
        f = Vector.Vector((force.x/self.mass), (force.y/self.mass))
        self.acl.add(f)

    def gravity(self, pos_of_other, mass_of_other):
        grav_direct = Vector.sub_two_vectors(pos_of_other, self.pos)
        r = max(grav_direct.mag, 25)
        grav_val = (G*self.mass*mass_of_other)/(r * r)
        grav_direct.normalise_this()
        gravity = Vector.multiply_new(grav_direct, grav_val)
        self.force_acting(gravity)

    def render(self, screen):
        color = (255, 255, 255)

        pygame.draw.circle(screen, color, (self.pos.x, self.pos.y), self.size, 2)
