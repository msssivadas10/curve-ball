# `curve-ball`: A Python Script for Simulating Curve Balls 

Simulating the curveball in football with simple physics. In modelling the physics, the only forces considered are the gravity, 
drag and magnus force. Forces like wind are not considered. Also, the ball is assumed as a smooth sphere. 

This code is based on the paper *“The aerodynamics of the beautiful game”* by John W. M. Bush.

## Using the Code

All the necessory things like the `Ball` class are in the `ball.py` module. To create a simulation, first load the necessory classes
from the `ball` module:

```{python} 
>>> from ball import Vector, World, Ball 
```

Simulation settings like gravity or drag coefficient are the attributes of the world object. To create a world with a drag coefficient 
of 0.4 and magnus effect coefficient of 0.5, with default values for other attributes, 

```{python}
>>> world = World(dragConst=0.4, spinConst=0.5)
```

Then create a ball object with some initial position, velocity and spin and link the world object to it.

```{python}
>>> posInit = Vector(50., 10., 0.) # initial position
>>> velInit = Vector.heading(theta=5., phi=35., mag=55.) # initial velocity
>>> Omega   = Vector.heading(theta=45., phi=0., mag=40.) # spin 
>>> ball = Ball(mass=0.45, circ=0.7, spin=Omega) # ball with 0.45 mass and 0.7 circumference
>>> ball.setWorld(world) # link world
>>> ball.setInitialConditions(r0=posInit, v0=velInit, t0=0.) # set initial conditions
```

Then, run the simulation with the forces you want. e.g.,

```{python}
>>> while True:
...   ball.applyForce(gravity=True, drag=True, spin=True) # apply all forces
...   ball.update(dt=0.01)
...   if ball.pos.z <= 0.:
...     break
... 
>>>
```
