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


class Pulsar(Mover):
    def __init__(self, position, velocity, acceleration, size, angle, angular_velcity):
        Mover.__init__(self, position, velocity, acceleration, size)
        self.ang = angle
        self.ang_vel = angular_velcity
        self.line_len = 2000
        self.rot_x = 0
        self.rot_y = 0
        self.einstein_delay = 10

    def rotate(self):
        if self.ang == 360:
            self.ang = 0
        else:
            self.ang += 0.02

        self.rot_x = self.line_len*math.sin(self.ang)
        self.rot_y = self.line_len*math.cos(self.ang)

    def render_beam(self, screen):
        self.rotate()
        pygame.draw.line(screen, (255, 255, 255), (self.pos.x, self.pos.y), (self.pos.x + self.rot_x, self.pos.y + self.rot_y))
        pygame.draw.line(screen, (255, 255, 255), (self.pos.x, self.pos.y), (self.pos.x - self.rot_x, self.pos.y - self.rot_y))

        test_rot = Vector.Vector(self.rot_x, self.rot_y)
        test_rot.normalise_this()

        dot = Vector.dot_product(self.vel, test_rot)
        self.einstein_delay = dot

        # dot is equivlient to doppler shift effect that causes einstein delay

        pygame.draw.line(screen, (255, 0, 0), (self.pos.x, self.pos.y), (self.pos.x + (self.rot_x/50)*-dot, self.pos.y + (self.rot_y/50)*-dot), 3)
        pygame.draw.line(screen, (0, 0, 255), (self.pos.x, self.pos.y), (self.pos.x + (self.rot_x/50)*dot, self.pos.y + (self.rot_y/50)*dot), 3)