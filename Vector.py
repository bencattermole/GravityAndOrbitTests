import math


class Vector:
    def __init__(self, x_val, y_val):
        self.x = x_val
        self.y = y_val
        self.mag = math.sqrt(self.x*self.x + self.y*self.y)

    def add(self, v_to_add):
        self.x = self.x + v_to_add.x
        self.y = self.y + v_to_add.y

    def sub(self, v_to_sub):
        self.x = self.x - v_to_sub.x
        self.y = self.y - v_to_sub.y

    def multi(self, n):
        self.x = self.x * n
        self.y = self.y * n

    def divide(self, n):
        self.x = self.x / n
        self.y = self.y / n

    def normalise_this(self):
        if self.mag != 0:
            self.divide(self.mag)
        else:
            pass


def normalise_vec(vec):
    m = vec.mag
    new_vec = vec

    if m != 0:
        print(new_vec)
        new_vec = vec.divide(m)
        print(new_vec)
        return new_vec
    else:
        return new_vec


def add_two_vectors(vec1, vec2):
    vec3 = Vector((vec1.x + vec2.x), (vec1.y + vec2.y))
    return vec3


def sub_two_vectors(vec1, vec2):
    vec3 = Vector((vec1.x - vec2.x), (vec1.y - vec2.y))
    return vec3


def multiply_new(vec, n):
    vec2 = Vector((vec.x * n), (vec.y * n))
    return vec2


def dot_product(vec1, vec2):
    dot = (vec1.x * vec2.x) + (vec1.y * vec2.y)
    return dot

