# !/usr/bin/python3

from typing import Any, Tuple
from math import sqrt, sin, cos, pi as PI


class Vector:

    __slots__ = 'x', 'y', 'z'

    def __init__(self, x: float, y: float, z: float) -> None:

        self.x, self.y, self.z = x, y, z

    def __repr__(self) -> str:
        x, y, z = self.x, self.y, self.z
        return f"Vector({x=:}, {y=:}, {z=:})"

    def get(self, i: str) -> float:

        assert i in 'xyz'
        return self.x if i == 'x' else self.y if i == 'y' else self.z
    
    def mag(self) -> float:

        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def setMag(self, val: float) -> None:

        fact = val / self.mag()

        self.x *= fact
        self.y *= fact
        self.z *= fact

    @classmethod
    def heading(cls, theta: float, phi: float, mag: float = 1.0) -> 'Vector':

        theta, phi = theta * PI / 180.0, phi * PI / 180.0

        x = mag * cos(theta) * cos(phi)
        y = mag * cos(theta) * sin(phi)
        z = mag * sin(theta)

        return cls(x, y, z)

    def __add__(self, other: Any) -> Any:

        if isinstance(other, Vector):
            return Vector( self.x + other.x, self.y + other.y, self.z + other.z )

        return Vector( self.x + other, self.y + other, self.z + other )

    __radd__ = __add__
    
    def __sub__(self, other: Any) -> Any:

        if isinstance(other, Vector):
            return Vector( self.x - other.x, self.y - other.y, self.z - other.z )

        return Vector( self.x - other, self.y - other, self.z - other )

    def __rsub__(self, other: Any) -> Any:

        return Vector( other - self.x, other - self.y, other - self.z )

    def __mul__(self, other: Any) -> Any:

        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y + self.z * other.z 

        return Vector( self.x * other, self.y * other, self.z * other )

    __rmul__ = __mul__

    def __matmul__(self, other: 'Vector') -> 'Vector':

        if not isinstance(other, Vector):
            return NotImplemented

        return Vector(
                        self.y * other.z - self.z * other.y,
                        self.z * other.x - self.x * other.z,
                        self.x * other.y - self.y * other.z
                     )

    def __truediv__(self, other: Any) -> Any:

        if isinstance(other, Vector):
            return NotImplemented

        return Vector( self.x / other, self.y / other, self.z / other )
        

    def __pos__(self):

        return self

    def __neg__(self):

        return Vector( -self.x, -self.y, -self.z )


class World:

    __slots__ = 'airDensity', 'g', 'dragConst', 'spinConst', 

    def __init__(self, g: float = 9.8, airDensity: float = 1.2754, dragConst: float = 1.0, spinConst: float = 1.0) -> None:
        
        self.airDensity = airDensity

        self.g = Vector(0.0, 0.0, -g)

        self.dragConst = dragConst
        self.spinConst = spinConst


class Path:

    __slots__ = 'time', 'pos', 'vel', 'size'

    def __init__(self) -> None:
        
        self.time = []
        self.pos  = []
        self.vel  = []

        self.size = 0

    def push(self, t: float, pos: Vector, vel: Vector) -> None:

        assert isinstance(pos, Vector)
        assert isinstance(vel, Vector)

        self.time.append(t)
        self.pos.append(pos)
        self.vel.append(vel)

        self.size += 1

    def get(self, i: int) -> Tuple[Any, Vector, Vector]:

        assert 0 <= i and i < self.size 
        return self.time[i], self.pos[i], self.vel[i]

    def asLineSegments(self, xvalue: str = 'x', yvalue: str = 'z', wvalue: str = 'y') -> Tuple[list, list]:

        lines, widths = [], []
        for i in range(self.size-1):

            pi, pj = self.pos[i], self.pos[i+1]
            xi, xj = pi.get(xvalue), pj.get(xvalue) 
            yi, yj = pi.get(yvalue), pj.get(yvalue) 
            zi, zj = pi.get(wvalue), pj.get(wvalue)

            wi = 0.5 * ( zi + zj )

            lines.append([(xi, yi), (xj, yj)])
            widths.append(wi)
        
        return lines, widths

    @property
    def xrange(self) -> tuple:

        xmin, xmax = None, None
        for pos in self.pos:
            if xmin is None:
                xmin, xmax = pos.x, pos.x
                continue
            
            xmin, xmax = min(xmin, pos.x), max(xmax, pos.x)
        
        return (xmin, xmax)

    @property
    def yrange(self) -> tuple:

        ymin, ymax = None, None
        for pos in self.pos:
            if ymin is None:
                ymin, ymax = pos.y, pos.y
                continue
            
            ymin, ymax = min(ymin, pos.y), max(ymax, pos.y)
        
        return (ymin, ymax)

    @property
    def zrange(self) -> tuple:

        zmin, zmax = None, None
        for pos in self.pos:
            if zmin is None:
                zmin, zmax = pos.z, pos.z
                continue
            
            zmin, zmax = min(zmin, pos.z), max(zmax, pos.z)
        
        return (zmin, zmax)

class Ball:

    __slots__ = 'radius', 'circ', 'mass', 'crossArea', 'volume', 'spin', 'pos', 'vel', 'acc', 't', 'world', 'path', 

    def __init__(self, mass: float, circ: float, spin: 'Vector'):

        self.circ      = circ
        self.radius    = self.circ / (2 * PI)
        self.crossArea = PI * self.radius**2

        self.volume    = 4/3 * PI * self.radius**3

        self.mass = mass

        assert isinstance( spin, Vector )
        self.spin = spin

        self.pos, self.vel, self.acc, self.t = None, None, None, None

        self.path = Path()

    def setInitialConditions(self, r0: Vector, v0: Vector, t0: float = 0.0) -> None:

        self.pos, self.vel = r0, v0
        self.acc           = Vector(0.0, 0.0, 0.0)
        self.t             = t0

        self.path.push(self.t, self.pos, self.vel)

    def applyGravity(self) -> None:

        self.acc = self.acc + self.world.g

    def applyDrag(self) -> None:

        world = self.world

        dragFactor = 0.5 * world.dragConst * world.airDensity * self.crossArea / self.mass
        dragAcc    = dragFactor * self.vel.mag() * self.vel

        self.acc = self.acc - dragAcc

    def applySpin(self) -> None:

        world = self.world

        spinFactor = self.volume * world.airDensity * world.spinConst / self.mass
        spinAcc    = spinFactor * self.spin @ self.vel

        self.acc = self.acc + spinAcc

    def applyForces(self, gravity: bool = True, drag: bool = False, spin: bool = False) -> None:

        if gravity:
            self.applyGravity()
        if drag:
            self.applyDrag()
        if spin:
            self.applySpin()
        return

    def update(self, dt: float) -> None:

        self.pos = self.pos + self.vel * dt
        self.vel = self.vel + self.acc * dt
        self.t   = self.t + dt

        self.acc = Vector(0.0, 0.0, 0.0)

        self.path.push(self.t, self.pos, self.vel)

    def onGround(self) -> bool:

        return self.pos.z <= 0.0

    def setWorld(self, world: World) -> None:

        self.world = world





