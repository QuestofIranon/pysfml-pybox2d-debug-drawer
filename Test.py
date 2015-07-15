
from sfmlDebugDraw import sfDebugDraw
import math
from random import *
import sfml as sf
import Box2D
from Box2D import *
from Box2D.b2 import *

TARGET_FPS=60
TIME_STEP=1.0/(TARGET_FPS)

window = sf.RenderWindow(sf.VideoMode(800, 600), "Debug Draw Test")
window.vertical_synchronization = True

DebugDraw = sfDebugDraw(window, 10)

clock = sf.Clock()
is_playing = False

world=b2World(gravity=(0,-9.8), doSleep=True)
world.renderer=DebugDraw

groundBody = world.CreateStaticBody(
	position = (0, 500),
	shapes=b2PolygonShape(box=(80,10))
	)

body = world.CreateDynamicBody(position=(50,20))
box = body.CreatePolygonFixture(box=(7,5), density=1, friction=0)

circlebody = world.CreateDynamicBody(position=(100,10))
circle = circlebody.CreateCircleFixture(radius=1, density = 1, friction = 0.3)
circle.restitution = 0.2

def draw():
	window.clear(sf.Color.BLACK)
	world.DrawDebugData()
	window.display()

def update(delta):

	world.Step(delta, 10, 10)
	world.ClearForces()


def main():

	since_last_update = 0.0

	while window.is_open:


		delta_time = clock.restart().seconds
		since_last_update = since_last_update + delta_time;
		while since_last_update > TIME_STEP:
			since_last_update = since_last_update - TIME_STEP
			
			for event in window.events:
				if type(event) is sf.CloseEvent:
					window.close()


			if sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
				body.ApplyLinearImpulse((-1000.0, 0.0), body.position, True)
				print "Key Pressed"

			if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
				body.ApplyLinearImpulse((1000.0, 0.0), body.position, True)
				print "Key Pressed"

			update(delta_time)

		draw()


if __name__ == '__main__':
	main()