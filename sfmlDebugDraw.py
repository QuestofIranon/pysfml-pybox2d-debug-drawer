import sys
from math import floor
from random import *
import sfml as sf
import Box2D
from Box2D import *
from Box2D.b2 import *

class sfDebugDraw:
	SCALE = 32.0

	def __init__(self, window):
		self.window = window


	def ColorToSFML(self, color, alpha = 255):
		return sf.Color((color.r * 255), (color.g * 255), (color.b * 255), alpha)

	def B2VectoSFVec(self, b2_vector, scale_to_pixels = True):
		return sf.Vector(
			b2_vector[0] * (self.SCALE if scale_to_pixels else 1),
			b2_vector[1] * (self.SCALE if scale_to_pixels else 1)
		)

	def DrawPolygon(self, vertices, color):
		
		polygon = sf.ConvexShape()
		
		polygon.point_count = len(vertices)
		
		point_index = 0
		for vertex in vertices:
			trans_vector = B2VectoSFVec(vertex)

			polygon.set_point(point_index, (floor(trans_vector.x), floor(trans_vector.y)))
			point_index = point_index + 1

		polygon.outline_thickness = 1.0
		polygon.fill_color = sf.Color.TRANSPARENT
		polygon.outline_color = ColorToSFML(color)

		self.window.draw(polygon)

	def DrawSolidPolygon(self, vertices, color):
		
		polygon = sf.ConvexShape()
		
		polygon.point_count = len(vertices)
		
		point_index = 0
		for vertex in vertices:
			trans_vector = B2VectoSFVec(vertex)

			polygon.set_point(point_index, (floor(trans_vector.x), floor(trans_vector.y)))
			point_index = point_index + 1

		polygon.outline_thickness = 1.0
		polygon.fill_color = ColorToSFML(color, 60)
		polygon.outline_color = ColorToSFML(color)

		self.window.draw(polygon)

	def DrawCircle(self, center, radius, color):

		circle = sf.CircleShape(radius * SCALE)
		circle.origin = radius * SCALE, radius * SCALE
		circle.position = B2VectoSFVec(center)
		circle.fill_color = sf.COLOR.TRANSPARENT
		circle.outline_thickness = 1.0
		circle.outline_color = ColorToSFML(color)

		self.window.draw(circle)

	def DrawSolidCircle(self, center, radius, axis, color):

		circle = sf.CircleShape(radius * SCALE)
		circle.origin = radius * SCALE, radius * SCALE
		circle.position = B2VectoSFVec(center)
		circle.fill_color = ColorToSFML(color, 60)
		circle.outline_thickness = 1.0
		circle.outline_color = ColorToSFML(color)

		end_point = center + radius * axis

		line = [sf.Vertex(B2VectoSFVec(center), ColorToSFML(color)), sf.Vertex(B2VectoSFVec(end_point), ColorToSFML(color))]

		self.window.draw(circle)
		self.window.draw(line, 2, sf.Lines)

	def DrawSegment(self, point_one, point_two, color):

		line = [sf.Vertex(B2VectoSFVec(point_one), ColorToSFML(color)), sf.Vertex(B2VectoSFVec(point_two), ColorToSFML(color))]

		window.draw(line, 2, sf.Lines)

	def DrawTransform(self, transform):

		line_length = 0.4

		xAxis = transform.position + line_length * transform.R.Col1
		yAxis = transform.position + line_length * transform.R.Col2

		red_line = [(B2VectoSFVec(transform.position), sf.Color.RED), (B2VectoSFVec(xAxis), sf.Color.RED)]
		green_line = [(B2VectoSFVec(transform.position), sf.Color.GREEN), (B2VectoSFVec(yAxis), sf.Color.GREEN)]

		self.window.draw(red_line, 2, sf.Lines)
		self.window.draw(gren_line, 2, sf.Lines)

