from vector import Vector
import math

class Projectile:
    def __init__(self, x, y, size, framerate):
        self.size = size
        self.mass = 3.14 * (size ** 2)
        self.pos = Vector(x, y)
        self.velocity = Vector(0, 0)
        self.gravity = 9.8 / framerate
        self.forces = []
        self.active = False

    def draw(self, cam):
        cam.draw_circle(self.pos.vector, self.size, (0, 0, 0))

    def add_force(self, force):
        self.forces.append(Vector(force[0], force[1]))

    def add_directional_force(self, magnitude, direction):
        pass
    
    def simulate(self):
        if self.active:
            acceleration = Vector(0, self.gravity)
            for force in self.forces:
                acceleration.x += force.x / self.mass
                acceleration.y -= force.y / self.mass
            self.forces = []
            self.velocity = Vector.Add(self.velocity, acceleration)
            self.pos = Vector.Add(self.pos, self.velocity)
    
    def activate(self):
        self.active = True
        self.velocity = Vector(0, 0)

    def get_velocity_magnitude(self, force):
        v = Vector(force[0] / self.mass, force[1] / self.mass)
        return v.magnitude

    def get_velocity_direction(self, force):
        v = Vector(force[0] / self.mass, force[1] / self.mass) 
        if v.x == 0:
            v.x = 0.0001
        return math.atan(v.y / v.x)

    def get_curve(self, x, magnitude, direction, height):
        return height + (math.tan(direction) * x) - (((9.8 / 2) * (x ** 2)) / ((magnitude ** 2) * (math.cos(direction) ** 2)))

    # y = ((height) + (x * tan(α))) - ((g * x²) / (2 * V₀² * cos²(α)))