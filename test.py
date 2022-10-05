import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection

plt.style.use('ggplot')

c = ["#f86a13", "#f67f1e", "#fa951e", "#f8a723"]

from ball import World, Vector, Ball

world = World(dragConst = 0.4, spinConst = 0.5) # world for simulation

Omega   = Vector.heading( theta = 45.0, phi = 0.0, mag = 40 ) # spin vector

# initital position and velocity
posInit = Vector( 50.0, 10.0, 0.0 ) 
velInit = Vector.heading( theta = 5.0, phi = 35.0, mag = 55.0 )

# ball will be affected by both drag and spin
ball  = Ball(mass = 0.45, circ = 0.7, spin = Omega)
ball.setWorld( world )

# ball is not affected by spin or drag
ball1  = Ball(mass = 0.45, circ = 0.7, spin = Omega)
ball1.setWorld( world )

def test1():

    ball.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball.onGround():
        started  = True
        ball.applyForces(gravity = True, drag = True, spin = False)
        ball.update(0.01)

    
    ball1.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball1.onGround():
        started  = True
        ball1.applyForces(gravity = True, drag = False, spin = False)
        ball1.update(0.01)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = [8, 6])
    
    ax1.plot([pos.x for pos in ball1.path.pos], [pos.z for pos in ball1.path.pos], color=c[3], label="no drag")
    ax1.plot([pos.x for pos in ball.path.pos], [pos.z for pos in ball.path.pos], color=c[0], label="with drag")
    ax1.grid(axis='x')
    ax1.set_xlabel('x')
    ax1.set_ylabel('z')

    ax2.plot([pos.x for pos in ball1.path.pos], [pos.y for pos in ball1.path.pos], color=c[3], label="no drag")
    ax2.plot([pos.x for pos in ball.path.pos], [pos.y for pos in ball.path.pos], color=c[0], label="with drag")
    ax2.grid(axis='x')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

    ax1.legend(loc="lower left", bbox_to_anchor=(0., 1.02, 1, 0.2), fancybox=True, ncol=2, mode="expand")

    plt.tight_layout()

    fig.savefig("Figure_1.png", bbox_inches = 'tight')

    plt.show()


    return 

def test2():

    ball.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball.onGround():
        started  = True
        ball.applyForces(gravity = True, drag = True, spin = True)
        ball.update(0.01)

    
    ball1.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball1.onGround():
        started  = True
        ball1.applyForces(gravity = True, drag = False, spin = False)
        ball1.update(0.01)

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize = [8, 6])
    
    ax1.plot([pos.x for pos in ball1.path.pos], [pos.z for pos in ball1.path.pos], color=c[3], label="no drag+spin")
    ax1.plot([pos.x for pos in ball.path.pos], [pos.z for pos in ball.path.pos], color=c[0], label="with drag+spin")
    ax1.grid(axis='x')
    ax1.set_xlabel('x')
    ax1.set_ylabel('z')

    ax2.plot([pos.x for pos in ball1.path.pos], [pos.y for pos in ball1.path.pos], color=c[3], label="no drag+spin")
    ax2.plot([pos.x for pos in ball.path.pos], [pos.y for pos in ball.path.pos], color=c[0], label="with drag+spin")
    ax2.grid(axis='x')
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')

    ax1.legend(loc="lower left", bbox_to_anchor=(0., 1.02, 1, 0.2), fancybox=True, ncol=2, mode="expand")

    plt.tight_layout()

    fig.savefig("Figure_2.png", bbox_inches = 'tight')

    plt.show()


    return 

def test3():
    
    ball.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball.onGround():
        started  = True
        ball.applyForces(gravity = True, drag = True, spin = True)
        ball.update(0.01)

    
    ball1.setInitialConditions( r0 = posInit, v0 = velInit, t0 = 0.0 )
    started = False
    while not started or not ball1.onGround():
        started  = True
        ball1.applyForces(gravity = True, drag = False, spin = False)
        ball1.update(0.01)


    fig, ax = plt.subplots(1, 1, figsize = [6,8])

    plt.imshow( plt.imread('ground.png'), origin='lower', extent = [0, 100, 0, 65] )

    ax.add_patch( plt.Circle( [85.0, 45.0], 2.0, facecolor = c[0], edgecolor = 'black' ) ) # player 2 team 1
    ax.add_patch( plt.Circle( [50.0, 10.0], 2.0, facecolor = c[0], edgecolor = 'black' ) ) # player 1 team 1
    ax.add_patch( plt.Circle( [86.0, 32.0], 2.0, facecolor = '#004d98', edgecolor = 'black' ) ) # player 1 team 2

    segments, widths = ball1.path.asLineSegments(xvalue='x', yvalue='y', wvalue='z')
    widths = np.exp(np.array(widths))
    lc1 = LineCollection( segments = segments, linewidths = widths, color = c[3], linestyle = '--', alpha = 0.5 )
    ax.add_collection(lc1)
    ax.annotate("", xy=segments[-1][1], xytext=segments[-1][0], arrowprops=dict(arrowstyle="->", color=c[3]))

    segments, widths = ball.path.asLineSegments(xvalue='x', yvalue='y', wvalue='z')
    widths = np.exp(np.array(widths))
    lc2 = LineCollection( segments = segments, linewidths = widths, color = c[3] )
    ax.add_collection(lc2)
    ax.annotate("", xy=segments[-1][1], xytext=segments[-1][0], arrowprops=dict(arrowstyle="->", color=c[3]))

    ax.set( xlim=[45, 100] )
    ax.axis('off')

    plt.tight_layout()
    
    # fig.savefig("Figure_3.png", bbox_inches = 'tight')

    plt.show()

    return


if __name__ == '__main__':
    # test1()
    test2()
    # test3()

