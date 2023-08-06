from math import atan, copysign, cos, pi, sin

from scipy.constants import G

M_EARTH = 5.972e24
VX = 0
VY = 6310.3
MASS = 10
R_EARTH = 6370 * 1000
X = 10000 * 1000
Y = 0


class Sat:
    def __init__(self, mass: float, x: float, y: float, vx: float = 0, vy: float = 0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.ax = 0
        self.ay = 0
        self.mass = mass
        self.acc = 0

    def step(self, dt: float):
        force = -G * M_EARTH * self.mass / (self.dist**2)
        acc_g = force / self.mass
        self.ax = acc_g * cos(self.angle) - self.acc * sin(self.angle)
        self.ay = acc_g * sin(self.angle) + self.acc * cos(self.angle)
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vx += self.ax * dt
        self.vy += self.ay * dt

    def accelerate(self, delta: float):
        self.acc = delta

    @property
    def angle(self) -> float:
        if self.x == 0:
            return copysign(pi / 2, self.y)
        if self.x > 0 and self.y >= 0:
            return atan(self.y / self.x)
        if self.x > 0 and self.y < 0:
            return 2 * pi - atan(abs(self.y / self.x))
        if self.y > 0:
            return pi - atan(abs(self.y / self.x))
        if self.y <= 0:
            return pi + atan(abs(self.y / self.x))

    @property
    def dist(self) -> float:
        return (self.x**2 + self.y**2) ** (1 / 2)

    def __repr__(self) -> str:
        return f"x={self.x:.2f} y={self.y:.2f} vx={self.vx:.2f} vy={self.vy:.2f} dist={self.dist:.2f} angle={self.angle:.2f} m={self.mass:.2f}"


if __name__ == "__main__":
    sat = Sat(MASS, X, Y, VX, VY)
    print(sat.dist)
    for i in range(100000):
        sat.step(1)
        if i % 1000 == 0:
            print(f"{sat.x = } {sat.y = } {sat.dist = } {sat.angle = }")
    print(sat.dist)
