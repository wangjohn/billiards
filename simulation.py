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

    def run(self, num_steps = 500):
        locations = []
        inversions = []
        for i in xrange(num_steps):
            x, y, inverted = self.step()
            locations.append((x,y))

            if inverted:
                inversions.append(inverted)

        return (locations, inversions)

    def step(self):
        x, y = self.particle.location
        x += self.particle.velocity.x
        y += self.particle.velocity.y

        inverted = self.change_direction(x, y, self.particle.velocity)
        self.particle.location = (x,y)

        return (x, y, inverted)

    def change_direction(self, x, y, velocity, epsilon = 0.01):
        inverted = self.invert_velocity(x, y, velocity)
        if inverted:
            return inverted

        perturbed_x = x + velocity.x * epsilon
        perturbed_y = y + velocity.y * epsilon
        inverted = self.invert_velocity(perturbed_x, perturbed_y, velocity)
        if inverted:
            return inverted
        return False

    def invert_velocity(self, x, y, velocity):
        if not self.square.contains((x,y)):
            if x < self.square.x0 or x > self.square.x1:
                velocity.invert_x()
                return 'x'
            else:
                velocity.invert_y()
                return 'y'
        return False

def plot_locations(locations):
    xvals = []
    yvals = []

    for x,y in locations:
        xvals.append(x)
        yvals.append(y)

    plot(xvals, yvals)
    show()

def minimum_periodic_sequence(sequence):
    potential = []
    while len(potential) == 0 or not valid_periodic_sequence(sequence, potential):
        potential = potential_periodic_sequence(sequence, potential)
        potential.append(sequence[len(potential)])

    return potential

def valid_periodic_sequence(sequence, potential):
    k = len(potential)
    for i in xrange(len(sequence)):
        if sequence[i] != potential[i % k]:
            return False
    return True

def potential_periodic_sequence(sequence, potential_sequence):
    counter = 0
    for val in sequence:
        if len(potential_sequence) > 0 and val == sequence[counter]:
            counter += 1
            if counter >= len(potential_sequence):
                return potential_sequence
        else:
            potential_sequence.extend(sequence[:counter])
            potential_sequence.append(val)
            counter = 0

if __name__ == '__main__':
    square = Rectangle(0.0, 1.0, 0.0, 1.0)
    velocity = VelocityVector(0.0234, 0.0342)
    particle = Particle((0.5, 0.5), velocity)

    simulation = SquareSimulation(square, particle)
    locations, inversions = simulation.run(1500)

    print minimum_periodic_sequence(inversions)
    plot_locations(locations)
