from pylab import *

class Container:
    def contains(self, (x,y)):
        raise "Container is an abstract class"

class Rectangle(Container):
    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.width = x1 - x0
        self.height = y1 - y0

    def contains(self, (x,y)):
        return self.x0 <= x and x <= self.x1 and self.y0 <= y and y <= self.y1

class VelocityVector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def magnitude(self):
        return (self.x**2.0 + self.y**2.0)**(0.5)

    def invert_y(self):
        self.y = - self.y

    def invert_x(self):
        self.x = - self.x

class Particle:
    def __init__(self, location, velocity):
        self.location = location
        self.velocity = velocity

class SquareSimulation:
    def __init__(self, square, particle):
        self.square = square
        self.particle = particle

    def step(self):
        x, y = self.particle.location
        x += self.particle.velocity.x
        y += self.particle.velocity.y

        self.change_direction(x, y, self.particle.velocity)
        self.particle.location = (x,y)

        return (x,y)

    def change_direction(self, x, y, velocity, epsilon = 0.01):
        if self.invert_velocity(x, y, velocity):
            return True

        perturbed_x = x + velocity.x * epsilon
        perturbed_y = y + velocity.y * epsilon
        if self.invert_velocity(perturbed_x, perturbed_y, velocity):
            return True
        return False

    def invert_velocity(self, x, y, velocity):
        if not self.square.contains((x,y)):
            if x < self.square.x0 or x > self.square.x1:
                velocity.invert_x()
            else:
                velocity.invert_y()
            return True
        return False

def plot_locations(locations):
    xvals = []
    yvals = []

    for x,y in locations:
        xvals.append(x)
        yvals.append(y)

    plot(xvals, yvals)
    show()

if __name__ == '__main__':
    square = Rectangle(0.0, 1.0, 0.0, 1.0)
    velocity = VelocityVector(0.05, 0.1)
    particle = Particle((0.5, 0.5), velocity)

    simulation = SquareSimulation(square, particle)

    locations = []
    for i in xrange(250):
        simulation.step()
        locations.append(simulation.particle.location)

    plot_locations(locations)


